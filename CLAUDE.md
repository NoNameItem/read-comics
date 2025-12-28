# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ReadComics.net is a full-stack web application for exploring and managing comic book data. The project consists of:
- **Backend**: Django + Django REST Framework API with Celery for background tasks
- **Frontend**: Nuxt 3 (Vue 3) application with Nuxt UI components
- **Data Sources**: ComicVine API integration via Scrapy spiders, MongoDB for caching scraped data, PostgreSQL for application data
- **Task Processing**: Celery workers with RabbitMQ message broker

## Development Environment Setup

### Backend (Django)

Run all backend commands from repository root using Docker Compose:

```bash
# Start all services
docker compose -f local.yml up

# Create superuser
docker compose -f local.yml run --rm backend python manage.py createsuperuser

# Run migrations
docker compose -f local.yml run --rm backend python manage.py migrate

# Run tests
docker compose -f local.yml run --rm backend pytest

# Run tests with coverage
docker compose -f local.yml run --rm backend coverage run -m pytest
docker compose -f local.yml run --rm backend coverage html

# Type checking
docker compose -f local.yml run --rm backend mypy read_comics

# Start Celery worker
docker compose -f local.yml up celeryworker

# Django shell
docker compose -f local.yml run --rm backend python manage.py shell
```

**Services available:**
- Django backend: http://localhost:8000
- PostgreSQL: localhost:5432
- MongoDB: localhost:27017
- RabbitMQ Management UI: http://localhost:15672
- MailHog (email testing): http://localhost:8026
- Flower (Celery monitoring): http://localhost:5555

### Frontend (Nuxt 3)

Run all frontend commands from `frontend/` directory:

```bash
# Install dependencies
pnpm install

# Start dev server
pnpm dev
# Frontend runs at http://localhost:3000

# Production build
pnpm build
pnpm preview

# Linting
pnpm lint        # Check only
pnpm lint:fix    # Auto-fix

# Formatting
pnpm format      # Check only
pnpm format:fix  # Auto-fix

# Type checking
pnpm typecheck
```

## Architecture Overview

### Backend Structure

**Django Apps** (in `read_comics/`):
- `issues/`, `volumes/`, `publishers/` - Core comic book models
- `characters/`, `teams/`, `people/` - Creator and character data
- `concepts/`, `locations/`, `objects/`, `story_arcs/`, `powers/` - Related entities
- `missing_issues/` - Tracks gaps in collection and API queue management
- `users/` - User authentication and profiles
- `spiders/` - Scrapy configuration and ComicVine spiders
- `utils/` - Shared utilities, base models, logging, tasks
- `search/` - Full-text search with django-watson

**Key Base Classes:**
- `ComicvineSyncModel` (`read_comics/utils/models.py`) - Base model for entities synced from ComicVine API
  - Manages MongoDB caching, API synchronization, field mapping from ComicVine
  - All comic entities inherit from this (Issue, Volume, Character, etc.)
- `ImageMixin` (`read_comics/utils/model_mixins.py`) - Handles image URLs and S3 storage

**Celery Task Organization:**
- Task routing is configured in `config/celery_app.py`
- Tasks ending with `_update` go to `read_comics_spiders` queue (web scraping)
- Missing issues tasks route to entity-specific queues (e.g., `read_comics_characters`)
- Default queue: `read_comics_default`

**API Structure:**
- All viewsets are in `<app>/api/viewsets.py`
- Serializers in `<app>/api/serializers.py`
- API routes registered in `config/api_router.py` using DRF Extensions router
- Authentication: JWT tokens with SimpleJWT, session auth in DEBUG mode

### Frontend Structure

**Directory Layout** (in `frontend/app/`):
- `pages/` - File-based routing (Nuxt auto-routing)
- `components/` - Vue components
- `layouts/` - Page layouts
- `stores/` - Pinia state management
- `composables/` - Vue composables
- `types/` - TypeScript type definitions
- `utils/` - Utility functions

**Tech Stack:**
- Nuxt 4.x with Nuxt UI (component library)
- Pinia for state management
- TypeScript
- Unovis for data visualizations
- date-fns for date handling

### Data Flow

1. **Scrapy Spiders** fetch data from ComicVine API → store in MongoDB
2. **Celery Tasks** process MongoDB data → create/update PostgreSQL models via `ComicvineSyncModel`
3. **Django Views/API** serve data from PostgreSQL
4. **Nuxt Frontend** consumes REST API and renders UI

## Code Style

### Python
- **Formatter**: Black with 120-character line length
- **Imports**: isort with trailing commas
- **Linting**: flake8 (configured in `setup.cfg`)
- **Type Checking**: mypy with Django and DRF plugins
- **Pre-commit hooks**: Black, isort, flake8, trailing whitespace
- **Quotes**: Double quotes preferred (enforced by flake8-quotes)
- **Line length**: 120 characters

### Frontend
- **Linting**: ESLint with @nuxt/eslint config
- **Formatting**: Prettier
- **Style**: Follows Antfu's ESLint config
- **Package Manager**: pnpm (v10.23.0)

## Testing

### Backend Testing
- Framework: pytest with pytest-django
- Settings: Uses `config.settings.test`
- Configuration: `pytest.ini` - `--ds=config.settings.test --reuse-db`
- Test files: `test_*.py` or `tests.py` in each app
- Coverage: Run with `coverage run -m pytest`, generate reports with `coverage html`

### Running Specific Tests
```bash
# Single test file
docker-compose -f local.yml run --rm backend pytest read_comics/issues/tests/test_models.py

# Single test function
docker-compose -f local.yml run --rm backend pytest read_comics/issues/tests/test_models.py::test_issue_creation

# With debugging output
docker-compose -f local.yml run --rm backend pytest -v -s
```

## Commits

Follow **Conventional Commits** format (configured in `conventionalcommit.json`):

```
<type>(<scope>): <description>

[optional body]
```

**Common types**: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`
**Common scopes**: App names (e.g., `issues`, `spiders`, `users`, `core`)

Examples:
- `feat(issues): add support for variant covers`
- `fix(spiders): handle missing image URLs in ComicVine response`
- `refactor(core): extract common sync logic to base model`

## Key Patterns and Conventions

### Working with ComicvineSyncModel
- Models syncing from ComicVine inherit from `ComicvineSyncModel`
- Define `MONGO_COLLECTION` class attribute (MongoDB collection name)
- Define `COMICVINE_INFO_TASK` (Celery task for syncing)
- Define `COMICVINE_API_URL` (ComicVine API endpoint)
- Field mapping via `_DEFAULT_FIELDS_MAPPING` or custom `FIELDS_MAPPING`
- Call `.sync()` to trigger data sync from MongoDB → PostgreSQL

### API Development
- Viewsets use DRF Extensions for nested routing support
- Use `ExtendedDefaultRouter` in DEBUG mode (browsable API)
- Use `ExtendedSimpleRouter` in production
- Serializers often have separate read/write serializers
- CORS configured via django-cors-headers

### Celery Tasks
- Task modules: `<app>/tasks.py`
- Import and bind Celery app: `from config.celery_app import app`
- Use `@app.task` decorator
- Task routing configured automatically based on naming patterns
- Check `config/celery_app.py` for queue routing logic

### Scrapy Spiders
- All spiders in `read_comics/spiders/spiders/`
- Base spider: `base_spider.py` (handles ComicVine API pagination, rate limiting)
- Entity-specific spiders inherit from base: `IssuesSpider`, `VolumesSpider`, etc.
- Configuration: `read_comics/spiders/settings.py`
- MongoDB pipelines: `read_comics/spiders/pipelines.py`

## Documentation References
- Django + DRF migration mapping: `DRF_MIGRATION_URL_MAP.md`
- Django pages map: `DJANGO_PAGES_MAP.md` and `DJANGO_PAGES_DRF_MAP.md`
- Refactoring plan: `REFACTORING_PLAN.md`

## Documentation Guidelines

**CRITICAL: Always follow `docs/doc-style.md` when writing documentation**

All documentation under `docs/backend/` must follow these rules:

1. **Structure**: Use `# Title` → `## Summary` → `## Reference` → `### Class/Function` → `#### Details`
2. **Summary section**: Include one-line bullets for each major entity with anchor links
3. **Endpoint docs**: ONLY in `endpoints.md` (NOT in viewsets.md)
   - Endpoints.md: endpoint descriptions, examples, request/response
   - Viewsets.md: ViewSet configuration, mixins, serializers, queryset only
4. **Docs comments**: Every Python module with docs must have `# Docs: [[docs/path/to_file.md]]` comment
5. **Links**: Use relative links (e.g., `[viewsets.md#classname]`, `../models.md#field`)
6. **English only**: All documentation in English

Before writing or updating documentation:
- Read `docs/doc-style.md` to ensure compliance
- Check adjacent docs for consistency
- Use Summary + Reference pattern
- Add Docs comment to Python module

## Using Documentation to Save Token Usage

**Strategy**: Use documentation as primary source instead of reading full source code.

### When Understanding a Module
1. **First**: Read `docs/backend/<app>/README.md` for overview
2. **Then**: Read relevant documentation files:
   - `models.md` for database schema and relationships
   - `api/serializers.md` for API response structures
   - `api/viewsets.md` for API configuration
   - `tasks.md` for background job definitions
   - `search_adapters.md` for search integration
3. **Finally**: Read source code only if:
   - Need specific implementation details
   - Debugging issues
   - Refactoring code
   - Documentation is incomplete/outdated

### Token Savings
- **models.md** (~3-4 KB) replaces **models.py** (~10+ KB) — 60-70% savings
- **serializers.md** (~3-4 KB) replaces **serializers.py** (~5-8 KB) — 50-60% savings
- **viewsets.md** (~2-3 KB) replaces **viewsets.py** (~8-15 KB) — 70-80% savings

### For New Modules
When writing documentation for new modules:
- Make it comprehensive enough to replace 80% of source code reading
- Include all field names, types, and relationships
- Document method signatures and behavior (not implementation)
- Add configuration details and mixins

**This approach enables efficient work within token budgets across sessions.**

## Project Management

- **Jira Project**: RC
- **Jira Base URL**: https://nonameitem.atlassian.net
- **Version**: 1.26.0 (tracked in `pyproject.toml` and `setup.cfg`)


Always use context7 when I need code generation, setup or configuration steps, or
library/API documentation. This means you should automatically use the Context7 MCP
tools to resolve library id and get library docs without me having to explicitly ask.

## Research-Plan-Implement Framework

This repository uses the Research-Plan-Implement framework with the following workflow commands:

1. `/1_research_codebase` - Deep codebase exploration with parallel AI agents
2. `/2_create_plan` - Create detailed, phased implementation plans
3. `/3_validate_plan` - Verify implementation matches plan
4. `/4_implement_plan` - Execute plan systematically
5. `/5_save_progress` - Save work session state
6. `/6_resume_work` - Resume from saved session
7. `/7_research_cloud` - Analyze cloud infrastructure (READ-ONLY)

Research findings are saved in `thoughts/shared/research/`
Implementation plans are saved in `thoughts/shared/plans/`
Session summaries are saved in `thoughts/shared/sessions/`
Cloud analyses are saved in `thoughts/shared/cloud/`
