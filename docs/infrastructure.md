# Infrastructure

## Summary

- [Docker Services](#docker-services) — local development stack
- [Services Overview](#services-overview) — ports and purposes
- [Celery Queues](#celery-queues) — background task routing
- [Environment Configuration](#environment-configuration) — settings and variables
- [Data Storage](#data-storage) — databases and file storage
- [Development Workflow](#development-workflow) — common commands
- [Production Deployment](#production-deployment) — deployment architecture

---

## Docker Services

Docker Compose stack for local development (`local.yml`):

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Compose                           │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│   backend   │  postgres   │  mongodb    │   redis     │rabbitmq │
│   :8000     │   :5432     │   :27017    │             │  :5672  │
├─────────────┼─────────────┴─────────────┴─────────────┴─────────┤
│   flower    │              celeryworker                         │
│   :5555     │                                                   │
├─────────────┼───────────────────────────────────────────────────┤
│   mailhog   │                    docs                           │
│   :8026     │                   :7001                           │
└─────────────┴───────────────────────────────────────────────────┘
```

**Note:** Frontend runs separately via `pnpm dev` in `frontend/` directory.

---

## Services Overview

| Service | Image | Purpose | Port |
|---------|-------|---------|------|
| backend | `read_comics_local_django` | Django API server | 8000 |
| postgres | `postgres:18.1` | Primary database | 5432 |
| mongodb | `mongo:8.0.4` | Raw scrape data | 27017 |
| redis | `redis:6` | Cache | — |
| rabbitmq | `rabbitmq:4-management` | Celery broker | 5672, 15672 |
| celeryworker | backend image | Background tasks | — |
| flower | backend image | Celery monitoring | 5555 |
| mailhog | `mailhog/mailhog:v1.0.0` | Email testing | 8026 |
| docs | `read_comics_local_docs` | Documentation server | 7001 |

---

## Celery Queues

| Queue | Purpose |
|-------|---------|
| `read_comics_default` | General tasks |
| `read_comics_spiders` | Spider-triggered syncs (`*_update`) |
| `read_comics_characters` | Heavy character processing |
| `read_comics_issues` | Issue sync, reading progress |
| `read_comics_volumes` | Volume processing |

Task routing configured in `config/celery_app.py`.

---

## Environment Configuration

### Django Settings Modules

| Module | Environment |
|--------|-------------|
| `config.settings.base` | Shared settings |
| `config.settings.local` | Development |
| `config.settings.test` | Testing |
| `config.settings.production` | Production |

### Key Environment Variables

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string |
| `MONGO_URL` | MongoDB connection string |
| `REDIS_URL` | Redis connection string |
| `CELERY_BROKER_URL` | Celery broker (RabbitMQ) |
| `COMICVINE_API_KEY` | External API access |
| `SECRET_KEY` | Django secret key |
| `DJANGO_SETTINGS_MODULE` | Active settings module |

### Frontend Environment

| File | API Base URL |
|------|--------------|
| `.env.development` | `http://127.0.0.1:8000/api` |
| `.env.production` | `https://readcomics.net/api` |

Variable: `NUXT_PUBLIC_API_BASE`

---

## Data Storage

| Storage | Technology | Data |
|---------|------------|------|
| Primary DB | PostgreSQL | Normalized entities, users, reading progress |
| Raw Data | MongoDB | Scraped JSON from ComicVine |
| Message Broker | RabbitMQ | Celery task queue |
| Cache | Redis | Session cache, query cache |
| Static Files | S3/DO Spaces | Collected static assets |
| Media | S3/DO Spaces | User uploads, comic images |

---

## Development Workflow

### Start All Services

```bash
docker compose -f local.yml up
```

### Backend Commands

```bash
# Run tests
docker compose -f local.yml run --rm django pytest

# Run specific test
docker compose -f local.yml run --rm django pytest path/to/test.py::TestClass::test_method

# Test coverage
docker compose -f local.yml run --rm django coverage run -m pytest && coverage html

# Type checking
docker compose -f local.yml run --rm django mypy read_comics

# Linting
docker compose -f local.yml run --rm django black read_comics config
docker compose -f local.yml run --rm django isort read_comics config
docker compose -f local.yml run --rm django flake8 read_comics config

# Create superuser
docker compose -f local.yml run --rm django python manage.py createsuperuser

# Generate OpenAPI schema
docker compose -f local.yml run --rm django python manage.py spectacular --file schema.yaml
```

### Frontend Commands

Run from `frontend/` directory:

```bash
pnpm dev          # Dev server on localhost:3000
pnpm build        # Production build
pnpm lint         # ESLint
pnpm lint:fix     # Auto-fix lint issues
pnpm format       # Check Prettier formatting
pnpm format:fix   # Auto-format
pnpm typecheck    # TypeScript checking
pnpm generate     # Generate types from OpenAPI schema
```

---

## Production Deployment

| Component | Deployment |
|-----------|------------|
| Django | Gunicorn behind Nginx/Traefik |
| Nuxt | Node.js SSR or static hosting |
| Database | Managed PostgreSQL |
| MongoDB | Managed MongoDB Atlas or self-hosted |
| Redis | Managed Redis |
| Static/Media | S3-compatible storage (DO Spaces) |
| Workers | Celery on separate instances |

### Production Architecture

```
                    ┌──────────────┐
                    │   Traefik/   │
                    │    Nginx     │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │   Django   │  │    Nuxt    │  │   Static   │
    │  (Gunicorn)│  │  (Node.js) │  │   (S3)     │
    └─────┬──────┘  └────────────┘  └────────────┘
          │
    ┌─────┴─────┬──────────────┐
    │           │              │
    ▼           ▼              ▼
┌────────┐ ┌────────┐  ┌────────────┐
│Postgres│ │ Redis  │  │   Celery   │
└────────┘ └────────┘  │  Workers   │
                       └────────────┘
```
