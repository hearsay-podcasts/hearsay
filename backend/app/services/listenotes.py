import logging
from dataclasses import dataclass

from listennotes import podcast_api

logger = logging.getLogger(__name__)


@dataclass
class PodcastData:
    """Parsed podcast data from Listen Notes API."""

    listenotes_id: str
    title: str
    publisher: str | None
    description: str | None
    cover_url: str | None
    feed_url: str | None
    total_episodes: int | None
    listen_score: int | None
    genre_ids: str | None
    listenotes_url: str | None


class ListenNotesService:
    """Service for interacting with the Listen Notes Podcast API."""

    def __init__(self, api_key: str | None):
        # None = connects to mock server for testing
        self.client = podcast_api.Client(api_key=api_key)

    def fetch_best_podcasts(
        self,
        genre_id: int = 0,
        page: int = 1,
    ) -> list[PodcastData] | None:
        """
        Fetch best podcasts from Listen Notes API.

        Args:
            genre_id: Genre ID to filter by. 0 = overall best podcasts.
            page: Page number for pagination.

        Returns:
            List of PodcastData objects, or None if the API call fails.
        """
        try:
            logger.info(f"Fetching best podcasts from Listen Notes (genre_id={genre_id}, page={page})")
            response = self.client.fetch_best_podcasts(genre_id=genre_id, page=page)
            data = response.json()

            podcasts = []
            for podcast in data.get("podcasts", []):
                genre_ids = podcast.get("genre_ids", [])
                genre_ids_str = ",".join(str(g) for g in genre_ids) if genre_ids else None

                # Handle fields that may be upgrade messages on free tier
                listen_score = podcast.get("listen_score")
                if not isinstance(listen_score, int):
                    listen_score = None

                total_episodes = podcast.get("total_episodes")
                if not isinstance(total_episodes, int):
                    total_episodes = None

                feed_url = podcast.get("rss")
                if feed_url and not feed_url.startswith(("http://", "https://")):
                    feed_url = None

                podcasts.append(
                    PodcastData(
                        listenotes_id=podcast.get("id"),
                        title=podcast.get("title", "Unknown"),
                        publisher=podcast.get("publisher"),
                        description=podcast.get("description"),
                        cover_url=podcast.get("image"),
                        feed_url=feed_url,
                        total_episodes=total_episodes,
                        listen_score=listen_score,
                        genre_ids=genre_ids_str,
                        listenotes_url=podcast.get("listennotes_url"),
                    )
                )

            logger.info(f"Fetched {len(podcasts)} podcasts from Listen Notes")
            return podcasts

        except Exception as e:
            logger.error(f"Listen Notes API error: {e}")
            return None
