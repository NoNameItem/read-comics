# Architecture and structure

## Key directories
- `read_comics/` — domain-specific Django apps (e.g., `issues/`, `spiders/`, `users/`).
- `config/` — settings, routing, Celery entry points, and WSGI/ASGI modules.
- `requirements/` and `pyproject.toml` — dependency manifests.
- `staticfiles/` — collected static assets.

## Settings
- Base settings live under `config/settings/` and change per environment (dev/test/prod).
- Environment variables cover Celery, email, external integrations, and other secrets.
- The Celery app is configured in `config/celery.py` and uses settings modules for runtime values.
