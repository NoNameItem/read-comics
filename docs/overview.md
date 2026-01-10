# Project Overview

**Read Comics** is a full-stack web application for browsing and managing comic data scraped from ComicVine.

## Core Data Flow

```
ComicVine API → Scrapy Spiders → MongoDB (raw) → Celery Tasks → PostgreSQL → DRF API → Nuxt Frontend
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 4.x, Django REST Framework, Celery |
| Database | PostgreSQL (primary), MongoDB (raw scrape data) |
| Message Broker | RabbitMQ |
| Cache | Redis |
| Frontend | Nuxt 3, Nuxt UI v4, Pinia, Axios |
| Infrastructure | Docker Compose |

## Key Components

- [**Django backend**](backend/README.md) — domain-driven apps under `read_comics/` handling API, data sync, and business logic
- [**Nuxt frontend**](frontend/README.md) — Nuxt 3 client in `frontend/` with SSR support and Nuxt UI components
- **Infrastructure** — Docker stacks and compose files under `compose/` and the root `local.yml`

## Key Services (local.yml)

| Service | Port | Purpose |
|---------|------|---------|
| backend | 8000 | Django API server |
| postgres | 5432 | Primary database |
| mongodb | 27017 | Raw scrape data |
| rabbitmq | 5672, 15672 | Celery broker |
| redis | — | Cache |
| celeryworker | — | Background tasks |
| flower | 5555 | Celery monitoring |
| mailhog | 8026 | Email testing |
| docs | 7001 | Documentation server |

**Note:** Frontend runs separately via `pnpm dev` in `frontend/` (port 3000).

## Repository Layout

```
read_comics/          # Django apps and shared backend code
├── characters/       # Character entities
├── issues/           # Comic issues
├── volumes/          # Comic series
├── publishers/       # Publishing companies
├── people/           # Creators
├── teams/            # Superhero teams
├── story_arcs/       # Cross-issue storylines
├── concepts/         # Abstract concepts
├── locations/        # Places
├── objects/          # Items and artifacts
├── powers/           # Superpowers
├── core/             # Shared utilities, collectors
├── users/            # Authentication
├── search/           # django-watson search
├── spiders/          # Scrapy spiders
├── missing_issues/   # Admin gap detection
└── utils/            # Shared models, mixins, API utilities

config/               # Settings, URL routing, WSGI/ASGI, Celery
frontend/             # Nuxt 3 client
docs/                 # Project documentation
requirements/         # Python dependencies
compose/              # Docker configuration
staticfiles/          # Collected static assets
```

## Architecture Documentation

- [Backend Architecture](backend/architecture.md) — data flow, models, API layer, Celery tasks
- [Frontend Architecture](frontend/architecture.md) — tech stack, patterns, data fetching, SSR strategy
- [Infrastructure](infrastructure.md) — Docker services, environment configuration, deployment

## Development

- [Local Development](dev.md) — setup and commands
- [Backend Workflow](backend/workflow.md) — testing, linting, type checking

## Maps

- [Django pages map](../DJANGO_PAGES_MAP.md)
- [Django pages DRF map](../DJANGO_PAGES_DRF_MAP.md)
- [DRF migration URL map](../DRF_MIGRATION_URL_MAP.md)
