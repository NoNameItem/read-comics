# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Read Comics is a full-stack web application for browsing and managing comic data. It scrapes data from ComicVine, stores it in PostgreSQL, and serves it via a REST API to a Nuxt 3 frontend.

**Data flow:** ComicVine API → Scrapy spiders → MongoDB (raw) → Celery tasks → PostgreSQL → DRF API → Nuxt frontend

## Development Commands

### Backend (run from repository root with Docker)

```bash
docker compose -f local.yml up                              # Start all services
docker compose -f local.yml run --rm django pytest          # Run all tests
docker compose -f local.yml run --rm django pytest path/to/test.py::TestClass::test_method  # Run single test
docker compose -f local.yml run --rm django coverage run -m pytest && coverage html  # Test coverage
docker compose -f local.yml run --rm django mypy read_comics  # Type checking

# Linting (inside container)
docker compose -f local.yml run --rm django black read_comics config
docker compose -f local.yml run --rm django isort read_comics config
docker compose -f local.yml run --rm django flake8 read_comics config
```

### Frontend (run from `frontend/` directory)

```bash
pnpm dev          # Dev server on localhost:3000
pnpm build        # Production build
pnpm lint         # ESLint
pnpm lint:fix     # Auto-fix lint issues
pnpm format       # Check Prettier formatting
pnpm format:fix   # Auto-format
pnpm typecheck    # TypeScript checking
```

### Running services

- Django API: http://localhost:8000
- Nuxt frontend: http://localhost:3000
- MailHog (email): http://localhost:8025
- Documentation: http://localhost:7001

## Architecture

### Backend Structure

Django apps are domain-driven under `read_comics/`:
- `characters/`, `issues/`, `volumes/`, `publishers/`, etc. - Comic entity apps
- `core/` - Shared utilities, collectors, base models
- `users/` - Authentication and user management
- `search/` - Search functionality (django-watson)

**Key patterns:**
- `ComicvineSyncModel` - Base class for all comic entities with MongoDB sync
- API endpoints registered in `config/api_router.py` using DRF Extensions router
- Celery task routing configured in `config/celery_app.py`

### Frontend Structure

Nuxt 4 app under `frontend/app/`:
- `pages/` - File-based routing
- `stores/` - Pinia stores (`user.ts` for auth, `breadcrumbs.ts` for navigation)
- `composables/useAxios.js` - Axios instance with JWT interceptor and token refresh
- `middleware/auth.global.ts` - Route protection based on `route.meta.loginRequired`
- `layouts/` - `default.vue` (dashboard with sidebar), `blank.vue` (auth pages)

**Authentication flow:**
1. Login POST to `/api/auth/login/` returns JWT tokens
2. Tokens stored in Pinia with localStorage persistence
3. `useAxios()` adds `Authorization: Bearer {token}` to requests
4. On 401, attempts refresh via `/api/auth/token/refresh/`

## Code Style

### Python
- Black formatter (120 char lines)
- isort for imports
- flake8 for linting
- mypy strict mode with Django stubs

### TypeScript/Vue
- ESLint with Prettier
- Single quotes, no semicolons, 2-space indent
- 100 char line width

## Documentation Requirements

When writing documentation under `docs/`:
1. Follow the style guide in `docs/doc-style.md`
2. Add `# Docs: [[docs/path/to_file.md]]` comment at top of Python modules
3. Endpoint documentation goes in `endpoints.md`, not `viewsets.md`
4. Test documentation: describe fixtures and assertions, not source code
