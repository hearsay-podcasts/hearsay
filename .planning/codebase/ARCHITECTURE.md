# Architecture

**Analysis Date:** 2026-01-18

## Pattern Overview

**Overall:** Monorepo with Multi-Client Architecture (REST API Backend + Multiple Frontend Clients)

**Key Characteristics:**
- FastAPI backend serving RESTful API with JWT cookie-based authentication
- SvelteKit SSR frontend as primary web client
- Flutter mobile client (scaffold only)
- PostgreSQL database with SQLModel ORM
- Cookie-based session management for web security

## Layers

**Presentation Layer:**
- Purpose: User interface and client-side logic
- Location: `web/src/` (SvelteKit), `mobile/lib/` (Flutter)
- Contains: Svelte components, page routes, server-side load functions, form actions
- Depends on: API Layer via HTTP
- Used by: End users

**API Layer:**
- Purpose: HTTP request handling, routing, authentication, and response formatting
- Location: `backend/app/api/`
- Contains: FastAPI routers, endpoint definitions, dependency injection
- Depends on: Business Logic Layer, Security Layer
- Used by: Presentation Layer

**Business Logic Layer:**
- Purpose: Core application logic and data operations
- Location: `backend/app/crud.py`, `backend/app/core/`
- Contains: CRUD operations, authentication logic, business rules
- Depends on: Data Layer, Security utilities
- Used by: API Layer

**Data Layer:**
- Purpose: Database interaction and persistence
- Location: `backend/app/core/db.py`, `backend/app/models.py`, `backend/app/alembic/`
- Contains: SQLModel models, database engine, Alembic migrations
- Depends on: PostgreSQL database
- Used by: Business Logic Layer

**Security Layer:**
- Purpose: Authentication, authorization, password hashing, token management
- Location: `backend/app/core/security.py`, `backend/app/api/deps.py`
- Contains: JWT creation/verification, bcrypt password hashing, dependency injection for auth
- Depends on: Data Layer (for user lookup)
- Used by: API Layer, Business Logic Layer

## Data Flow

**User Authentication Flow:**

1. User submits credentials via SvelteKit form action (`web/src/routes/login/+page.server.ts`)
2. Form action sends POST to FastAPI endpoint (`backend/app/api/routes/auth.py`)
3. Auth endpoint uses CRUD layer to verify credentials (`backend/app/crud.py`)
4. Security layer hashes/verifies password using bcrypt (`backend/app/core/security.py`)
5. JWT token created and set as httpOnly cookie in response
6. SvelteKit extracts cookie from API response and sets it in browser
7. Subsequent requests include cookie, verified by hooks (`web/src/hooks.server.ts`)
8. Protected endpoints use dependency injection to extract/validate user from cookie (`backend/app/api/deps.py`)

**State Management:**
- Backend: Stateless (JWT tokens contain session data)
- Web Frontend: Server-side locals for user state, passed to client via load functions
- Mobile: Not implemented (scaffold only)

## Key Abstractions

**SQLModel Models:**
- Purpose: Define database schema and validation logic
- Examples: `backend/app/models.py` (User, UserCreate, UserPublic, LoginRequest)
- Pattern: Pydantic-based models with SQLAlchemy table definitions

**Dependency Injection (FastAPI):**
- Purpose: Provide shared resources and enforce authentication
- Examples: `SessionDep` (database session), `CurrentUser` (authenticated user), `TokenDep` (JWT token)
- Pattern: Type-annotated dependencies using `Annotated[T, Depends(func)]`

**SvelteKit Load Functions:**
- Purpose: Server-side data fetching before page render
- Examples: `web/src/routes/+layout.server.ts`, `web/src/routes/dashboard/+page.server.ts`
- Pattern: Async functions returning data to Svelte components

**Form Actions:**
- Purpose: Handle form submissions server-side
- Examples: `web/src/routes/login/+page.server.ts`, `web/src/routes/signup/+page.server.ts`
- Pattern: Export actions object with async handlers

## Entry Points

**Backend (FastAPI):**
- Location: `backend/app/main.py`
- Triggers: HTTP requests to port 8000
- Responsibilities: Initialize FastAPI app, configure CORS, mount API router, expose health check

**Web Frontend (SvelteKit):**
- Location: `web/src/hooks.server.ts` (server hooks), route files under `web/src/routes/`
- Triggers: HTTP requests to port 5173 (dev) or production server
- Responsibilities: Handle authentication state, route requests, render pages

**Mobile (Flutter):**
- Location: `mobile/lib/main.dart`
- Triggers: App launch
- Responsibilities: Initialize Flutter app (currently placeholder)

**Database Migrations:**
- Location: `backend/app/alembic/env.py`
- Triggers: `alembic upgrade head` command
- Responsibilities: Apply schema migrations to PostgreSQL

## Error Handling

**Strategy:** HTTP status codes with structured error responses

**Patterns:**
- FastAPI raises `HTTPException` with status codes and detail messages
- SvelteKit form actions use `fail(status, data)` to return validation errors
- API errors converted to user-friendly messages in frontend
- Uncaught errors logged to console (web: `console.error`, backend: FastAPI default logging)

## Cross-Cutting Concerns

**Logging:** Console output (development), FastAPI default uvicorn logging

**Validation:** Pydantic models on backend, basic client-side validation in forms

**Authentication:** JWT tokens in httpOnly cookies, verified on every request via SvelteKit hooks and FastAPI dependencies

---

*Architecture analysis: 2026-01-18*
