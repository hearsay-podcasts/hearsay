import asyncio
import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from app.api.deps import SessionDep
from app.core.config import settings
from app.models import CacheMetadata, Podcast, PodcastList, PodcastPublic
from app.services.itunes import ITunesArtworkService
from app.services.listenotes import ListenNotesService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/podcasts", tags=["podcasts"])

CACHE_KEY_BEST_PODCASTS = "best_podcasts_overall"
CACHE_MAX_AGE_HOURS = 24


def is_cache_fresh(session: SessionDep, cache_key: str, max_age_hours: int = CACHE_MAX_AGE_HOURS) -> bool:
    """Check if the cache for a given key is still fresh."""
    metadata = session.exec(
        select(CacheMetadata).where(CacheMetadata.cache_key == cache_key)
    ).first()

    if not metadata:
        return False

    age = datetime.utcnow() - metadata.last_fetched_at
    return age < timedelta(hours=max_age_hours)


def update_cache_timestamp(session: SessionDep, cache_key: str) -> None:
    """Update or create cache metadata timestamp."""
    metadata = session.exec(
        select(CacheMetadata).where(CacheMetadata.cache_key == cache_key)
    ).first()

    if metadata:
        metadata.last_fetched_at = datetime.utcnow()
    else:
        metadata = CacheMetadata(cache_key=cache_key, last_fetched_at=datetime.utcnow())
        session.add(metadata)

    session.commit()


def refresh_best_podcasts_cache(session: SessionDep) -> bool:
    """
    Fetch best podcasts from Listen Notes and update the database.
    Returns True if successful, False otherwise.
    """
    if not settings.LISTENOTES_API_KEY:
        logger.warning("LISTENOTES_API_KEY not configured, skipping cache refresh")
        return False

    service = ListenNotesService(api_key=settings.LISTENOTES_API_KEY)
    podcasts_data = service.fetch_best_podcasts(genre_id=0, page=1)

    if podcasts_data is None:
        logger.error("Failed to fetch podcasts from Listen Notes API")
        return False

    # Fetch iTunes artwork for each podcast
    artwork_map = _fetch_itunes_artwork(podcasts_data)

    # Upsert podcasts
    for data in podcasts_data:
        # Check if podcast already exists by listenotes_id
        existing = session.exec(
            select(Podcast).where(Podcast.listenotes_id == data.listenotes_id)
        ).first()

        artwork = artwork_map.get(data.listenotes_id)
        cover_url_sm = artwork["sm"] if artwork else data.cover_url
        cover_url_md = artwork["md"] if artwork else data.cover_url
        cover_url_lg = artwork["lg"] if artwork else data.cover_url

        if existing:
            # Update existing podcast
            existing.title = data.title
            existing.publisher = data.publisher
            existing.author = data.publisher  # Map publisher to author for compatibility
            existing.description = data.description
            existing.cover_url = data.cover_url
            existing.feed_url = data.feed_url
            existing.total_episodes = data.total_episodes
            existing.listen_score = data.listen_score
            existing.genre_ids = data.genre_ids
            existing.listenotes_url = data.listenotes_url
            existing.itunes_id = data.itunes_id
            existing.cover_url_sm = cover_url_sm
            existing.cover_url_md = cover_url_md
            existing.cover_url_lg = cover_url_lg
            existing.is_featured = True
        else:
            # Create new podcast
            podcast = Podcast(
                title=data.title,
                publisher=data.publisher,
                author=data.publisher,  # Map publisher to author for compatibility
                description=data.description,
                cover_url=data.cover_url,
                feed_url=data.feed_url,
                listenotes_id=data.listenotes_id,
                total_episodes=data.total_episodes,
                listen_score=data.listen_score,
                genre_ids=data.genre_ids,
                listenotes_url=data.listenotes_url,
                itunes_id=data.itunes_id,
                cover_url_sm=cover_url_sm,
                cover_url_md=cover_url_md,
                cover_url_lg=cover_url_lg,
                is_featured=True,
            )
            session.add(podcast)

    session.commit()
    update_cache_timestamp(session, CACHE_KEY_BEST_PODCASTS)
    logger.info(f"Successfully refreshed best podcasts cache with {len(podcasts_data)} podcasts")
    return True


def _fetch_itunes_artwork(
    podcasts_data: list,
) -> dict[str, dict[str, str]]:
    """
    Fetch iTunes artwork URLs for a list of podcasts.
    Returns a dict mapping listenotes_id -> artwork URLs dict.
    """
    async def _fetch_all():
        itunes_service = ITunesArtworkService()
        results = {}
        try:
            for data in podcasts_data:
                artwork = await itunes_service.get_artwork_urls(
                    itunes_id=data.itunes_id, title=data.title
                )
                if artwork:
                    results[data.listenotes_id] = artwork
                await asyncio.sleep(0.5)  # Rate limit protection
        finally:
            await itunes_service.close()
        return results

    return asyncio.run(_fetch_all())


@router.get("/popular", response_model=PodcastList)
def get_popular_podcasts(
    session: SessionDep,
    limit: int = Query(default=6, ge=1, le=20),
) -> PodcastList:
    """
    Get popular/featured podcasts for the landing page.

    Uses cached data from Listen Notes API. If cache is stale (>24h),
    attempts to refresh from API. Falls back to stale cache if API fails.
    """
    cache_fresh = is_cache_fresh(session, CACHE_KEY_BEST_PODCASTS)

    if not cache_fresh:
        logger.info("Best podcasts cache is stale, attempting refresh")
        refresh_success = refresh_best_podcasts_cache(session)

        if not refresh_success:
            # Check if we have any cached data to fall back to
            cache_metadata = session.exec(
                select(CacheMetadata).where(CacheMetadata.cache_key == CACHE_KEY_BEST_PODCASTS)
            ).first()

            if cache_metadata:
                age_hours = (datetime.utcnow() - cache_metadata.last_fetched_at).total_seconds() / 3600
                logger.warning(f"Listen Notes API failed, serving stale cache (age: {age_hours:.1f} hours)")
            else:
                logger.warning("No cached data available and API failed, returning empty list")

    # Fetch podcasts from database, ordered by listen score
    statement = (
        select(Podcast)
        .where(Podcast.is_featured == True)
        .order_by(Podcast.listen_score.desc())
        .limit(limit)
    )
    podcasts = session.exec(statement).all()

    return PodcastList(
        podcasts=[PodcastPublic.model_validate(p) for p in podcasts],
        count=len(podcasts),
    )


@router.get("/{podcast_id}", response_model=PodcastPublic)
def get_podcast(
    session: SessionDep,
    podcast_id: str,
) -> PodcastPublic:
    """
    Get a specific podcast by ID.
    """
    podcast = session.get(Podcast, podcast_id)
    if not podcast:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Podcast not found",
        )
    return PodcastPublic.model_validate(podcast)
