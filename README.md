# Hearsay

A podcast platform built with SvelteKit and FastAPI.

## Project Structure

```
hearsay/
├── backend/          # FastAPI backend
├── web/              # SvelteKit frontend
├── mobile/           # Flutter mobile app (future)
├── docker-compose.yml
└── .env
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- pnpm
- Docker (for PostgreSQL)
- [uv](https://docs.astral.sh/uv/) (Python package manager)

## Getting Started

### 1. Start the Database

```bash
docker compose up -d
```

### 2. Setup Backend

```bash
cd backend

# Install dependencies
uv sync

# Run database migrations
uv run alembic upgrade head

# Start the development server
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### 3. Setup Frontend

```bash
cd web

# Install dependencies
pnpm install

# Start the development server
pnpm dev
```

The frontend will be available at `http://localhost:5173`

## Environment Variables

Copy `.env` and update the values for production:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing key (change in production!) | Auto-generated |
| `POSTGRES_SERVER` | Database host | `localhost` |
| `POSTGRES_PORT` | Database port | `5432` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `postgres` |
| `POSTGRES_DB` | Database name | `hearsay` |
| `FRONTEND_HOST` | Frontend URL for CORS | `http://localhost:5173` |

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/signup` | Create new account |
| POST | `/api/v1/auth/login` | Login and get JWT cookie |
| POST | `/api/v1/auth/logout` | Clear JWT cookie |
| GET | `/api/v1/auth/me` | Get current user info |

## Development

### Backend Commands

```bash
cd backend

# Run server with auto-reload
uv run uvicorn app.main:app --reload

# Create a new migration
uv run alembic revision --autogenerate -m "Description"

# Apply migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1
```

### Frontend Commands

```bash
cd web

# Development server
pnpm dev

# Type checking
pnpm check

# Build for production
pnpm build

# Preview production build
pnpm preview
```

## Tech Stack

**Backend:**
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- PostgreSQL
- Alembic (migrations)
- JWT authentication (httpOnly cookies)

**Frontend:**
- SvelteKit 2
- Svelte 5 (with runes)
- TypeScript

## License

MIT