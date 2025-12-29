# CLAUDE.md

## Project Overview

ReadComics.net — Django + Nuxt 3 app for comic book data management.

**Stack:** Django REST Framework, Celery/RabbitMQ, PostgreSQL, MongoDB (cache), Scrapy (ComicVine API), Nuxt 3 + Nuxt UI

**Commands:** See `.claude/commands.md` | **Style:** See `.claude/style.md` | **Docs:** See `.claude/docs-guidelines.md`

## Architecture

### Data Flow
ComicVine API → Scrapy → MongoDB → Celery Tasks → PostgreSQL → DRF API → Nuxt Frontend

### Key Patterns

**ComicvineSyncModel** (`read_comics/utils/models.py`) — Base for all comic entities:
- `MONGO_COLLECTION` — MongoDB collection name
- `COMICVINE_INFO_TASK` — Celery sync task
- `FIELDS_MAPPING` — ComicVine → Django field mapping
- `.sync()` — trigger MongoDB → PostgreSQL sync

**API Structure:**
- `<app>/api/viewsets.py`, `<app>/api/serializers.py`
- Routes: `config/api_router.py` (DRF Extensions router)
- Auth: JWT (SimpleJWT), session in DEBUG

**Celery Routing** (`config/celery_app.py`):
- `*_update` tasks → `read_comics_spiders` queue
- Missing issues → entity-specific queues
- Default: `read_comics_default`

### Structure
- Backend: `read_comics/` (Django apps: issues, volumes, characters, etc.)
- Frontend: `frontend/app/` (pages, components, stores, composables)
- Spiders: `read_comics/spiders/spiders/`

## Token Optimization

**Read docs first, source code second:**
1. `docs/backend/<app>/README.md` → overview
2. `models.md`, `api/serializers.md`, `api/viewsets.md` → details
3. Source code → only for implementation specifics

## Project Management

- **Jira:** RC @ https://nonameitem.atlassian.net
- **Version:** 1.26.0 (`pyproject.toml`)

## Integrations

**Context7:** Auto-use for library docs, code generation, API references.

**Research-Plan-Implement Framework:**
1. `/1_research_codebase` — Explore codebase
2. `/2_create_plan` — Create implementation plan
3. `/3_validate_plan` — Verify plan
4. `/4_implement_plan` — Execute
5. `/5_save_progress` / `/6_resume_work` — Session management
7. `/7_research_cloud` — Cloud infrastructure (READ-ONLY)

Artifacts: `thoughts/shared/{research,plans,sessions,cloud}/`
