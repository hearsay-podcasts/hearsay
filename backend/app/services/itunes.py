import logging

import httpx

logger = logging.getLogger(__name__)

ITUNES_LOOKUP_URL = "https://itunes.apple.com/lookup"
ITUNES_SEARCH_URL = "https://itunes.apple.com/search"


class ITunesArtworkService:
    """Service for fetching high-resolution podcast artwork from iTunes."""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)

    async def close(self):
        await self.client.aclose()

    def _build_artwork_urls(self, artwork_url_100: str) -> dict[str, str] | None:
        """
        Build multiple resolution artwork URLs from an artworkUrl100.

        Replaces the dimension segment (e.g. '100x100bb') with target sizes.
        """
        if "100x100bb" not in artwork_url_100:
            return None

        ext_match = artwork_url_100.rsplit(".", 1)
        if len(ext_match) != 2:
            return None

        ext = ext_match[1]

        return {
            "sm": artwork_url_100.replace(f"100x100bb.{ext}", f"300x300bb.{ext}"),
            "md": artwork_url_100.replace(f"100x100bb.{ext}", f"600x600bb.{ext}"),
            "lg": artwork_url_100.replace(f"100x100bb.{ext}", f"100000x100000-999.{ext}"),
        }

    async def lookup_by_id(self, itunes_id: str) -> dict[str, str] | None:
        """Look up podcast artwork by iTunes ID."""
        try:
            response = await self.client.get(
                ITUNES_LOOKUP_URL, params={"id": itunes_id}
            )
            if response.status_code != 200:
                logger.warning(f"iTunes lookup failed with status {response.status_code}")
                return None

            data = response.json()
            results = data.get("results", [])
            if not results:
                return None

            artwork_url = results[0].get("artworkUrl100")
            if not artwork_url:
                return None

            return self._build_artwork_urls(artwork_url)

        except Exception as e:
            logger.error(f"iTunes lookup error for id={itunes_id}: {e}")
            return None

    async def search_podcast(self, name: str, country: str = "us") -> dict[str, str] | None:
        """Search for podcast artwork by name."""
        try:
            response = await self.client.get(
                ITUNES_SEARCH_URL,
                params={
                    "term": name,
                    "entity": "podcast",
                    "country": country,
                    "limit": 5,
                },
            )
            if response.status_code != 200:
                logger.warning(f"iTunes search failed with status {response.status_code}")
                return None

            data = response.json()
            results = data.get("results", [])
            if not results:
                return None

            artwork_url = results[0].get("artworkUrl100")
            if not artwork_url:
                return None

            return self._build_artwork_urls(artwork_url)

        except Exception as e:
            logger.error(f"iTunes search error for name={name}: {e}")
            return None

    async def get_artwork_urls(
        self, itunes_id: str | None, title: str
    ) -> dict[str, str] | None:
        """
        Get artwork URLs, trying lookup by ID first, then search by name.

        Returns dict with 'sm', 'md', 'lg' keys, or None if all methods fail.
        """
        if itunes_id:
            result = await self.lookup_by_id(itunes_id)
            if result:
                return result

        return await self.search_podcast(title)
