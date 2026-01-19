# Hearsay Backend

FastAPI backend for the Hearsay podcast app, based on the [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template).

## Technology Stack

- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM (SQLAlchemy + Pydantic)
- **PostgreSQL** - SQL database (containerized)
- **Alembic** - Database migrations
- **JWT** - Authentication tokens
- **uv** - Fast Python package manager

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.10+ (for local development without Docker)
- [uv](https://docs.astral.sh/uv/) (recommended for local development)

### Using Docker (Recommended)

1. **Start the database:**
   ```bash
   docker compose up -d db
   ```

2. **Start all services:**
   ```bash
   docker compose up -d
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - Adminer (DB admin): http://localhost:8080

### Local Development

1. **Start the database container:**
   ```bash
   docker compose up -d db
   ```

2. **Install dependencies:**
   ```bash
   cd backend
   uv sync
   ```

3. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

4. **Create initial data:**
   ```bash
   python app/initial_data.py
   ```

5. **Start the development server:**
   ```bash
   fastapi dev app/main.py
   ```

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/          # API route handlers
│   │   ├── deps.py          # Dependencies (auth, db)
│   │   └── main.py          # Router aggregation
│   ├── core/
│   │   ├── config.py        # Settings management
│   │   ├── db.py            # Database engine
│   │   └── security.py      # JWT & password utils
│   ├── alembic/             # Database migrations
│   ├── models.py            # SQLModel database models
│   ├── crud.py              # CRUD operations
│   ├── utils.py             # Utility functions
│   └── main.py              # FastAPI app entry point
├── scripts/
│   └── prestart.sh          # Container startup script
├── Dockerfile
├── pyproject.toml           # Dependencies
└── alembic.ini              # Migration config
```

## API Endpoints

### Authentication
- `POST /api/v1/login/access-token` - Get JWT access token
- `POST /api/v1/login/test-token` - Verify token validity

### Users
- `GET /api/v1/users/me` - Get current user
- `POST /api/v1/users/signup` - Register new user
- `PATCH /api/v1/users/me` - Update current user

### Items (Example CRUD)
- `GET /api/v1/items/` - List items
- `POST /api/v1/items/` - Create item
- `GET /api/v1/items/{id}` - Get item
- `PUT /api/v1/items/{id}` - Update item
- `DELETE /api/v1/items/{id}` - Delete item

### Utilities
- `GET /api/v1/utils/health-check/` - Health check

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

## Environment Variables

See `.env` file in the project root for all configuration options.

**Important for production:**
- Change `SECRET_KEY`
- Change `FIRST_SUPERUSER_PASSWORD`
- Change `POSTGRES_PASSWORD`

## Default Credentials

- **Email:** admin@example.com
- **Password:** changethis

⚠️ **Change these for production!**
