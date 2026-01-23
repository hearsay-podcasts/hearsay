# iTunes Artwork Service Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a Python service that fetches high-resolution podcast artwork from Apple's iTunes API during podcast ingestion, storing multiple resolution tiers.

**Architecture:** New `ITunesArtworkService` class using `httpx` for HTTP calls to Apple's public iTunes Search/Lookup API. Integrates into the existing `refresh_best_podcasts_cache` flow in the podcasts route. Falls back to Listen Notes image URL when iTunes lookup fails.

**Tech Stack:** Python 3.11+, httpx, FastAPI, SQLModel, Alembic, pytest

---

### Task 1: Add httpx dependency

**Files:**
- Modify: `backend/pyproject.toml:6-18`

**Step 1: Add httpx to main dependencies**

Move `httpx` from `[project.optional-dependencies].dev` to `[project.dependencies]`:

```toml
dependencies = [
    "fastapi[standard]>=0.115.0",
    "sqlmodel>=0.0.22",
    "psycopg[binary]>=3.2.0",
    "bcrypt>=4.2.0",
    "pyjwt>=2.9.0",
    "pydantic-settings>=2.6.0",
    "python-multipart>=0.0.12",
    "email-validator>=2.2.0",
    "alembic>=1.14.0",
    "tenacity>=9.0.0",
    "podcast-api>=1.1.6",
    "httpx>=0.28.0",
]
```

And remove it from `dev` dependencies:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.8.0",
]
```

**Step 2: Install**

Run: `cd C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend && pip install -e .`

**Step 3: Commit**

```bash
git add backend/pyproject.toml
git commit -m "feat: add httpx as main dependency for iTunes API calls"
```

---

### Task 2: Create the iTunes artwork service

**Files:**
- Create: `backend/app/services/itunes.py`
- Test: `backend/tests/test_itunes_service.py`

**Step 1: Create test file and directory**

Create `backend/tests/__init__.py` (empty) and `backend/tests/test_itunes_service.py`:

```python
import pytest
from unittest.mock import AsyncMock, patch

from app.services.itunes import ITunesArtworkService


class TestBuildArtworkUrls:
    def test_replaces_100x100bb_with_sizes(self):
        service = ITunesArtworkService()
        url = "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/abc/100x100bb.jpg"
        result = service._build_artwork_urls(url)
        assert result == {
            "sm": "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/abc/300x300bb.jpg",
            "md": "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/abc/600x600bb.jpg",
            "lg": "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/abc/100000x100000-999.jpg",
        }

    def test_handles_different_extensions(self):
        service = ITunesArtworkService()
        url = "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/abc/100x100bb.png"
        result = service._build_artwork_urls(url)
        assert result["sm"].endswith("300x300bb.png")
        assert result["md"].endswith("600x600bb.png")
        assert result["lg"].endswith("100000x100000-999.png")

    def test_returns_none_if_pattern_not_found(self):
        service = ITunesArtworkService()
        url = "https://example.com/some-image.jpg"
        result = service._build_artwork_urls(url)
        assert result is None


class TestLookupById:
    @pytest.mark.asyncio
    async def test_returns_artwork_urls_on_success(self):
        service = ITunesArtworkService()
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "resultCount": 1,
            "results": [{"artworkUrl100": "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/abc/100x100bb.jpg"}],
        }

        with patch.object(service.client, "get", return_value=mock_response):
            result = await service.lookup_by_id("12345")

        assert result is not None
        assert result["sm"].endswith("300x300bb.jpg")

    @pytest.mark.asyncio
    async def test_returns_none_on_no_results(self):
        service = ITunesArtworkService()
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"resultCount": 0, "results": []}

        with patch.object(service.client, "get", return_value=mock_response):
            result = await service.lookup_by_id("99999")

        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_on_http_error(self):
        service = ITunesArtworkService()

        with patch.object(service.client, "get", side_effect=Exception("timeout")):
            result = await service.lookup_by_id("12345")

        assert result is None


class TestSearchPodcast:
    @pytest.mark.asyncio
    async def test_returns_artwork_urls_for_first_result(self):
        service = ITunesArtworkService()
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "resultCount": 2,
            "results": [
                {"artworkUrl100": "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/first/100x100bb.jpg"},
                {"artworkUrl100": "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/second/100x100bb.jpg"},
            ],
        }

        with patch.object(service.client, "get", return_value=mock_response):
            result = await service.search_podcast("My Podcast")

        assert result is not None
        assert "first" in result["sm"]

    @pytest.mark.asyncio
    async def test_returns_none_on_no_results(self):
        service = ITunesArtworkService()
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"resultCount": 0, "results": []}

        with patch.object(service.client, "get", return_value=mock_response):
            result = await service.search_podcast("Nonexistent Podcast")

        assert result is None


class TestGetArtworkUrls:
    @pytest.mark.asyncio
    async def test_uses_lookup_when_itunes_id_provided(self):
        service = ITunesArtworkService()
        expected = {"sm": "s", "md": "m", "lg": "l"}

        with patch.object(service, "lookup_by_id", return_value=expected) as mock_lookup:
            result = await service.get_artwork_urls(itunes_id="123", title="Test")

        mock_lookup.assert_called_once_with("123")
        assert result == expected

    @pytest.mark.asyncio
    async def test_falls_back_to_search_when_lookup_fails(self):
        service = ITunesArtworkService()
        expected = {"sm": "s", "md": "m", "lg": "l"}

        with patch.object(service, "lookup_by_id", return_value=None) as mock_lookup, \
             patch.object(service, "search_podcast", return_value=expected) as mock_search:
            result = await service.get_artwork_urls(itunes_id="123", title="Test Pod")

        mock_lookup.assert_called_once_with("123")
        mock_search.assert_called_once_with("Test Pod")
        assert result == expected

    @pytest.mark.asyncio
    async def test_uses_search_when_no_itunes_id(self):
        service = ITunesArtworkService()
        expected = {"sm": "s", "md": "m", "lg": "l"}

        with patch.object(service, "search_podcast", return_value=expected) as mock_search:
            result = await service.get_artwork_urls(itunes_id=None, title="Test Pod")

        mock_search.assert_called_once_with("Test Pod")
        assert result == expected

    @pytest.mark.asyncio
    async def test_returns_none_when_all_methods_fail(self):
        service = ITunesArtworkService()

        with patch.object(service, "lookup_by_id", return_value=None), \
             patch.object(service, "search_podcast", return_value=None):
            result = await service.get_artwork_urls(itunes_id="123", title="Test")

        assert result is None
```

**Step 2: Run tests to verify they fail**

Run: `cd C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend && python -m pytest tests/test_itunes_service.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.services.itunes'`

**Step 3: Write the implementation**

Create `backend/app/services/itunes.py`:

```python
import logging
import re

import httpx

logger = logging.getLogger(__name__)

ITUNES_LOOKUP_URL = "https://itunes.apple.com/lookup"
ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
ARTWORK_PATTERN = re.compile(r"(\d+x\d+)(bb|[^./]*)")


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

        # Get the file extension
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
```

**Step 4: Run tests to verify they pass**

Run: `cd C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend && python -m pytest tests/test_itunes_service.py -v`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add backend/app/services/itunes.py backend/tests/__init__.py backend/tests/test_itunes_service.py
git commit -m "feat: add iTunes artwork service with tests"
```

---

### Task 3: Add itunes_id to Listen Notes PodcastData

**Files:**
- Modify: `backend/app/services/listenotes.py:10-22` and `:70-82`

**Step 1: Add itunes_id field to PodcastData dataclass**

In `backend/app/services/listenotes.py`, add `itunes_id` field after `listenotes_url`:

```python
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
    itunes_id: str | None
```

**Step 2: Extract itunes_id in fetch_best_podcasts**

In the `podcasts.append(...)` call, add `itunes_id`:

```python
                itunes_id = podcast.get("itunes_id")
                if itunes_id is not None:
                    itunes_id = str(itunes_id)

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
                        itunes_id=itunes_id,
                    )
                )
```

**Step 3: Commit**

```bash
git add backend/app/services/listenotes.py
git commit -m "feat: extract itunes_id from Listen Notes API response"
```

---

### Task 4: Add new fields to Podcast model

**Files:**
- Modify: `backend/app/models.py:55-68`

**Step 1: Add fields to PodcastBase**

Add these fields after `listenotes_url` in `PodcastBase`:

```python
class PodcastBase(SQLModel):
    title: str = Field(max_length=500)
    author: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None)
    cover_url: str | None = Field(default=None, max_length=2000)
    feed_url: str | None = Field(default=None, unique=True, index=True, max_length=2000)
    is_featured: bool = Field(default=False, index=True)
    # Listen Notes fields
    listenotes_id: str | None = Field(default=None, unique=True, index=True, max_length=255)
    publisher: str | None = Field(default=None, max_length=500)
    total_episodes: int | None = Field(default=None)
    listen_score: int | None = Field(default=None)
    genre_ids: str | None = Field(default=None, max_length=500)
    listenotes_url: str | None = Field(default=None, max_length=2000)
    # iTunes artwork fields
    itunes_id: str | None = Field(default=None, max_length=255)
    cover_url_sm: str | None = Field(default=None, max_length=2000)
    cover_url_md: str | None = Field(default=None, max_length=2000)
    cover_url_lg: str | None = Field(default=None, max_length=2000)
```

**Step 2: Commit**

```bash
git add backend/app/models.py
git commit -m "feat: add iTunes artwork fields to Podcast model"
```

---

### Task 5: Create Alembic migration

**Files:**
- Create: `backend/app/alembic/versions/<auto>_add_itunes_artwork_fields.py`

**Step 1: Generate migration**

Run: `cd C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend && alembic revision --autogenerate -m "Add iTunes artwork fields"`

**Step 2: Verify the generated migration**

Read the generated file and confirm it adds columns: `itunes_id`, `cover_url_sm`, `cover_url_md`, `cover_url_lg`.

**Step 3: Run migration**

Run: `cd C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend && alembic upgrade head`

**Step 4: Commit**

```bash
git add backend/app/alembic/versions/
git commit -m "feat: add migration for iTunes artwork fields"
```

---

### Task 6: Wire up iTunes service in podcast ingestion

**Files:**
- Modify: `backend/app/api/routes/podcasts.py:48-105`

**Step 1: Update refresh_best_podcasts_cache to use iTunes service**

Replace the `refresh_best_podcasts_cache` function:

```python
import asyncio

from app.services.itunes import ITunesArtworkService

# ... existing imports stay ...

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
        artwork = artwork_map.get(data.listenotes_id)

        # Check if podcast already exists by listenotes_id
        existing = session.exec(
            select(Podcast).where(Podcast.listenotes_id == data.listenotes_id)
        ).first()

        cover_url_sm = artwork["sm"] if artwork else data.cover_url
        cover_url_md = artwork["md"] if artwork else data.cover_url
        cover_url_lg = artwork["lg"] if artwork else data.cover_url

        if existing:
            # Update existing podcast
            existing.title = data.title
            existing.publisher = data.publisher
            existing.author = data.publisher
            existing.description = data.description
            existing.cover_url = data.cover_url
            existing.feed_url = data.feed_url
            existing.total_episodes = data.total_episodes
            existing.listen_score = data.listen_score
            existing.genre_ids = data.genre_ids
            existing.listenotes_url = data.listenotes_url
            existing.is_featured = True
            existing.itunes_id = data.itunes_id
            existing.cover_url_sm = cover_url_sm
            existing.cover_url_md = cover_url_md
            existing.cover_url_lg = cover_url_lg
        else:
            # Create new podcast
            podcast = Podcast(
                title=data.title,
                publisher=data.publisher,
                author=data.publisher,
                description=data.description,
                cover_url=data.cover_url,
                feed_url=data.feed_url,
                listenotes_id=data.listenotes_id,
                total_episodes=data.total_episodes,
                listen_score=data.listen_score,
                genre_ids=data.genre_ids,
                listenotes_url=data.listenotes_url,
                is_featured=True,
                itunes_id=data.itunes_id,
                cover_url_sm=cover_url_sm,
                cover_url_md=cover_url_md,
                cover_url_lg=cover_url_lg,
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
```

**Step 2: Run existing tests (if any) and verify the app starts**

Run: `cd C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend && python -c "from app.main import app; print('OK')"`

**Step 3: Commit**

```bash
git add backend/app/api/routes/podcasts.py
git commit -m "feat: wire iTunes artwork fetching into podcast ingestion"
```

---

### Task 7: Run full test suite and verify

**Step 1: Run all tests**

Run: `cd C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend && python -m pytest tests/ -v`
Expected: All tests PASS

**Step 2: Manual smoke test**

Run: `cd C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend && python -c "from app.services.itunes import ITunesArtworkService; print('Import OK')"`

**Step 3: Final commit if any fixes needed**

---
