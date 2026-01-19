# Testing Patterns

**Analysis Date:** 2026-01-18

## Test Framework

**Runner:**
- Backend: pytest 8.3.0+
- Frontend: Not configured (no test files or configuration detected)

**Configuration:**
- Backend: `pyproject.toml` lists `pytest>=8.3.0`, `pytest-asyncio>=0.24.0`, `httpx>=0.28.0` in dev dependencies
- Frontend: No test framework installed

**Run Commands:**
```bash
# Backend tests (expected usage)
pytest                       # Run all tests
pytest --asyncio-mode=auto  # With async support
pytest --cov=app            # Coverage (if pytest-cov installed)

# Frontend tests
# No test commands configured
```

## Test File Organization

**Location:**
- Backend: Test files not yet created
- Frontend: Test files not yet created

**Naming:**
- Python convention: `test_*.py` or `*_test.py`
- No established frontend testing pattern yet

**Structure:**
```
Expected backend structure:
backend/
├── app/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_crud.py
│   │   └── test_security.py

Expected frontend structure:
web/
├── src/
│   ├── lib/
│   │   └── __tests__/
│   └── routes/
│       └── __tests__/
```

## Test Structure

**Suite Organization:**
```python
# Expected pattern based on FastAPI/pytest best practices
import pytest
from fastapi.testclient import TestClient

def test_login_success(client: TestClient, db_session):
    """Test successful login flow."""
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.cookies
```

**Patterns:**
- Pytest fixtures for database sessions and test clients
- Async test support via pytest-asyncio
- Descriptive test names with docstrings

## Mocking

**Framework:** httpx for testing FastAPI (included in dev dependencies)

**Expected Patterns:**
```python
# Database mocking
@pytest.fixture
def db_session():
    """Create a test database session."""
    # Setup test database
    yield session
    # Teardown

# External API mocking
@pytest.fixture
def mock_api(monkeypatch):
    """Mock external API calls."""
    def mock_fetch(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr('httpx.get', mock_fetch)
```

**What to Mock:**
- Database connections (use test database or in-memory)
- External API calls
- Time-dependent functions (datetime.now)
- File I/O operations

**What NOT to Mock:**
- Business logic functions
- Data validation (Pydantic models)
- Password hashing/verification (test real implementation)

## Fixtures and Factories

**Test Data:**
```python
# Expected pattern for test users
@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    }

@pytest.fixture
def test_user(db_session, test_user_data):
    """Create a test user in the database."""
    user = crud.create_user(
        session=db_session,
        user_create=UserCreate(**test_user_data)
    )
    return user
```

**Location:**
- Backend: `backend/app/tests/conftest.py` (expected)
- Shared fixtures in root conftest, specialized fixtures in test files

## Coverage

**Requirements:** Not enforced (no coverage configuration detected)

**View Coverage:**
```bash
# Install pytest-cov if needed
pip install pytest-cov

# Run with coverage
pytest --cov=app --cov-report=html
pytest --cov=app --cov-report=term-missing
```

## Test Types

**Unit Tests:**
- Scope: Individual functions in isolation
- Focus areas:
  - `backend/app/core/security.py`: password hashing, token creation/verification
  - `backend/app/crud.py`: database operations
  - `backend/app/models.py`: Pydantic validation

**Integration Tests:**
- Scope: API endpoints with database
- Focus areas:
  - `backend/app/api/routes/auth.py`: login, signup, logout flows
  - Cookie setting and extraction
  - Authentication middleware
- Approach: Use TestClient with test database

**E2E Tests:**
- Framework: Not configured
- Recommended: Playwright for SvelteKit frontend testing

## Common Patterns

**Async Testing:**
```python
# pytest-asyncio is included in dev dependencies
import pytest

@pytest.mark.asyncio
async def test_async_operation():
    """Test asynchronous operations."""
    result = await some_async_function()
    assert result == expected
```

**Error Testing:**
```python
# Testing expected exceptions
import pytest
from fastapi import HTTPException

def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    response = client.post("/api/v1/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 400
    assert "Incorrect email or password" in response.json()["detail"]

def test_authentication_required(client: TestClient):
    """Test endpoints that require authentication."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
```

**Database Testing:**
```python
# Expected pattern for database tests
def test_create_user(db_session):
    """Test user creation."""
    user_data = UserCreate(
        email="new@example.com",
        password="password123",
        full_name="New User"
    )
    user = crud.create_user(session=db_session, user_create=user_data)

    assert user.id is not None
    assert user.email == "new@example.com"
    assert user.hashed_password != "password123"
    assert verify_password("password123", user.hashed_password)
```

## Testing Dependencies

**Backend (from `pyproject.toml`):**
- pytest >= 8.3.0 - Test runner
- pytest-asyncio >= 0.24.0 - Async test support
- httpx >= 0.28.0 - HTTP client for testing FastAPI
- ruff >= 0.8.0 - Linting (can be used in CI)

**Frontend:**
- No testing dependencies installed
- Recommended additions:
  - @playwright/test - E2E testing
  - vitest - Unit testing for TypeScript/Svelte
  - @testing-library/svelte - Component testing

## Current State

**Backend:**
- Test infrastructure ready (dependencies installed)
- No test files created yet
- No CI/CD pipeline detected
- Coverage tooling not configured

**Frontend:**
- No test infrastructure
- No test files
- SvelteKit provides `check` command for type checking (not testing)

## Recommended Next Steps

**Backend Testing:**
1. Create `backend/app/tests/conftest.py` with database fixtures
2. Add `backend/app/tests/test_auth.py` for authentication flows
3. Add `backend/app/tests/test_security.py` for password/token functions
4. Configure pytest-cov for coverage reporting
5. Add GitHub Actions workflow for CI

**Frontend Testing:**
1. Install Vitest: `pnpm add -D vitest @testing-library/svelte`
2. Install Playwright: `pnpm add -D @playwright/test`
3. Create test configuration in `vite.config.ts`
4. Add unit tests for utilities in `src/lib/`
5. Add E2E tests for authentication flows

---

*Testing analysis: 2026-01-18*
