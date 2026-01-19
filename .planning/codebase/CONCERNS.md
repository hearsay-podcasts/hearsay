# Codebase Concerns

**Analysis Date:** 2026-01-18

## Tech Debt

**SECRET_KEY Auto-Generation in Config:**
- Issue: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/core/config.py` line 36 generates a new SECRET_KEY on startup using `secrets.token_urlsafe(32)` if not set via environment variable. This causes all existing JWT tokens to become invalid after each restart.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/core/config.py`
- Impact: Users are logged out every time the server restarts in development. In production, this would invalidate all sessions on each deployment/restart.
- Fix approach: Remove the default value and make SECRET_KEY required from environment variables. Add validation to fail fast if not set.

**Cookie Parsing with Regex:**
- Issue: Frontend uses regex to parse Set-Cookie headers in `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/routes/login/+page.server.ts` line 38 and `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/routes/signup/+page.server.ts` line 47. This is fragile and doesn't handle edge cases properly.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/routes/login/+page.server.ts`, `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/routes/signup/+page.server.ts`
- Impact: Cookie extraction could fail silently if FastAPI changes cookie format or adds additional attributes.
- Fix approach: Use a proper cookie parsing library or let SvelteKit handle the cookie forwarding automatically. Consider using fetch with credentials: 'include' instead of manual cookie extraction.

**Frontend Makes Redundant API Call on Every Request:**
- Issue: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/hooks.server.ts` calls `/auth/me` endpoint on every single page load to verify the token, even for public pages.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/hooks.server.ts`
- Impact: Doubles the number of requests (every page load triggers an auth check). Increases latency and backend load. Unnecessary for public routes like login/signup.
- Fix approach: Add route protection logic to only call `/auth/me` for protected routes. Consider validating JWT locally without API call, or cache user data in session.

**No Database Connection Pooling Configuration:**
- Issue: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/core/db.py` creates SQLAlchemy engine without explicit pool size limits or timeout settings.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/core/db.py`
- Impact: Under load, could exhaust database connections or create too many idle connections.
- Fix approach: Add pool_size, max_overflow, and pool_timeout parameters to create_engine call.

**Empty init_db Function:**
- Issue: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/core/db.py` has an empty `init_db()` function that does nothing but has a docstring suggesting it should initialize data.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/core/db.py`
- Impact: Dead code that could confuse developers. Not actually called anywhere.
- Fix approach: Either implement initial data seeding logic or remove the function entirely.

## Known Bugs

**Password Timing Attack Vulnerability:**
- Symptoms: In `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/crud.py` line 28-33, the authenticate function returns early if user doesn't exist vs password verification fails, creating different response times.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/crud.py`
- Trigger: Attempt login with existing vs non-existing email addresses and measure response times
- Workaround: None currently implemented
- Fix: Always call verify_password even if user doesn't exist (with a dummy hash) to ensure constant-time responses.

**Silent Cookie Failure on Login/Signup:**
- Symptoms: If cookie parsing fails in login/signup flows, the user is redirected to dashboard but without authentication cookie, resulting in immediate redirect back to login.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/routes/login/+page.server.ts`, `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/routes/signup/+page.server.ts`
- Trigger: Backend sends malformed Set-Cookie header or changes cookie format
- Workaround: None - results in redirect loop
- Fix: Add validation to ensure cookie was successfully set before redirecting. Log warning if cookie extraction fails.

## Security Considerations

**.env File Committed to Repository:**
- Risk: Root `.env` file at `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/.env` contains actual SECRET_KEY and is in repository. While .gitignore excludes .env files, this one appears to have been committed.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/.env`
- Current mitigation: File is marked for local environment
- Recommendations: Verify this file is not in git history. If committed, rotate the SECRET_KEY immediately. Use .env.example as template only.

**Default Database Credentials:**
- Risk: `docker-compose.yml` and `.env` use default postgres/postgres credentials.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/docker-compose.yml`, `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/.env`
- Current mitigation: Warning in config.py for non-local environments
- Recommendations: Generate strong random passwords for all deployments. Never use defaults in staging/production.

**No Rate Limiting:**
- Risk: Auth endpoints lack rate limiting, allowing brute force attacks on user passwords.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/api/routes/auth.py`
- Current mitigation: None
- Recommendations: Add rate limiting middleware (e.g., slowapi) to limit login attempts per IP. Implement account lockout after N failed attempts.

**JWT Algorithm Not Validated:**
- Risk: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/api/deps.py` line 40-41 uses jwt.decode with single algorithm but doesn't explicitly prevent algorithm confusion attacks.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/api/deps.py`
- Current mitigation: Algorithm specified as list `[security.ALGORITHM]`
- Recommendations: Current implementation is acceptable, but ensure ALGORITHM constant is never changed to 'none' or weak algorithms.

**CORS Allows All Methods and Headers:**
- Risk: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/main.py` lines 17-18 allow all methods and headers via `["*"]` wildcards.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/main.py`
- Current mitigation: Origins are restricted to specific frontend hosts
- Recommendations: Limit allow_methods to actually used methods (GET, POST, OPTIONS). Limit allow_headers to necessary headers (Content-Type, Authorization).

**No CSRF Protection:**
- Risk: Using httpOnly cookies without CSRF tokens makes the app vulnerable to CSRF attacks if XSS vulnerability exists.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/api/routes/auth.py`
- Current mitigation: SameSite=lax provides some protection
- Recommendations: Consider adding CSRF token validation for state-changing operations, or switch to SameSite=strict for stronger protection.

## Performance Bottlenecks

**Authentication Check on Every Request:**
- Problem: Every page load calls `/auth/me` endpoint even for unauthenticated users and public pages.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/hooks.server.ts`
- Cause: Hook runs unconditionally for all requests
- Improvement path: Cache user data in server-side session, verify JWT locally instead of API call, or skip auth check for public routes.

**Bcrypt Password Hashing:**
- Problem: While secure, bcrypt is CPU-intensive and can become bottleneck during signup/login under high load.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/core/security.py`
- Cause: Synchronous bcrypt operations block event loop
- Improvement path: Consider using argon2 (more modern) or run bcrypt operations in thread pool executor to avoid blocking.

**No Database Indexes Beyond Primary Key:**
- Problem: User lookups by email in `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/crud.py` line 18 rely on email index, but no verification that index exists after migrations.
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/models.py`
- Cause: SQLModel Field definition has `index=True` but should verify in database
- Improvement path: Check actual database indexes. Add composite indexes if needed for common query patterns.

## Fragile Areas

**Cookie Configuration Duplication:**
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/api/routes/auth.py`, `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/lib/server/config.ts`
- Why fragile: Cookie configuration (maxAge, secure, sameSite, path) duplicated between backend and frontend. Changes in one location won't automatically update the other.
- Safe modification: Always update both files simultaneously. Consider moving to shared config or environment variables.
- Test coverage: No tests for cookie configuration consistency

**Database Migration Path:**
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/alembic/env.py`, `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/alembic/versions/`
- Why fragile: Only one migration exists (initial user table). No rollback testing. Adding models requires manual import in env.py line 10.
- Safe modification: Always test migrations with downgrade before applying to production. Update env.py imports whenever adding new models.
- Test coverage: No automated migration testing

**Error Handling in Frontend:**
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/routes/login/+page.server.ts`, `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/routes/signup/+page.server.ts`, `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/routes/logout/+page.server.ts`, `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/hooks.server.ts`
- Why fragile: All error handling uses generic console.error with no structured logging or error tracking. Network failures result in generic "unexpected error" messages.
- Safe modification: Add proper error types and user-friendly messages. Implement error tracking service.
- Test coverage: No error handling tests

## Scaling Limits

**Single Database Instance:**
- Current capacity: All database operations go through single PostgreSQL container
- Limit: No read replicas, connection pooling not configured
- Scaling path: Add read replicas for query distribution, implement connection pooling with PgBouncer, consider sharding strategy for multi-tenancy

**Synchronous Request Handling:**
- Current capacity: FastAPI uses async but database operations are synchronous (SQLModel/SQLAlchemy)
- Limit: Database operations block async event loop
- Scaling path: Use async database driver (asyncpg instead of psycopg), or run blocking operations in thread pool

**Frontend SSR for Every Request:**
- Current capacity: SvelteKit server-side renders every page, including auth checks
- Limit: Server CPU becomes bottleneck under high traffic
- Scaling path: Add caching layer (Redis), implement static generation for public pages, use CDN for assets

## Dependencies at Risk

**SQLModel Early Stage:**
- Risk: SQLModel is version 0.0.22, indicating pre-1.0 unstable API
- Impact: Breaking changes possible in future updates
- Migration plan: Stay updated with SQLModel releases, or migrate to pure SQLAlchemy 2.x with Pydantic separately

**Svelte 5 Rapid Evolution:**
- Risk: Svelte 5 with runes is relatively new (version 5.45.6), ecosystem still catching up
- Impact: Third-party libraries may not support runes syntax yet
- Migration plan: Current code uses modern patterns, but be prepared for component library compatibility issues

## Missing Critical Features

**No Logging Infrastructure:**
- Problem: Only console.error statements exist. No structured logging, no log aggregation, no production logging strategy.
- Blocks: Debugging production issues, monitoring system health, audit trails
- Priority: High - Essential for production deployment

**No Test Suite:**
- Problem: Zero tests found in codebase. No unit tests, integration tests, or E2E tests.
- Blocks: Safe refactoring, confident deployments, regression prevention
- Priority: High - Critical before production

**No Email Verification:**
- Problem: User signup doesn't verify email addresses. Anyone can claim any email.
- Blocks: Secure user authentication, password reset functionality
- Priority: Medium - Required for production but workaround exists (manual verification)

**No Password Reset Flow:**
- Problem: No way for users to reset forgotten passwords.
- Blocks: User account recovery, production readiness
- Priority: Medium - Users will lock themselves out

**No API Documentation Beyond OpenAPI:**
- Problem: No architecture docs, no API usage examples, no onboarding guide beyond README
- Blocks: Team scaling, contributor onboarding
- Priority: Low - Can be added incrementally

**No Monitoring or Observability:**
- Problem: No health metrics, no performance monitoring, no error tracking service integration
- Blocks: Understanding production behavior, detecting outages, debugging issues
- Priority: High - Essential before production

## Test Coverage Gaps

**Authentication Flow:**
- What's not tested: Login, signup, logout, token validation, cookie handling
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/api/routes/auth.py`, `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/crud.py`, `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/routes/login/+page.server.ts`, `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/routes/signup/+page.server.ts`
- Risk: Security vulnerabilities, authentication bypass, cookie issues could go undetected
- Priority: High

**Database Models and CRUD:**
- What's not tested: User model validation, email uniqueness, password hashing, CRUD operations
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/models.py`, `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/crud.py`
- Risk: Data corruption, constraint violations, authentication failures
- Priority: High

**Frontend Form Validation:**
- What's not tested: Email format validation, password length requirements, error message display
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/routes/login/+page.svelte`, `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/web/src/routes/signup/+page.svelte`
- Risk: Poor user experience, invalid data submission
- Priority: Medium

**CORS Configuration:**
- What's not tested: Cross-origin requests, cookie handling across origins, preflight requests
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/main.py`
- Risk: Frontend-backend communication failures in production
- Priority: Medium

**Database Migration Rollback:**
- What's not tested: Migration downgrade paths, data preservation during rollback
- Files: `C:/Users/Samuel/Projects/hearsay-podcasts/hearsay/backend/app/alembic/versions/6a85b748a5ff_create_user_table.py`
- Risk: Cannot safely rollback deployments, potential data loss
- Priority: Medium

---

*Concerns audit: 2026-01-18*
