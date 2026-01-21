# Listen Notes API Integration Design

## Overview

Integrate the Listen Notes Podcast API to fetch and cache "best podcasts" data, displaying them on the landing page with popularity badges.

## Requirements

- Fetch best podcasts from Listen Notes API
- Cache results in PostgreSQL for 24 hours
- Serve stale cache if API fails
- Display podcasts on landing page with listen score badges

## Architecture

```
┌─────────────┐     ┌─────────────────────────────────────────────┐
│   Frontend  │     │                  Backend                    │
│  (SvelteKit)│     │                 (FastAPI)                   │
│             │     │                                             │
│ +page.svelte│────▶│  GET /podcasts/popular                      │
│             │     │         │                                   │
└─────────────┘     │         ▼                                   │
                    │  ┌─────────────┐    ┌──────────────────┐   │
                    │  │ Cache Check │───▶│ PostgreSQL       │   │
                    │  │ (< 24h?)    │    │ - podcasts table │   │
                    │  └─────────────┘    │ - cache_metadata │   │
                    │         │           └──────────────────┘   │
                    │         │ stale                             │
                    │         ▼                                   │
                    │  ┌─────────────┐                           │
                    │  │Listen Notes │                           │
                    │  │    API      │                           │
                    │  └─────────────┘                           │
                    └─────────────────────────────────────────────┘
```

### Flow

1. Frontend calls `GET /api/v1/podcasts/popular`
2. Backend checks `cache_metadata` table for last fetch time
3. If cache is fresh (<24h), return podcasts from DB
4. If stale, call Listen Notes API, update DB, return fresh data
5. If API fails but cache exists, serve stale data with warning log

## Database Changes

### Modified `Podcast` Table

Add these fields to the existing model:

| Field | Type | Notes |
|-------|------|-------|
| `listenotes_id` | `str` | Unique ID from Listen Notes (indexed) |
| `publisher` | `str` | Publisher name |
| `total_episodes` | `int` | Episode count |
| `listen_score` | `int` | Listen Notes popularity score (0-100) |
| `genre_ids` | `str` | Comma-separated genre IDs |
| `listenotes_url` | `str` | Link to Listen Notes page |

### New `CacheMetadata` Table

| Field | Type | Notes |
|-------|------|-------|
| `id` | `uuid` | Primary key |
| `cache_key` | `str` | Unique identifier (e.g., "best_podcasts_overall") |
| `last_fetched_at` | `datetime` | When data was last pulled from API |

## Backend Implementation

### Dependencies

Add to `pyproject.toml`:

```toml
podcast-api = "^2.0.0"
```

### Configuration

Add to `.env`:

```
LISTENOTES_API_KEY=your_api_key_here
```

Add to `backend/app/core/config.py`:

```python
class Settings(BaseSettings):
    # ... existing settings
    LISTENOTES_API_KEY: str | None = None
```

### Listen Notes Service

New file: `backend/app/services/listenotes.py`

```python
from listennotes import podcast_api
import logging

logger = logging.getLogger(__name__)

class ListenNotesService:
    def __init__(self, api_key: str | None):
        # None = mock server for testing
        self.client = podcast_api.Client(api_key=api_key)

    def fetch_best_podcasts(
        self,
        genre_id: int = 0,
        page: int = 1
    ) -> dict | None:
        """Fetch best podcasts from Listen Notes API."""
        try:
            response = self.client.fetch_best_podcasts(
                genre_id=genre_id,
                page=page
            )
            return response.json()
        except Exception as e:
            logger.error(f"Listen Notes API error: {e}")
            return None
```

### Field Mapping

| Listen Notes field | Our field |
|-------------------|-----------|
| `id` | `listenotes_id` |
| `title` | `title` |
| `publisher` | `publisher` |
| `image` | `cover_url` |
| `description` | `description` |
| `total_episodes` | `total_episodes` |
| `listen_score` | `listen_score` |
| `genre_ids` | `genre_ids` (joined as string) |
| `listennotes_url` | `listenotes_url` |
| `rss` | `feed_url` |

### Endpoint Logic

Modify `GET /api/v1/podcasts/popular`:

1. Check `cache_metadata` for `best_podcasts_overall`
2. If fresh (< 24h): return podcasts from DB
3. If stale:
   - Call Listen Notes API
   - Upsert podcasts to DB (match on `listenotes_id`)
   - Update `cache_metadata` timestamp
   - Return fresh data
4. If API fails: return stale cache (log warning)

### Error Handling

| Scenario | Behavior |
|----------|----------|
| No API key configured | Log warning, return empty list |
| API returns error (4xx/5xx) | Log error, serve stale cache if available |
| API timeout | Log warning, serve stale cache |
| No cache exists + API fails | Return empty list |
| Rate limited (429) | Log warning, serve stale cache |

## Frontend Implementation

### Type Updates

Update `web/src/lib/types.ts`:

```typescript
export interface Podcast {
  id: string;
  title: string;
  author: string | null;
  description: string | null;
  cover_url: string | null;
  feed_url: string;
  is_featured: boolean;
  // New fields from Listen Notes
  listenotes_id: string | null;
  publisher: string | null;
  total_episodes: number | null;
  listen_score: number | null;
  genre_ids: string | null;
  listenotes_url: string | null;
}
```

### UI Changes

Add listen score badge to podcast cards in `+page.svelte`:

- Position: top-right corner of artwork (absolute)
- Appearance: small pill with score (0-100)
- Color: accent background, cream text
- Only shown if `listen_score` exists

## Files to Modify

1. `backend/pyproject.toml` — add `podcast-api` dependency
2. `backend/app/core/config.py` — add `LISTENOTES_API_KEY` setting
3. `backend/app/models.py` — extend `Podcast`, add `CacheMetadata`
4. `backend/app/services/listenotes.py` — new service (create)
5. `backend/app/api/routes/podcasts.py` — caching logic
6. `backend/app/alembic/versions/` — new migration
7. `web/src/lib/types.ts` — extend `Podcast` type
8. `web/src/routes/+page.svelte` — add badge styling and markup
9. `.env` — add `LISTENOTES_API_KEY`

## API Key Setup

1. Sign up at https://www.listennotes.com/api/
2. Get API key from dashboard (free tier available)
3. Add to `.env` file
