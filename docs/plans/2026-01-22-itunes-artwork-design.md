# iTunes High-Resolution Artwork Service

## Overview

Add a backend service that fetches high-resolution podcast artwork from Apple's iTunes Search/Lookup API. The service is called at podcast ingestion time (when caching from Listen Notes) and stores multiple resolution tiers for frontend use.

## Approach

The iTunes API returns an `artworkUrl100` field containing a CDN URL like:
```
https://is1-ssl.mzstatic.com/image/thumb/.../100x100bb.jpg
```

By manipulating the dimension segment of this URL, we can request arbitrary sizes from Apple's CDN:
- `300x300bb` — small thumbnails
- `600x600bb` — card-sized
- `100000x100000-999` — maximum available resolution (CDN returns the largest it has)

## New Service: `services/itunes.py`

`ITunesArtworkService` class with:

- **`lookup_by_id(itunes_id: str) -> dict | None`** — Calls `https://itunes.apple.com/lookup?id={itunes_id}`, extracts `artworkUrl100`.
- **`search_podcast(name: str, country: str = "us") -> dict | None`** — Calls `https://itunes.apple.com/search?term={name}&entity=podcast&country={country}&limit=5`, picks best match.
- **`_build_artwork_urls(artwork_url_100: str) -> dict`** — Returns `{"sm": "...", "md": "...", "lg": "..."}` by replacing the `100x100bb` segment.

Uses `httpx` for async HTTP. Lookup by ID is preferred; search by name is the fallback.

## Database Changes

New fields on `Podcast` model:

| Field | Type | Description |
|-------|------|-------------|
| `cover_url_sm` | `str \| None` | 300x300 artwork URL |
| `cover_url_md` | `str \| None` | 600x600 artwork URL |
| `cover_url_lg` | `str \| None` | Max resolution artwork URL |
| `itunes_id` | `str \| None` | Apple iTunes ID for direct lookups |

Existing `cover_url` field remains unchanged (Listen Notes source).

New Alembic migration adds these four columns.

## Ingestion Flow

During `fetch_best_podcasts` → save-to-DB:

1. Extract `itunes_id` from Listen Notes response (available as `podcast.get("itunes_id")`)
2. Call `ITunesArtworkService.lookup_by_id(itunes_id)` if available
3. If lookup returns `None`, fall back to `search_podcast(title)`
4. If artwork URLs returned, populate `cover_url_sm`, `cover_url_md`, `cover_url_lg`
5. If both methods fail, set all three fields to the Listen Notes `cover_url` value

## Rate Limiting

Apple's iTunes API is public (no auth required) with an informal limit of ~20 requests/minute. Current ingestion fetches ~6 podcasts per 24-hour cache cycle. A `0.5s` sleep between calls provides safety margin.

## Dependencies

- Add `httpx` to `pyproject.toml`

## Files Touched

- `backend/app/services/itunes.py` — New file
- `backend/app/services/listenotes.py` — Add `itunes_id` to `PodcastData`
- `backend/app/models.py` — Add 4 new fields
- `backend/app/crud.py` — Update podcast save logic
- `backend/app/api/routes/podcasts.py` — Wire up iTunes service during ingestion
- `backend/pyproject.toml` — Add `httpx`
- New Alembic migration

## Frontend

No frontend changes required. The new fields are available for future use. Frontend can use `cover_url_sm`/`cover_url_md`/`cover_url_lg` when ready, falling back to `cover_url` if null.
