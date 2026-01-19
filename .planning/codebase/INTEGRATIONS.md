# External Integrations

**Analysis Date:** 2026-01-18

## APIs & External Services

**None detected:**
- No third-party API integrations identified in source code
- Future podcast data sources not yet implemented

## Data Storage

**Databases:**
- PostgreSQL 17
  - Connection: `postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}`
  - Client: SQLModel (SQLAlchemy-based ORM)
  - Configuration: `backend/app/core/config.py` computed field `SQLALCHEMY_DATABASE_URI`
  - Engine creation: `backend/app/core/db.py`
  - Migrations: Alembic (config at `backend/alembic.ini`, migrations in `backend/app/alembic/versions/`)

**File Storage:**
- Local filesystem only (no cloud storage integration detected)

**Caching:**
- None

## Authentication & Identity

**Auth Provider:**
- Custom JWT-based authentication
  - Implementation: `backend/app/core/security.py`
  - Token algorithm: HS256
  - Token expiration: Configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 8 days)
  - Password hashing: bcrypt
  - Cookie-based token storage (httpOnly, sameSite: lax)
  - Frontend cookie config: `web/src/lib/server/config.ts` COOKIE_CONFIG
  - Backend token creation: `create_access_token()`, verification: `verify_token()`

## Monitoring & Observability

**Error Tracking:**
- None

**Logs:**
- Standard output/console only (no centralized logging service)

## CI/CD & Deployment

**Hosting:**
- Not configured (local development only)

**CI Pipeline:**
- None

## Environment Configuration

**Required env vars:**
- `SECRET_KEY` - JWT signing key (backend)
- `POSTGRES_SERVER` - Database host (default: localhost)
- `POSTGRES_PORT` - Database port (default: 5432)
- `POSTGRES_USER` - Database username (default: postgres)
- `POSTGRES_PASSWORD` - Database password (default: postgres)
- `POSTGRES_DB` - Database name (default: hearsay)
- `FRONTEND_HOST` - Frontend URL for CORS (default: http://localhost:5173)
- `BACKEND_CORS_ORIGINS` - Comma-separated allowed origins
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token TTL (default: 11520 = 8 days)
- `ENVIRONMENT` - Deployment environment (local/staging/production)
- `PROJECT_NAME` - Application name (default: Hearsay)
- `API_URL` - Backend API URL for frontend (default: http://localhost:8000/api/v1)

**Secrets location:**
- `.env` in project root (loaded by backend at `backend/.env.example` → `../.env`)
- Template at `backend/.env.example`
- Frontend loads from `$env/dynamic/private` (SvelteKit convention)

## Webhooks & Callbacks

**Incoming:**
- None

**Outgoing:**
- None

## Database Infrastructure

**Docker Setup:**
- Service: `hearsay-postgres` container
- Image: `postgres:17`
- Port mapping: 5432:5432
- Volume: `postgres_data` for persistence
- Health check: `pg_isready` command every 5s
- Configuration: `docker-compose.yml`

---

*Integration audit: 2026-01-18*
