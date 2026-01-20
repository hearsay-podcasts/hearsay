from fastapi import APIRouter, Query
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Podcast, PodcastList, PodcastPublic

router = APIRouter(prefix="/podcasts", tags=["podcasts"])


@router.get("/popular", response_model=PodcastList)
def get_popular_podcasts(
    session: SessionDep,
    limit: int = Query(default=4, ge=1, le=20),
) -> PodcastList:
    """
    Get popular/featured podcasts for the landing page.
    Returns featured podcasts first, then by most recent.
    """
    statement = (
        select(Podcast)
        .order_by(Podcast.is_featured.desc())
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
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Podcast not found",
        )
    return PodcastPublic.model_validate(podcast)
