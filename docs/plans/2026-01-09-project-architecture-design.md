# Read Comics — Project Architecture Design

## 1. System Overview

**Read Comics** is a full-stack web application for browsing and managing comic data scraped from ComicVine.

### Core Data Flow

```
ComicVine API → Scrapy Spiders → MongoDB (raw) → Celery Tasks → PostgreSQL → DRF API → Nuxt Frontend
```

### Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 4.x, Django REST Framework, Celery |
| Database | PostgreSQL (primary), MongoDB (raw scrape data) |
| Cache/Queue | Redis |
| Frontend | Nuxt 3, Nuxt UI v4, Pinia, Axios |
| Infrastructure | Docker Compose |

### Key Services (local.yml)

- Django API on `:8000`
- Nuxt frontend on `:3000`
- PostgreSQL, MongoDB, Redis
- Celery workers (default, spiders queues)
- MailHog for email testing

---

## 2. Backend Architecture

### 2.1 Data Ingestion Pipeline

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ComicVine API │───▶│  Scrapy Spider  │───▶│    MongoDB      │
│   (external)    │    │  (read_comics/  │    │  (raw JSON)     │
└─────────────────┘    │   spiders/)     │    └────────┬────────┘
                       └─────────────────┘             │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   DRF API       │◀───│   PostgreSQL    │◀───│  Celery Tasks   │
│   (viewsets)    │    │   (normalized)  │    │  (sync + map)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Spider Types** (`read_comics/spiders/`):

- `BaseSpider` — common crawling logic
- `FullSpider` — complete entity scrape
- `ImageSpider` — image-only updates
- Entity-specific: `CharactersSpider`, `IssuesSpider`, `VolumesSpider`, etc.

### 2.2 Domain-Driven Apps

Django apps under `read_comics/` organized by comic entity:

| App | Purpose |
|-----|---------|
| `characters/` | Character entities (heroes, villains) |
| `issues/` | Individual comic issues |
| `volumes/` | Comic series/volumes |
| `publishers/` | Publishing companies |
| `people/` | Creators (writers, artists) |
| `teams/` | Superhero teams |
| `story_arcs/` | Cross-issue storylines |
| `concepts/`, `locations/`, `objects/`, `powers/` | Related entities |
| `core/` | Shared utilities, collectors, base models |
| `users/` | Authentication & user management |
| `search/` | django-watson search integration |
| `spiders/` | Scrapy spiders for ComicVine |
| `missing_issues/` | Admin tools for gap detection |

### 2.3 Model Hierarchy

```
django.db.Model
    └── ComicvineSyncModel (utils/models.py)
            ├── Character
            ├── Issue
            ├── Volume
            ├── Publisher
            ├── Person
            ├── Team
            ├── StoryArc
            ├── Concept
            ├── Location
            └── Object
```

**ComicvineSyncModel Fields:**

| Field | Type | Purpose |
|-------|------|---------|
| `comicvine_id` | Integer | External ID from ComicVine |
| `comicvine_url` | URL | Link to source |
| `name` | CharField | Entity name |
| `slug` | SlugField | URL-friendly identifier |
| `image` | ImageField | Main image |
| `thumb_url` | URL | Thumbnail from ComicVine |
| `short_description` | Text | Brief description |
| `description` | HTML | Full description |
| `created_dt` / `modified_dt` | DateTime | Timestamps |

**Key Mixins** (`utils/model_mixins.py`):

- `ReadingProgressMixin` — tracks user reading state
- `WatchlistMixin` — watchlist functionality
- `RelatedEntitiesMixin` — cross-entity relationships

### 2.4 Manager Classes

**Custom Managers** (`utils/model_managers.py`):

- `ComicvineSyncManager` — `get_by_comicvine_id()`, `sync_from_mongo()`, `bulk_sync()`
- `EntityWithCountsManager` — `with_issues_count()`, `with_volumes_count()`, `annotate_reading_progress(user)`

### 2.5 API Layer

**ViewSet Hierarchy:**

```
rest_framework.viewsets.ModelViewSet
    └── BaseComicViewSet (utils/api/viewsets.py)
            ├── CharacterViewSet
            ├── IssueViewSet
            ├── VolumeViewSet
            └── ...
```

**ViewSet Mixins** (`utils/api/viewset_*.py`):

- `QuerySetFilterMixin` — filtering by related entities
- `QuerySetAnnotationMixin` — adds counts, reading progress
- `StartWithActionMixin` — `/start-with/{letter}/` endpoint
- `WatchlistActionMixin` — `/watch/`, `/unwatch/` actions
- `ReadingProgressActionMixin` — `/mark-read/`, `/mark-unread/`

**Pagination Response:**

```json
{
  "count": 1234,
  "next": "...",
  "previous": "...",
  "pages_count": 42,
  "results": [...]
}
```

**Error Response (400):**

```json
{
  "field_name": ["Error message 1"],
  "non_field_errors": ["General error"]
}
```

### 2.6 Celery Task Architecture

| Queue | Tasks | Purpose |
|-------|-------|---------|
| `read_comics_default` | General tasks | Default processing |
| `read_comics_spiders` | `*_update`, `*_sync` | Spider-triggered syncs |
| `read_comics_characters` | Character-specific | Heavy character processing |
| `read_comics_issues` | Issue-specific | Issue sync, reading progress |

### 2.7 Search Integration

**django-watson** for full-text search.

**Search Endpoint:** `GET /api/search/?q=batman`

---

## 3. Frontend Architecture

### 3.1 Technology Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| Framework | Nuxt 3 | SSR/SSG Vue.js framework |
| UI Library | Nuxt UI v4 | Component library with dashboard components |
| State | Pinia | Reactive stores with localStorage persistence |
| Data Fetching | Pinia Colada | Query caching with stale-while-revalidate |
| HTTP Client | Axios | API requests with JWT interceptors |
| Styling | UnoCSS | Utility-first CSS |
| Validation | Zod | Schema-based form validation |
| Icons | Iconify (Lucide) | Icon system |
| Date Utils | date-fns | Date formatting |

### 3.2 Directory Structure

```
frontend/app/
├── assets/           # Global CSS, static images
├── components/       # Reusable Vue components (app/, entity/)
├── composables/      # API queries, useAxios, useFormErrors
├── layouts/          # default (dashboard), blank (auth)
├── middleware/       # auth.global.ts - route protection
├── pages/            # File-based routing
├── stores/           # user.ts, breadcrumbs.ts
├── types/api/        # Generated from OpenAPI schema
└── utils/            # Helper functions
```

### 3.3 Authentication Flow

```
Login Page → useUserStore.login() → POST /api/auth/login/
                    ↓
            JWT tokens + user data
                    ↓
            localStorage (persist: true)
                    ↓
            Axios interceptor adds Authorization header
                    ↓
            On 401 → auto-refresh via /api/auth/token/refresh/
```

**Key Components:**

- `useUserStore` — manages tokens, user data, login/logout/refresh actions
- `useAxios` — configured instance with request/response interceptors
- `auth.global.ts` — middleware checks `route.meta.loginRequired`

### 3.4 Route Protection

**Page Meta Flags:**

| Flag | Purpose |
|------|---------|
| `loginRequired` | Redirect to login if not authenticated |
| `staffRequired` | 403 if user is not staff |
| `superuserRequired` | 403 if user is not superuser |

### 3.5 Data Fetching (Pinia Colada)

**Pattern:** Keys Factory + defineQuery/defineMutation

**Query Keys Structure:**

- `['characters']` — all character queries
- `['characters', 'list', params]` — list with filters
- `['characters', 'detail', slug]` — single character

**Caching Strategy:**

| Data Type | staleTime | gcTime |
|-----------|-----------|--------|
| Entity lists | 5 min | 30 min |
| Entity details | 5 min | 30 min |
| Profile / reading progress | 1 min | 30 min |

**Mutations:** Pessimistic updates with cache invalidation on success

### 3.6 Layouts

**Default Layout** (dashboard):

```
┌─────────────────────────────────────────────────────┐
│  Header (user menu, color mode toggle)              │
├──────────┬──────────────────────────────────────────┤
│          │  Breadcrumbs                             │
│  Sidebar │──────────────────────────────────────────│
│  (nav)   │  <slot /> (page content)                 │
└──────────┴──────────────────────────────────────────┘
```

**Blank Layout** (auth pages): Centered content, no navigation chrome

### 3.7 Forms and Validation

- **Schema:** Zod, defined inline per component
- **Component:** UForm from Nuxt UI
- **Server Errors:** `useFormErrors` composable maps 400 response to form field errors

### 3.8 SSR/CSR Strategy

| Route Pattern | Mode | Reason |
|---------------|------|--------|
| `/characters/**`, `/issues/**`, `/volumes/**` | SSR | SEO for public content |
| `/search` | SSR | SEO for search results |
| `/users/**` | CSR | Private user data |
| `/missing-issues/**` | CSR | Staff-only admin pages |

### 3.9 Error Handling

| Error | Handler | User Experience |
|-------|---------|-----------------|
| 401 Unauthorized | Axios interceptor | Redirect to login |
| 403 Forbidden | Axios interceptor | Toast notification |
| 400 Validation | useFormErrors | Inline form errors |
| 404 / 500 | error.vue | Full-page UError component |

---

## 4. Infrastructure

### 4.1 Docker Services (local.yml)

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Compose                            │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│   django    │   nuxt      │  postgres   │   mongo     │  redis  │
│   :8000     │   :3000     │   :5432     │   :27017    │  :6379  │
├─────────────┼─────────────┴─────────────┴─────────────┴─────────┤
│  celerybeat │              celeryworker (multiple queues)        │
├─────────────┼───────────────────────────────────────────────────┤
│   mailhog   │                    docs                            │
│   :8025     │                   :7001                            │
└─────────────┴───────────────────────────────────────────────────┘
```

### 4.2 Services Overview

| Service | Image/Build | Purpose | Port |
|---------|-------------|---------|------|
| django | ./compose/local/django | API server, admin | 8000 |
| nuxt | ./frontend | Frontend dev server | 3000 |
| postgres | postgres:14 | Primary database | 5432 |
| mongo | mongo:6 | Raw scrape data | 27017 |
| redis | redis:7 | Cache, Celery broker | 6379 |
| celeryworker | django image | Background tasks | — |
| celerybeat | django image | Scheduled tasks | — |
| mailhog | mailhog/mailhog | Email testing | 8025 |
| docs | — | MkDocs documentation | 7001 |

### 4.3 Celery Queues

| Queue | Purpose |
|-------|---------|
| `read_comics_default` | General tasks |
| `read_comics_spiders` | Spider-triggered syncs (`*_update`) |
| `read_comics_characters` | Heavy character processing |
| `read_comics_issues` | Issue sync, reading progress |
| `read_comics_volumes` | Volume processing |

### 4.4 Environment Configuration

**Django Settings Modules:**

- `config.settings.local` — development
- `config.settings.test` — testing
- `config.settings.production` — production

**Key Environment Variables:**

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection |
| `MONGO_URL` | MongoDB connection |
| `REDIS_URL` | Redis connection |
| `CELERY_BROKER_URL` | Celery broker (Redis) |
| `COMICVINE_API_KEY` | External API access |
| `SECRET_KEY` | Django secret |

**Frontend Environment:**

- `.env.development`: `NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000/api`
- `.env.production`: `NUXT_PUBLIC_API_BASE=https://readcomics.net/api`

### 4.5 Data Storage

| Storage | Technology | Data |
|---------|------------|------|
| Primary DB | PostgreSQL | Normalized entities, users, reading progress |
| Raw Data | MongoDB | Scraped JSON from ComicVine |
| Cache | Redis | Session, query cache, Celery broker |
| Static Files | S3/DO Spaces | Images, collected static |
| Media | S3/DO Spaces | User uploads, comic images |

### 4.6 Development Workflow

```bash
# Start all services
docker compose -f local.yml up

# Run tests
docker compose -f local.yml run --rm django pytest

# Run linters
docker compose -f local.yml run --rm django black read_comics config
docker compose -f local.yml run --rm django isort read_comics config
docker compose -f local.yml run --rm django flake8 read_comics config

# Type checking
docker compose -f local.yml run --rm django mypy read_comics

# Frontend (separate terminal)
cd frontend && pnpm dev
```

### 4.7 Production Deployment

| Component | Deployment |
|-----------|------------|
| Django | Gunicorn behind Nginx/Traefik |
| Nuxt | Node.js SSR or static hosting |
| Database | Managed PostgreSQL |
| MongoDB | Managed MongoDB Atlas or self-hosted |
| Redis | Managed Redis |
| Static/Media | S3-compatible storage (DO Spaces) |
| Workers | Celery on separate instances |

---

## 5. Current State

The project is migrating from a legacy frontend (`frontend_old/`) to Nuxt UI v4 (`frontend/`). Recent work includes:

- Login page migration
- Registration page migration
- Logout functionality
- High-level architecture planning
