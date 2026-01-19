# Coding Conventions

**Analysis Date:** 2026-01-18

## Naming Patterns

**Files:**
- Svelte components: PascalCase for standalone components, lowercase with `+` prefix for SvelteKit routes (`+page.svelte`, `+layout.svelte`, `+page.server.ts`)
- TypeScript/JavaScript: lowercase with extensions (`.ts`, `.server.ts`)
- Python: snake_case (e.g., `core/config.py`, `api/routes/auth.py`)
- Configuration: lowercase with dots (e.g., `svelte.config.js`, `vite.config.ts`, `pyproject.toml`)

**Functions:**
- Python: snake_case (e.g., `get_password_hash`, `create_access_token`, `get_user_by_email`)
- TypeScript/JavaScript: camelCase (e.g., `getTokenFromCookie`, `getCurrentUser`)
- SvelteKit actions: `default` export for primary form action

**Variables:**
- Python: snake_case (e.g., `hashed_password`, `access_token_expires`, `db_obj`)
- TypeScript/JavaScript: camelCase (e.g., `loading`, `formData`, `setCookieHeader`)
- Constants: SCREAMING_SNAKE_CASE (e.g., `API_URL`, `COOKIE_CONFIG`, `ALGORITHM`)
- Svelte 5 reactive state: `$state()` for local reactive values, `$props()` for component props

**Types:**
- Python: PascalCase for classes (e.g., `User`, `UserCreate`, `UserPublic`, `LoginRequest`)
- TypeScript: PascalCase for interfaces (e.g., `User`, `LoginCredentials`, `SignupData`, `ApiError`)
- Type annotations: Union types with `|` (Python and TypeScript both use `str | None` / `string | null`)

## Code Style

**Formatting:**
- Python: Ruff formatter with 88 character line length
- TypeScript: No explicit formatter configured (defaults to Prettier-compatible via Vite/SvelteKit)
- Indentation: Tabs in TypeScript/Svelte, spaces in Python (PEP 8 default)

**Linting:**
- Python: Ruff linter (`pyproject.toml`)
  - Rules: E (errors), F (pyflakes), I (import order), UP (pyupgrade)
  - Ignores: E501 (line too long)
  - Target: Python 3.11+
- TypeScript: svelte-check for type checking
  - Strict mode enabled (`"strict": true` in `tsconfig.json`)
  - Module resolution: bundler

## Import Organization

**Python (`backend/app/`):**
1. Standard library imports (e.g., `from datetime import datetime, timedelta`)
2. Third-party imports (e.g., `from fastapi import FastAPI`, `from sqlmodel import Field`)
3. Local application imports (e.g., `from app.core.config import settings`, `from app import crud`)

**TypeScript (`web/src/`):**
1. SvelteKit imports (e.g., `import { enhance } from '$app/forms'`)
2. Type imports with `type` keyword (e.g., `import type { PageData } from './$types'`)
3. Library imports (e.g., `$lib/server/config`, `$lib/types`)

**Path Aliases:**
- SvelteKit: `$lib` → `src/lib`, `$app` → SvelteKit internal
- Python: Absolute imports from `app` package root

## Error Handling

**Python Backend:**
- Use FastAPI `HTTPException` with appropriate status codes
- Example pattern from `backend/app/api/routes/auth.py`:
```python
if not user:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect email or password",
    )
```
- Security functions return `None` on failure (e.g., `verify_token` returns `str | None`)
- Database operations commit/refresh pattern in CRUD operations

**TypeScript Frontend:**
- SvelteKit `fail()` for form action errors
- Try-catch with console.error for API calls
- Example pattern from `web/src/routes/login/+page.server.ts`:
```typescript
try {
    const response = await fetch(`${API_URL}/auth/login`, {...});
    if (!response.ok) {
        const error = await response.json();
        return fail(response.status, { error: error.detail || 'Login failed' });
    }
} catch (error) {
    console.error('Login error:', error);
    return fail(500, { error: 'An unexpected error occurred' });
}
```

## Logging

**Framework:** console (both frontend and backend)

**Patterns:**
- Backend: Minimal logging, relies on FastAPI's built-in request logging
- Frontend: `console.error` for caught exceptions (e.g., `console.error('Auth check failed:', error)` in `hooks.server.ts`)

## Comments

**When to Comment:**
- Docstrings for all public Python functions/endpoints
- Inline comments for non-obvious logic (e.g., "Extract the cookie from FastAPI response")
- Configuration comments explaining purpose (e.g., "Required for httpOnly cookies")

**JSDoc/TSDoc:**
- Not consistently used in TypeScript files
- Python uses triple-quoted docstrings for API endpoints
- Example from `backend/app/api/routes/auth.py`:
```python
@router.post("/login", response_model=UserPublic)
def login(...) -> UserPublic:
    """
    Login with email and password. Sets httpOnly cookie with JWT.
    """
```

## Function Design

**Size:**
- Backend route handlers: Single-purpose, 20-40 lines typical
- CRUD operations: Small, focused functions (5-15 lines)
- SvelteKit load/actions: Concise, ~10-50 lines

**Parameters:**
- Python: Keyword-only arguments with `*` separator (e.g., `def create_user(*, session: Session, user_create: UserCreate)`)
- FastAPI: Dependency injection via `Annotated` types (e.g., `SessionDep`, `CurrentUser`)
- TypeScript: Destructured parameters for SvelteKit hooks/actions (e.g., `async ({ event, resolve })`)

**Return Values:**
- Python: Explicit type hints always (e.g., `-> User | None`, `-> UserPublic`)
- TypeScript: Type inference preferred, explicit types for complex returns
- FastAPI: Pydantic models for API responses (e.g., `response_model=UserPublic`)

## Module Design

**Exports:**
- Python: Direct imports (no `__all__` defined)
- TypeScript: Named exports for utilities/types, default export for SvelteKit configs
- Svelte components: Default export (implicit)

**Barrel Files:**
- Python: `__init__.py` files exist but are mostly empty
- TypeScript: `$lib/index.ts` exists (minimal usage)

## Type Safety

**Python:**
- Full type hints on all functions
- Pydantic/SQLModel for runtime validation
- Union types with `|` operator (modern Python 3.10+ syntax)

**TypeScript:**
- Strict mode enabled
- Generated types from SvelteKit (`import type { PageData } from './$types'`)
- Interface-based type definitions in `$lib/types.ts`

## Authentication Patterns

**Cookie-based JWT:**
- Backend sets httpOnly cookies via `response.set_cookie()`
- Frontend extracts from request via `event.cookies.get('access_token')`
- Configuration centralized in `COOKIE_CONFIG` (frontend) and route handlers (backend)

**Dependency Injection:**
- Backend uses FastAPI `Depends()` with `Annotated` type aliases
- Pattern: `SessionDep = Annotated[Session, Depends(get_db)]`
- Used for database sessions, authentication, token extraction

## Database Patterns

**ORM:**
- SQLModel (combines SQLAlchemy + Pydantic)
- Model inheritance for shared fields (e.g., `UserBase` → `User`, `UserPublic`)
- Example from `backend/app/models.py`:
```python
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
```

**CRUD Operations:**
- Separate `crud.py` module for database operations
- Keyword-only arguments with session injection
- Commit/refresh pattern for creates

## Svelte 5 Patterns

**Reactivity:**
- Use `$state()` for local reactive variables
- Use `$props()` for component props with destructuring
- Example from `web/src/routes/login/+page.svelte`:
```typescript
let { form }: { form: ActionData } = $props();
let loading = $state(false);
```

**Form Enhancement:**
- Use `use:enhance` directive for progressive enhancement
- Pattern includes loading state management

---

*Convention analysis: 2026-01-18*
