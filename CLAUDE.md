# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Read Comics is a web application for exploring and managing comic data. Django REST Framework backend + Nuxt 4 frontend, Docker-based development, ComicVine API integration.

**Documentation:** `docs/backend/README.md`, `docs/backend/architecture.md`, `docs/frontend/README.md`

## Instructions for Claude

- Before modifying files, read the corresponding documentation in `docs/` (e.g., `docs/backend/characters/` before changing `read_comics/characters/`)

## Development Commands

### Backend (Docker-based)

```bash
docker compose -f local.yml up                    # Start all services
docker compose -f local.yml run --rm backend pytest  # Run tests
docker compose -f local.yml run --rm backend pytest path/to/test.py::TestClass::test_method  # Single test
docker compose -f local.yml run --rm backend mypy read_comics   # Type check
docker compose -f local.yml run --rm backend flake8             # Lint
docker compose -f local.yml run --rm backend python manage.py migrate
docker compose -f local.yml run --rm backend python manage.py createsuperuser
```

### Frontend (`frontend/` directory)

```bash
pnpm dev          # Dev server (localhost:3000)
pnpm build        # Production build
pnpm lint:fix     # Fix ESLint issues
pnpm format:fix   # Fix Prettier issues
pnpm typecheck    # TypeScript check
```

## Architecture

### Backend
- **`config/`** — settings (`base.py`, `local.py`, `production.py`), `api_router.py`, `celery_app.py`
- **`read_comics/`** — Django apps (users, characters, issues, volumes, etc.), each with `api/viewsets.py`, `api/serializers.py`, `models.py`, `tests/`
- **`read_comics/utils/`** — shared utilities, `ComicvineSyncModel` base class

### Frontend (`frontend/app/`)
- **`pages/`** — file-based routing
- **`stores/`** — Pinia (`user.ts`, `breadcrumbs.ts`)
- **`composables/`** — `useAxios.js` (JWT interceptors)
- **`layouts/`** — `default.vue` (dashboard), `blank.vue` (auth)

### Data Flow
ComicVine API → Scrapy → MongoDB → Celery → PostgreSQL → Django REST API → Nuxt frontend

### Databases
- **PostgreSQL** — app data, users
- **MongoDB** — scraped ComicVine data
- **Redis** — cache, Celery broker

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

## Testing

See `docs/testing.md` for comprehensive guide.

**Structure:** `<app>/tests/` — `conftest.py`, `factories.py`, `test_drf_urls.py`, `test_e2e.py`

**Key concepts:**
- **Factories** (Factory Boy): `VolumeFactory(add_issues=3)` — create test data
- **Fixtures**: `api_client`, `authenticated_api_client`, `user`, `staff`, `superuser`
- **URL tests**: verify `reverse()` ↔ `resolve()` mapping
- **E2E tests**: full API workflow (request → response validation)

**Fixtures pattern:**
- `volume_no_issues` / `volume_with_issues` — single objects
- `volumes_no_issues` / `volumes_with_issues` — batches
- `finished_volume(user)` / `finished_volumes(user)` — user-specific state

## Common Tasks

### Add API endpoint
1. `read_comics/<app>/api/viewsets.py` — ViewSet
2. `read_comics/<app>/api/serializers.py` — Serializer
3. `config/api_router.py` — register route

### Add frontend page
1. `frontend/app/pages/<path>.vue`
2. `definePageMeta({ layout: 'blank', loginRequired: true })`

## Naming Conventions

### Backend
- ViewSet: `CharacterViewSet` → route `characters`
- Serializer: `CharacterDetailSerializer`, `CharactersListSerializer`
- URL lookup: `slug` (not `id`)

### Frontend
- Components: PascalCase (`UserMenu.vue`)
- Stores: `useUserStore`
- Composables: `useAxios`

## Reference Files (use as templates)

### Backend
- ViewSet: `read_comics/characters/api/viewsets.py`
- Serializer: `read_comics/characters/api/serializers.py`
- Tests: `read_comics/characters/tests/`
- Fixtures: `read_comics/conftest.py`

### Frontend
- Store: `frontend/app/stores/user.ts`
- Composable: `frontend/app/composables/useAxios.js`
- Page: `frontend/app/pages/users/login.vue`

## Key Backend Utilities

See `docs/backend/utils/` for details.

**ViewSet Mixins** (`read_comics/utils/api/viewsets.py`):
- `CountActionMixin` — `GET /count/`
- `TechnicalInfoActionMixin` — `GET /<slug>/technical-info/`
- `OnlyWithIssuesQuerySetMixin`, `IssuesCountQuerySetMixin`, `FinishedQuerySetMixin`, etc.

**ComicvineSyncModel** (`read_comics/utils/models.py`):
- Base model for ComicVine entities
- `MONGO_COLLECTION`, `FIELD_MAPPING`, `fill_from_comicvine()`

## Frontend Patterns

See `docs/frontend/architecture.md` for details.

**Auth:** JWT tokens in `useUserStore`, axios interceptor refreshes on 401
**Data fetching:** Pinia Colada with keys factory pattern
**Route protection:** `definePageMeta({ loginRequired: true })`
**Error handling:** 401→login redirect, 400→form errors, 404/500→error.vue

## Query Parameters

- `?show-all=yes` — include entities with zero issues
- `?hide-finished=yes` — hide completed (authenticated)
- `?ordering=name` / `?ordering=-issues_count`

## Environment

**Backend:** `.envs/.local/` (`.django`, `.postgres`, `.mongo`)
**Frontend:** `NUXT_PUBLIC_API_BASE` (default `http://127.0.0.1:8000/api`)

## Docker Services

| Service | Port | Purpose |
|---------|------|---------|
| backend | 8000 | Django API |
| postgres | 5432 | Database |
| mongodb | 27017 | Scraped data |
| redis | 6379 | Cache/broker |
| mailhog | 8026 | Email testing |
| celeryworker | - | Async tasks |
