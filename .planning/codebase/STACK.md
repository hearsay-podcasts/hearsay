# Technology Stack

**Analysis Date:** 2026-01-18

## Languages

**Primary:**
- Python 3.13.9 - Backend API (`backend/`)
- TypeScript 5.9.3 - Frontend application (`web/`)

**Secondary:**
- JavaScript (ESM) - Configuration files

## Runtime

**Environment:**
- Node.js v24.11.1 (Frontend)
- Python 3.13.9 (Backend)

**Package Manager:**
- pnpm 10.26.2 (Frontend)
- uv 0.9.26 (Backend Python package manager)
- Lockfile: `web/pnpm-lock.yaml`, `backend/uv.lock` (both present)

## Frameworks

**Core:**
- FastAPI 0.115.0+ - Backend REST API framework with async support
- SvelteKit 2.49.1+ - Frontend meta-framework with SSR
- Svelte 5.45.6+ - UI component framework

**Testing:**
- pytest 8.3.0+ - Backend testing framework (dev dependency)
- pytest-asyncio 0.24.0+ - Async test support (dev dependency)
- httpx 0.28.0+ - HTTP client for API testing (dev dependency)

**Build/Dev:**
- Vite 7.2.6+ - Frontend build tool and dev server
- Hatchling - Python build backend
- Alembic 1.14.0+ - Database migration tool

## Key Dependencies

**Critical:**
- `sqlmodel` 0.0.22+ - ORM combining SQLAlchemy and Pydantic for type-safe database operations
- `psycopg[binary]` 3.2.0+ - PostgreSQL database adapter
- `bcrypt` 4.2.0+ - Password hashing
- `pyjwt` 2.9.0+ - JWT token generation and validation for authentication
- `pydantic-settings` 2.6.0+ - Environment-based configuration management
- `@sveltejs/kit` 2.49.1+ - SvelteKit framework core
- `@sveltejs/vite-plugin-svelte` 6.2.1+ - Svelte integration for Vite

**Infrastructure:**
- `email-validator` 2.2.0+ - Email validation for user registration
- `python-multipart` 0.0.12+ - Form data parsing
- `tenacity` 9.0.0+ - Retry logic for resilient operations
- `ruff` 0.8.0+ - Python linter and formatter (dev)
- `@sveltejs/adapter-auto` 7.0.0+ - Automatic platform adapter for deployment
- `svelte-check` 4.3.4+ - Type checking for Svelte components

## Configuration

**Environment:**
- Backend: `backend/.env.example` template, loads from `../.env` via pydantic-settings
- Frontend: Uses `$env/dynamic/private` from SvelteKit
- Key configs required: `SECRET_KEY`, `POSTGRES_*`, `FRONTEND_HOST`, `BACKEND_CORS_ORIGINS`

**Build:**
- `web/vite.config.ts` - Vite build configuration
- `web/svelte.config.js` - SvelteKit configuration with adapter-auto
- `web/tsconfig.json` - TypeScript compiler options (strict mode enabled)
- `backend/pyproject.toml` - Python project metadata and dependencies
- `backend/alembic.ini` - Database migration configuration
- `backend/pyproject.toml` [tool.ruff] - Linter configuration (line-length: 88, target: py311)

## Platform Requirements

**Development:**
- Python 3.11+ (project specifies >=3.11)
- Node.js (recent version for Vite 7 and SvelteKit 2)
- PostgreSQL 17 (via Docker)
- Docker & Docker Compose (for local database)

**Production:**
- Auto-detected via `@sveltejs/adapter-auto` (supports Node, Vercel, Netlify, Cloudflare)
- Backend: Any platform supporting FastAPI/ASGI (Uvicorn)
- PostgreSQL database

---

*Stack analysis: 2026-01-18*
