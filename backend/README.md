# Backend API

A FastAPI backend with PostgreSQL database and JWT authentication.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Copy the example environment file and update the values:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials and a secure JWT secret key.

### 3. Set up PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE app;
```

Update `DATABASE_URL` in `.env` with your connection string.

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create a new user |
| POST | `/auth/login` | Get access token |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get current user profile |
| PUT | `/users/me` | Update current user |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |

## Project Structure

```
app/
├── main.py           # FastAPI application entry point
├── config.py         # Settings and configuration
├── database.py       # Database connection and session
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
├── services/         # Business logic
└── routers/          # API endpoints
```
