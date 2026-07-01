# Backend Architecture

## Summary

- [Data Ingestion Pipeline](#data-ingestion-pipeline) — ComicVine → Scrapy → MongoDB → Celery → PostgreSQL
- [Domain-Driven Apps](#domain-driven-apps) — Django apps organized by comic entity
- [Model Hierarchy](#model-hierarchy) — `ComicvineSyncModel` base class and mixins
- [Manager Classes](#manager-classes) — custom managers for queries and sync
- [API Layer](#api-layer) — DRF ViewSets, serializers, and mixins
- [Celery Task Architecture](#celery-task-architecture) — queues and routing

---

## Data Ingestion Pipeline

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

**Spider Types** ([docs](spiders/README.md)):

- `BaseSpider` — common crawling logic
- `FullSpider` — complete entity scrape
- `ImageSpider` — image-only updates
- Entity-specific: `CharactersSpider`, `IssuesSpider`, `VolumesSpider`, etc.

---

## Domain-Driven Apps

Django apps under `read_comics/` organized by comic entity:

| App | Purpose | Documentation |
|-----|---------|---------------|
| `characters/` | Character entities (heroes, villains) | [README](characters/README.md) |
| `issues/` | Individual comic issues | [README](issues/README.md) |
| `volumes/` | Comic series/volumes | [README](volumes/README.md) |
| `publishers/` | Publishing companies | [README](publishers/README.md) |
| `people/` | Creators (writers, artists) | [README](people/README.md) |
| `teams/` | Superhero teams | [README](teams/README.md) |
| `story_arcs/` | Cross-issue storylines | [README](story_arcs/README.md) |
| `concepts/` | Abstract concepts | [README](concepts/README.md) |
| `locations/` | Places | [README](locations/README.md) |
| `objects/` | Items and artifacts | [README](objects/README.md) |
| `powers/` | Superpowers | [README](powers/README.md) |
| `core/` | Shared utilities, collectors | [README](core/README.md) |
| `users/` | Authentication & user management | [README](users/README.md) |
| `search/` | django-watson search integration | [README](search/README.md) |
| `spiders/` | Scrapy spiders for ComicVine | [README](spiders/README.md) |
| `missing_issues/` | Admin tools for gap detection | [README](missing_issues/README.md) |

---

## Model Hierarchy

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

### ComicvineSyncModel

Base class for all comic entities ([docs](utils/models.md)):

**Class Attributes:**

| Attribute | Purpose |
|-----------|---------|
| `MONGO_COLLECTION` | MongoDB collection name |
| `COMICVINE_INFO_TASK` | Celery sync task path |
| `FIELDS_MAPPING` | ComicVine → Django field mapping |

**Fields:**

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

**Key Methods:**

- `.sync()` — trigger MongoDB → PostgreSQL sync

### Model Mixins

Key mixins from [`utils/model_mixins.py`](utils/model_mixins.md):

- `ReadingProgressMixin` — tracks user reading state
- `WatchlistMixin` — watchlist functionality
- `RelatedEntitiesMixin` — cross-entity relationships

---

## Manager Classes

Custom managers from [`utils/model_managers.py`](utils/model_managers.md):

### ComicvineSyncManager

- `get_by_comicvine_id()` — lookup by external ID
- `sync_from_mongo()` — sync single document
- `bulk_sync()` — batch sync operations

### EntityWithCountsManager

- `with_issues_count()` — annotate with issue count
- `with_volumes_count()` — annotate with volume count
- `annotate_reading_progress(user)` — annotate with user's reading progress

---

## API Layer

### ViewSet Hierarchy

```
rest_framework.viewsets.ModelViewSet
    └── BaseComicViewSet (utils/api/viewsets.py)
            ├── CharacterViewSet
            ├── IssueViewSet
            ├── VolumeViewSet
            └── ...
```

### ViewSet Mixins

Mixins from [`utils/api/viewset_*.py`](utils/api/viewsets.md):

| Mixin | Purpose | Endpoints |
|-------|---------|-----------|
| `QuerySetFilterMixin` | Filter by related entities | Query params |
| `QuerySetAnnotationMixin` | Add counts, reading progress | — |
| `CountActionMixin` | Count endpoint | `/count/` |
| `StartWithActionMixin` | Filter by first letter | `/start-with/{letter}/` |
| `WatchlistActionMixin` | Watch/unwatch | `/start-watch/`, `/stop-watch/` |
| `ReadingProgressActionMixin` | Mark read/unread | `/mark-read/`, `/mark-unread/` |
| `TechnicalInfoActionMixin` | Staff technical info | `/technical-info/` |

### Serializer Pattern

Each app has serializers in `<app>/api/serializers.py`:

- `<Entity>ListSerializer` — minimal fields for list views
- `<Entity>DetailSerializer` — full fields for detail views
- `<Entity>SublistSerializer` — for nested lists in tabs

### Routing

Routes registered in `config/api_router.py` using DRF Extensions router:

```python
router = ExtendedSimpleRouter()
router.register("characters", CharacterViewSet)
router.register("issues", IssueViewSet)
# ...
```

### API Conventions

**Pagination Response:**

```json
{
  "count": 1234,
  "next": "https://api/characters/?page=2",
  "previous": null,
  "pages_count": 42,
  "results": [...]
}
```

**Error Response (400 Validation):**

```json
{
  "field_name": ["Error message 1", "Error message 2"],
  "non_field_errors": ["General error"]
}
```

**Authentication:**

- JWT tokens via SimpleJWT
- Session authentication in DEBUG mode
- `Authorization: Bearer {token}` header

---

## Celery Task Architecture

### Queues

| Queue | Purpose |
|-------|---------|
| `read_comics_default` | General tasks |
| `read_comics_spiders` | Spider-triggered syncs (`*_update`) |
| `read_comics_characters` | Heavy character processing |
| `read_comics_issues` | Issue sync, reading progress |
| `read_comics_volumes` | Volume processing |

### Task Routing

Configured in `config/celery_app.py`:

- `*_update` tasks → `read_comics_spiders` queue
- Missing issues tasks → entity-specific queues
- Default: `read_comics_default`

### Common Task Patterns

Entity-specific tasks in `<app>/tasks.py`:

- `<entity>_comicvine_info_task` — sync from ComicVine
- `<entity>_update` — spider-triggered update
- `<entity>_issues_mapping` — map issues to entity

---

## Settings

### Configuration Modules

- `config/settings/base.py` — shared settings
- `config/settings/local.py` — development
- `config/settings/test.py` — testing
- `config/settings/production.py` — production

### Key Environment Variables

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection |
| `MONGO_URL` | MongoDB connection |
| `REDIS_URL` | Redis connection |
| `CELERY_BROKER_URL` | Celery broker (Redis) |
| `COMICVINE_API_KEY` | External API access |
| `SECRET_KEY` | Django secret |

---

## OpenAPI Schema Generation

Use `drf-spectacular` to generate OpenAPI schema for frontend type generation:

```bash
python manage.py spectacular --file schema.yaml
```

Frontend types generated with:

```bash
cd frontend && npm run generate:types
```
