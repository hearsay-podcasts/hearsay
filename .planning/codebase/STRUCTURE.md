# Codebase Structure

**Analysis Date:** 2026-01-18

## Directory Layout

```
hearsay/
├── backend/           # FastAPI REST API
│   ├── app/          # Application code
│   ├── .venv/        # Python virtual environment
│   └── alembic.ini   # Database migration config
├── web/              # SvelteKit web frontend
│   ├── src/          # Source code
│   ├── static/       # Static assets
│   └── node_modules/ # Dependencies
├── mobile/           # Flutter mobile app (scaffold)
│   ├── lib/          # Dart source code
│   └── android/      # Android platform code
├── .planning/        # GSD planning documents
├── .claude/          # Claude Code configuration
└── docker-compose.yml # PostgreSQL database
```

## Directory Purposes

**backend/**
- Purpose: Python FastAPI backend API
- Contains: API routes, business logic, database models, migrations
- Key files: `pyproject.toml` (dependencies), `alembic.ini` (migrations)

**backend/app/**
- Purpose: Core application logic
- Contains: Main app, API routes, models, CRUD operations, core utilities
- Key files: `main.py` (FastAPI app), `models.py` (database models), `crud.py` (data operations)

**backend/app/api/**
- Purpose: API routing and endpoint definitions
- Contains: Route handlers organized by domain
- Key files: `main.py` (API router), `deps.py` (dependency injection), `routes/auth.py` (auth endpoints)

**backend/app/core/**
- Purpose: Core utilities and configuration
- Contains: Settings, database connection, security functions
- Key files: `config.py` (settings), `db.py` (database engine), `security.py` (JWT/password handling)

**backend/app/alembic/**
- Purpose: Database migration management
- Contains: Alembic migration scripts
- Key files: `env.py` (migration environment), `versions/*.py` (migration files)

**web/src/**
- Purpose: SvelteKit application source
- Contains: Routes, components, server-side logic, type definitions
- Key files: `hooks.server.ts` (auth middleware), `app.d.ts` (type definitions)

**web/src/lib/**
- Purpose: Shared libraries and utilities
- Contains: TypeScript types, server config, reusable components
- Key files: `types.ts` (shared types), `server/config.ts` (API URL config)

**web/src/routes/**
- Purpose: File-based routing (SvelteKit convention)
- Contains: Page components, server load functions, form actions
- Key files: `+layout.server.ts` (layout data), `+page.svelte` (page UI), `+page.server.ts` (server logic)

**mobile/lib/**
- Purpose: Flutter application source (scaffold only)
- Contains: Dart widgets and app logic
- Key files: `main.dart` (app entry point)

**.planning/codebase/**
- Purpose: Codebase analysis documents for GSD commands
- Contains: Architecture, structure, conventions, stack, integrations, testing, concerns
- Key files: `ARCHITECTURE.md`, `STRUCTURE.md`

**.claude/**
- Purpose: Claude Code configuration and GSD workflows
- Contains: Agents, commands, hooks, templates
- Key files: `settings.json`, `commands/gsd/*.json`

## Key File Locations

**Entry Points:**
- `backend/app/main.py`: FastAPI application initialization
- `web/src/hooks.server.ts`: SvelteKit server-side hooks (auth middleware)
- `mobile/lib/main.dart`: Flutter app entry point

**Configuration:**
- `backend/pyproject.toml`: Python dependencies and project metadata
- `backend/alembic.ini`: Alembic database migration configuration
- `backend/app/core/config.py`: Application settings (environment-based)
- `web/svelte.config.js`: SvelteKit configuration
- `web/vite.config.ts`: Vite build configuration
- `web/tsconfig.json`: TypeScript compiler options
- `docker-compose.yml`: PostgreSQL database container
- `.env`: Environment variables (backend and frontend)

**Core Logic:**
- `backend/app/models.py`: SQLModel database models and Pydantic schemas
- `backend/app/crud.py`: Database CRUD operations
- `backend/app/core/security.py`: JWT and password hashing
- `backend/app/api/routes/auth.py`: Authentication endpoints
- `web/src/lib/types.ts`: Shared TypeScript types

**Testing:**
- Not yet implemented

## Naming Conventions

**Files:**
- Python: `snake_case.py` (e.g., `app/core/security.py`)
- TypeScript: `camelCase.ts` or `kebab-case.ts` (e.g., `hooks.server.ts`)
- Svelte: `+page.svelte`, `+layout.svelte`, `+page.server.ts` (SvelteKit convention)
- Dart: `snake_case.dart` (e.g., `main.dart`)

**Directories:**
- Lowercase, singular or plural as appropriate (e.g., `routes`, `core`, `api`)
- SvelteKit uses route-based directory names (e.g., `login/`, `dashboard/`)

## Where to Add New Code

**New API Endpoint:**
- Primary code: `backend/app/api/routes/{domain}.py`
- Register in: `backend/app/api/main.py` (add router import and include)
- Models: `backend/app/models.py` (request/response schemas)
- Business logic: `backend/app/crud.py` (or new file for complex domains)

**New Web Page:**
- Implementation: `web/src/routes/{route-name}/+page.svelte`
- Server logic: `web/src/routes/{route-name}/+page.server.ts` (load/actions)
- Layout: `web/src/routes/+layout.svelte` (shared layout)

**New Database Model:**
- Definition: `backend/app/models.py` (SQLModel class)
- Migration: Run `alembic revision --autogenerate -m "description"` from `backend/`
- Apply: Run `alembic upgrade head`

**Shared TypeScript Types:**
- Implementation: `web/src/lib/types.ts`
- Server-only code: `web/src/lib/server/{name}.ts`

**Utilities:**
- Backend shared helpers: `backend/app/core/{utility}.py`
- Frontend shared helpers: `web/src/lib/{utility}.ts`
- Server-only frontend helpers: `web/src/lib/server/{utility}.ts`

## Special Directories

**backend/.venv/**
- Purpose: Python virtual environment
- Generated: Yes (by uv or pip)
- Committed: No

**web/node_modules/**
- Purpose: Node.js dependencies
- Generated: Yes (by pnpm)
- Committed: No

**web/.svelte-kit/**
- Purpose: SvelteKit build artifacts and generated types
- Generated: Yes (by SvelteKit)
- Committed: No

**backend/app/alembic/versions/**
- Purpose: Database migration history
- Generated: Yes (by `alembic revision`)
- Committed: Yes (migrations are version-controlled)

**mobile/.dart_tool/**
- Purpose: Dart build cache
- Generated: Yes (by Flutter)
- Committed: No

**.planning/**
- Purpose: GSD planning and analysis documents
- Generated: Yes (by GSD commands)
- Committed: Depends on workflow (typically yes for persistence)

---

*Structure analysis: 2026-01-18*
