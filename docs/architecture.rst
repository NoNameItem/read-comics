Architecture Overview
"
    "=====================

"
    "This repository hosts ReadComics.net as a Django backend with a Nuxt 3 frontend. "
    "The backend persists canonical data in PostgreSQL and stores scraped ComicVine payloads in MongoDB. "
    "Background processing runs through Celery with RabbitMQ as the broker, and Redis is used for caching. "
    "Local orchestration relies on docker-compose via `local.yml`.

"
    "Core Services (Docker Compose)
"
    "------------------------------
"
    "- `backend` (container `django`): Django app, server-rendered pages, and REST API.
"
    "- `celeryworker`: Celery worker for ingestion, refresh, and missing-issues jobs.
"
    "- `postgres`, `mongodb`, `redis`, `rabbitmq`, `mailhog`, `flower` provide persistence, cache, broker, email UI, and task monitoring.

"
    "Data Ingestion & Sync
"
    "---------------------
"
    "- Scrapy spiders in `read_comics/spiders/` crawl ComicVine endpoints and write documents into MongoDB collections
"
    "  such as `comicvine_issues` and `comicvine_volumes`.
"
    "- Celery tasks in each domain app (e.g., `read_comics/issues/tasks.py`) pull from MongoDB and sync into Django models.
"
    "- Missing-issues tasks use MongoDB to detect gaps and create `MissingIssue` rows for review in the UI.

"
    "Backend Apps & APIs
"
    "-------------------
"
    "- Domain apps live under `read_comics/` (issues, volumes, characters, concepts, story_arcs, teams, etc.) with their own URLs
"
    "  and templates.
"
    "- REST endpoints are registered in `config/api_router.py` under `/api/` using read-only viewsets, plus profile endpoints
"
    "  like `/api/profile/` and `/api/profile/finished-stats/`.

"
    "Frontend
"
    "--------
"
    "- `frontend/` is a Nuxt 3 app with pages, stores, and components.
"
    "- It consumes Django API endpoints and complements server-rendered pages.

"
    "Observability
"
    "-------------
"
    "- `/metrics/` exposes Prometheus-style metrics for MongoDB, database, and API queue counts.
"
