# CLAUDE.md

## Project Overview

ReadComics.net — Django + Nuxt 3 app for comic book data management.

**Stack:** Django REST Framework, Celery/RabbitMQ, PostgreSQL, MongoDB (cache), Scrapy (ComicVine API), Nuxt 3 + Nuxt UI

**Commands:** See `.claude/commands.md` | **Style:** See `.claude/style.md` | **Docs:** See `.claude/docs-guidelines.md`

## Architecture

**Detailed docs:**
- Backend: `docs/backend/architecture.md`
- Frontend: `docs/frontend/architecture.md`
- Migration plan: `docs/plans/2026-01-02-drf-nuxt-migration-design.md`

### Data Flow
ComicVine API → Scrapy → MongoDB → Celery Tasks → PostgreSQL → DRF API → Nuxt Frontend

### Key Patterns

**ComicvineSyncModel** (`read_comics/utils/models.py`) — Base for all comic entities

**API Structure:**
- `<app>/api/viewsets.py`, `<app>/api/serializers.py`
- Routes: `config/api_router.py` (DRF Extensions router)
- Auth: JWT (SimpleJWT), session in DEBUG

**Frontend Stack:**
- Data fetching: Pinia Colada (defineQuery + Keys Factory)
- Forms: Zod + useFormErrors composable
- Types: Generated from OpenAPI via openapi-ts
- SSR by default, CSR for private pages

### Structure
- Backend: `read_comics/` (Django apps: issues, volumes, characters, etc.)
- Frontend: `frontend/app/` (pages, components, stores, composables)
- Spiders: `read_comics/spiders/spiders/`

## Testing

**Detailed docs:**
- Backend: `docs/backend/testing/README.md`
- Frontend: `docs/frontend/testing/README.md`

**Backend:** pytest + Factory Boy, files: `test_drf_urls.py` (URL resolution), `test_e2e.py` (API integration)

**Frontend:** Vitest for composables (high priority), Vue Test Utils for components (medium), Playwright for E2E (later)

## Token Optimization

**Read docs first, source code second:**
1. `docs/backend/<app>/README.md` → overview
2. `models.md`, `api/serializers.md`, `api/viewsets.md` → details
3. Source code → only for implementation specifics

## Project Management

- **Jira:** RC @ https://nonameitem.atlassian.net
- **Version:** 1.26.0 (`pyproject.toml`)

## Git Rules

- **NEVER commit without explicit user request** — `git add` is OK, but no `git commit` unless explicitly asked

## Integrations

**Atlassian (Jira/Confluence):**
- **CRITICAL:** NEVER call `mcp__atlassian__*` tools directly — responses are too large and consume context quickly
- ALWAYS wrap Atlassian operations in `Task` tool with `subagent_type="general-purpose"`
- In the prompt, specify exactly what data to return (e.g., "return only: key, summary, status")
- Example:
  ```
  Task(subagent_type="general-purpose",
       prompt="Find Jira issue RC-123. Return only: key, summary, status, assignee displayName")
  ```

**Context7:** Auto-use for library docs, code generation, API references.
