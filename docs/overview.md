# Project overview

Read Comics is a web application for managing and browsing comic data. The backend is built with Django, and the frontend runs on Nuxt 3.

## Key components
- [**Django backend**](backend/README.md): applications under `read_comics/` (e.g., `issues/`, `spiders/`, `users/`).
- [**Nuxt frontend**](frontend/README.md): client code in `frontend/`.
- **Infrastructure**: Docker stacks and compose files under `compose/` and the root `local.yml`.

## Repository layout
- `read_comics/` — Django apps and shared backend code.
- `config/` — settings, URL routing, WSGI/ASGI and Celery wiring.
- `frontend/` — Nuxt 3 client.
- `docs/` — project documentation.
- `requirements/`, `pyproject.toml` — dependency definitions.
- `staticfiles/` — collected static assets.

## Useful maps
- [Django pages map](../DJANGO_PAGES_MAP.md)
- [Django pages DRF map](../DJANGO_PAGES_DRF_MAP.md)
- [DRF migration URL map](../DRF_MIGRATION_URL_MAP.md)
