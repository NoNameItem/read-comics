---
date: 2025-12-28T12:00:00+03:00
researcher: Claude
topic: "High-Level Project Architecture"
tags: [research, architecture, backend, frontend, infrastructure, data-flow]
status: complete
---

# Research: High-Level Project Architecture

## Research Question
Исследовать верхнеуровневую архитектуру проекта ReadComics.net

## Summary

ReadComics.net - full-stack веб-приложение для работы с данными о комиксах. Архитектура состоит из:

- **Backend**: Django 5.2.9 + Django REST Framework с Celery для фоновых задач
- **Frontend**: Nuxt 4.x (Vue 3) с Nuxt UI компонентами
- **Data Pipeline**: Scrapy spiders → MongoDB (кэш) → Celery tasks → PostgreSQL
- **Infrastructure**: Docker Compose с PostgreSQL, MongoDB, Redis, RabbitMQ

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            ComicVine API                                     │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │        Scrapy Spiders         │
                    │   (11 entity-specific + Full)  │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │          MongoDB              │
                    │   (Raw data cache layer)      │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │       Celery + RabbitMQ       │
                    │   (Background sync tasks)     │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │     Django + PostgreSQL       │
                    │   (Application data)          │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │    Nuxt 3 Frontend (SPA)      │
                    │   (REST API consumption)      │
                    └───────────────────────────────┘
```

---

## Detailed Findings

### 1. Backend Architecture (Django)

#### Django Apps Structure (`read_comics/`)

| App | Purpose |
|-----|---------|
| `issues/` | Individual comic issues - primary content entity |
| `volumes/` | Volume entities (comic series) |
| `publishers/` | Comic book publishers (Marvel, DC, etc.) |
| `characters/` | Characters (superheroes, villains) |
| `teams/` | Team entities (Avengers, X-Men) |
| `people/` | Comic creators (writers, artists) |
| `concepts/` | Comic concepts (time travel, alternate universes) |
| `locations/` | Geographic/fictional locations |
| `objects/` | Notable objects (Mjolnir, Infinity Gauntlet) |
| `story_arcs/` | Story arcs spanning multiple issues |
| `powers/` | Superpowers and abilities |
| `missing_issues/` | Gap tracking and API queue management |
| `users/` | User authentication and profiles |
| `spiders/` | Scrapy configuration and ComicVine spiders |
| `search/` | Full-text search with django-watson |
| `utils/` | Shared utilities, base models, mixins |
| `core/` | Core application functionality |

#### Key Base Classes

**ComicvineSyncModel** (`read_comics/utils/models.py:37-572`)
- Abstract base model for all entities synced from ComicVine API
- Manages MongoDB caching, field mapping, API synchronization
- Class attributes: `MONGO_COLLECTION`, `COMICVINE_INFO_TASK`, `COMICVINE_API_URL`
- Key methods: `fill_from_comicvine()`, `process_document()`, `get_document_from_api()`

**Model Mixins** (`read_comics/utils/model_mixins.py`)
- `ImageMixin` - Image URL properties (full_size, thumb, avatar)
- `DownloadSizeMixin` - Total download size calculation
- `AliasesListMixin` - Parse aliases into list

**ViewSet Mixins** (`read_comics/utils/api/viewset_queryset_mixins.py`)
- `OnlyWithIssuesQuerySetMixin` - Filter entities with issues
- `IssuesCountQuerySetMixin` / `VolumesCountQuerySetMixin` - Annotate counts
- `FinishedQuerySetMixin` - Reading progress annotations
- `CountActionMixin` - `/count/` endpoint
- `TechnicalInfoActionMixin` - `/technical-info/` for superusers

#### API Structure

- Router: `config/api_router.py` - DRF Extensions `ExtendedDefaultRouter`
- Pattern: Slug-based lookups, separate list/detail serializers
- Authentication: JWT (SimpleJWT) + session auth in DEBUG mode
- Pagination: 48 items per page (`read_comics/utils/api/pagination.py`)

---

### 2. Frontend Architecture (Nuxt 3)

#### Directory Structure (`frontend/app/`)

```
app/
├── pages/           # File-based routing
├── components/      # Vue components
├── layouts/         # default.vue, blank.vue
├── stores/          # Pinia state (user.ts, breadcrumbs.js)
├── composables/     # useAxios.js, useDashboard.ts
├── types/           # TypeScript definitions
└── utils/           # Utility functions
```

#### Tech Stack

- **Framework**: Nuxt 4.x with Vue 3 Composition API
- **UI**: Nuxt UI v4 (Dashboard components)
- **State**: Pinia with localStorage persistence
- **HTTP**: Axios with JWT interceptors
- **Charts**: @unovis/vue
- **Icons**: Lucide, Simple Icons

#### Key Stores

**User Store** (`frontend/app/stores/user.ts`)
- JWT authentication (access/refresh tokens)
- User profile (username, email, gender, images)
- Actions: `login()`, `register()`, `refreshTokens()`, `logout()`

**Breadcrumbs Store** (`frontend/app/stores/breadcrumbs.js`)
- Page title and breadcrumb navigation

#### Layouts

- `default.vue` - Dashboard with sidebar navigation
- `blank.vue` - Minimal layout for auth pages

---

### 3. Infrastructure (Docker)

#### Services (`local.yml`)

| Service | Image | Port | Role |
|---------|-------|------|------|
| backend | Custom Django | 8000 | REST API |
| postgres | postgres:18.1 | 5432 | Application database |
| mongodb | mongo:8.0.4 | 27017 | Scraped data cache |
| redis | redis:6 | - | Cache backend |
| rabbitmq | rabbitmq:4-management | 5672, 15672 | Message broker |
| celeryworker | Custom | - | Background tasks |
| flower | Custom | 5555 | Celery monitoring |
| mailhog | mailhog:v1.0.0 | 8026 | Email testing |
| docs | Custom | 7001 | Sphinx docs |

#### Environment Configuration

```
.envs/.local/
├── .django          # Django settings, Redis URL, DO Spaces
├── .django_unsafe   # Sensitive secrets, API keys
├── .postgres        # PostgreSQL connection
├── .mongo           # MongoDB credentials
└── .rabbit_unsafe   # RabbitMQ credentials
```

#### Production Differences

- Web server: Gunicorn (port 5000) vs Django runserver
- Reverse proxy: Traefik with Let's Encrypt SSL
- Email: Mailgun vs MailHog
- Storage: DigitalOcean Spaces vs local
- JWT: 5min/30d vs 15min/60d tokens

---

### 4. Data Flow Pipeline

#### Scrapy Spiders (`read_comics/spiders/spiders/`)

**Spider Hierarchy:**
- `BaseSpider` - Abstract base with pagination, rate limiting
- Entity spiders: `CharactersSpider`, `IssuesSpider`, `VolumesSpider`, etc.
- `FullSpider` - Crawls all 11 endpoints simultaneously

**Key Features:**
- API key rotation for rate limit handling
- Incremental mode via `date_last_updated` filter
- Two-phase crawling: list (priority 5) → detail (priority 1)
- Documents tagged with `crawl_source: "list"|"detail"` and `crawl_date`

#### MongoDB Collections

`comicvine_<entity>` - One collection per entity type (characters, issues, volumes, etc.)

#### Celery Task Organization (`config/celery_app.py`)

**Queue Routing:**
- `read_comics_spiders` - Web scraping tasks (`*_update`)
- `read_comics_<entity>` - Entity-specific sync tasks
- `read_comics_default` - Fallback queue

**Task Types:**
1. **Spider Update Tasks** - Run scrapy spiders
2. **ComicvineInfoTask** - Sync MongoDB → PostgreSQL
3. **RefreshTask** - Batch sync for outdated records
4. **MissingIssuesTask** - Find gaps in collection
5. **SpaceTask** - S3 file processing

#### Sync Process

```
1. Scrapy crawls ComicVine API → stores in MongoDB
2. Celery task triggers for entity
3. ComicvineSyncModel.fill_from_comicvine() called
4. Document fetched from MongoDB (or API fallback)
5. Field mapping applied via FIELDS_MAPPING
6. M2M relationships created on-demand
7. PostgreSQL model saved with comicvine_status=MATCHED
```

---

### 5. Development Tooling

#### Python Stack

| Tool | Purpose |
|------|---------|
| Black (120 chars) | Code formatting |
| isort | Import sorting |
| flake8 + plugins | Linting |
| pylint + pylint-django | Advanced linting |
| mypy | Type checking |
| pytest + coverage | Testing |
| pre-commit | Git hooks |

#### Frontend Stack

| Tool | Purpose |
|------|---------|
| ESLint | Linting |
| Prettier | Formatting |
| TypeScript + vue-tsc | Type checking |
| pnpm | Package manager |

#### CI/CD (GitHub Actions)

```
Push/PR → qa.yml → linters.yml (flake8, pylint, mypy, prettier, eslint)
                 → unit_tests.yml (pytest + coverage)
                 → publish_reports.yml
```

---

## Code References

### Backend
- `config/api_router.py` - API route registration
- `config/celery_app.py:40-68` - Task queue routing
- `config/settings/base.py` - Base Django settings
- `read_comics/utils/models.py:37-572` - ComicvineSyncModel
- `read_comics/utils/model_managers.py` - ComicvineSyncManager
- `read_comics/utils/api/viewset_queryset_mixins.py` - ViewSet mixins
- `read_comics/spiders/spiders/base_spider.py` - BaseSpider
- `read_comics/spiders/pipelines.py` - MongoDB pipeline

### Frontend
- `frontend/nuxt.config.ts` - Nuxt configuration
- `frontend/app/layouts/default.vue` - Main layout
- `frontend/app/stores/user.ts` - Authentication store
- `frontend/app/composables/useAxios.js` - HTTP client

### Infrastructure
- `local.yml` - Docker Compose (development)
- `compose/production/traefik/traefik.yml` - Production proxy
- `compose/local/django/Dockerfile` - Django container

---

## Architecture Insights

### Design Patterns

1. **Repository Pattern** - ComicvineSyncModel acts as repository for ComicVine data
2. **Producer-Consumer** - Scrapy produces to MongoDB, Celery consumes to PostgreSQL
3. **Mixins Composition** - ViewSets and models composed from multiple mixins
4. **Queue-based Routing** - Workload distributed across specialized queues
5. **Cache-aside** - MongoDB as cache layer with PostgreSQL as source of truth

### Conventions

1. **Slug-based URLs** - All entities use slug instead of pk in API
2. **Separate serializers** - List and detail serializers for performance
3. **Read-only API** - All ViewSets extend `ReadOnlyModelViewSet`
4. **Docs comments** - Python modules reference docs with `# Docs: [[docs/path]]`
5. **Conventional Commits** - `feat`, `fix`, `refactor` with app scopes

### Key Decisions

1. **Dual Database** - MongoDB for raw API cache, PostgreSQL for application data
2. **Delayed Sync** - Entities created immediately, synced asynchronously via Celery
3. **Rate Limiting** - Multiple levels (spider, middleware, model queue)
4. **JWT + Persistence** - Tokens stored in localStorage with auto-refresh

---

## Migration Status (DRF + Nuxt)

### Overview

Проект находится в процессе миграции с Django views на REST API + Nuxt frontend.

**История миграции:**
1. `frontend_old/` - первая итерация с проприетарной библиотекой компонентов
2. `frontend/` - текущая миграция на Nuxt UI v4
3. После завершения будут удалены: `frontend_old/`, Django views/templates

**Источник:** `DRF_MIGRATION_URL_MAP.md` (captured 2025-12-20)

### API Endpoints Status

| Status | Description | Count |
|--------|-------------|-------|
| **OK** | Endpoint ready | ~20 |
| **NEEDS WORK** | Need detail serializer | ~7 |
| **NOT READY** | No serializer | 1 |
| **PLAN** | Not implemented | ~150+ |

### Entity-wise Status

| Entity | List | Detail | Nested/Actions |
|--------|------|--------|----------------|
| Characters | OK | OK | PLAN (issues, volumes, enemies, friends, teams, authors) |
| Concepts | OK | OK | PLAN (issues, volumes) |
| Issues | OK | OK | PLAN (characters, concepts, locations, authors, etc.) |
| Locations | OK | OK | PLAN (issues, volumes) |
| Objects | OK | NEEDS WORK | PLAN + slug lookup pending |
| People | OK | NEEDS WORK | PLAN + slug lookup pending |
| Publishers | OK | NEEDS WORK | PLAN + slug lookup pending |
| Story Arcs | OK | NEEDS WORK | PLAN + slug lookup pending |
| Teams | OK | NEEDS WORK | PLAN + slug lookup pending |
| Volumes | OK | NEEDS WORK | PLAN + slug lookup pending |
| Missing Issues | NOT READY | - | PLAN |
| Search | - | - | PLAN |

### Key Pending Work

1. **Detail Serializers** - Objects, People, Publishers, Story Arcs, Teams, Volumes
2. **Slug Lookup** - Several entities still use `pk` instead of `slug`
3. **Nested Endpoints** - `/<entity>/<slug>/issues/`, `/volumes/`, etc.
4. **Actions** - `start-watch`, `stop-watch`, `mark-read`, `mark-finished`
5. **Search** - `/search/` and `/search/ajax/`
6. **Missing Issues** - Full missing issues management API

### Celery Beat Schedule

Schedule закомментирован намеренно - настройки управляются через django-admin, чтобы не перезатирать при обновлении кода.

### Production Deployment

- **Способ**: Ручной деплой через Docker Compose на частный сервер
- **Конфигурация**: `deploy/` директория
- ~~Yandex Cloud~~ - больше не используется

---

## Open Questions

Все вопросы закрыты.
