# Backend Architecture

## Data Flow

```
ComicVine API → Scrapy → MongoDB → Celery Tasks → PostgreSQL → DRF API → Nuxt Frontend
```

## Key directories

- `read_comics/` — domain-specific Django apps (e.g., `issues/`, `spiders/`, `users/`).
- `config/` — settings, routing, Celery entry points, and WSGI/ASGI modules.
- `requirements/` and `pyproject.toml` — dependency manifests.
- `staticfiles/` — collected static assets.

## Settings

- Base settings live under `config/settings/` and change per environment (dev/test/prod).
- Environment variables cover Celery, email, external integrations, and other secrets.
- The Celery app is configured in `config/celery.py` and uses settings modules for runtime values.

## Key Patterns

### ComicvineSyncModel

Base class for all comic entities (`read_comics/utils/models.py`):

- `MONGO_COLLECTION` — MongoDB collection name
- `COMICVINE_INFO_TASK` — Celery sync task
- `FIELDS_MAPPING` — ComicVine → Django field mapping
- `.sync()` — trigger MongoDB → PostgreSQL sync

### API Structure

- `<app>/api/viewsets.py` — DRF ViewSets
- `<app>/api/serializers.py` — DRF Serializers
- `config/api_router.py` — DRF Extensions router
- Auth: JWT (SimpleJWT), session in DEBUG

### Celery Routing

(`config/celery_app.py`):

- `*_update` tasks → `read_comics_spiders` queue
- Missing issues → entity-specific queues
- Default: `read_comics_default`

## API Conventions

### Pagination Response

```json
{
  "count": 1234,
  "next": "...",
  "previous": "...",
  "pages_count": 42,
  "results": [...]
}
```

### Error Response (400 Validation)

```json
{
  "field_name": ["Error message 1", "Error message 2"],
  "other_field": ["Error message"]
}
```

## OpenAPI Schema Generation

Use `drf-spectacular` to generate OpenAPI schema for frontend type generation:

```bash
python manage.py spectacular --file schema.yaml
```
