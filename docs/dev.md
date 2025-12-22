# Local development

## Backend (Docker)
See the [Backend (Django) guide](backend/README.md) for architectural context.
Run from the repository root:
- `docker-compose -f local.yml up`
- `docker-compose -f local.yml run --rm django python manage.py createsuperuser`
- `docker-compose -f local.yml run --rm django pytest`
- `docker-compose -f local.yml run --rm django coverage run -m pytest`
- `docker-compose -f local.yml run --rm django mypy read_comics`

## Frontend (Nuxt 3)
See the [Frontend (Nuxt 3) guide](frontend/README.md) for structure, stores, and assets.
Run from the `frontend/` directory:
- `pnpm install`
- `pnpm dev`
- `pnpm build`
- `pnpm preview`
- `pnpm lint`
- `pnpm lint:check`

## Documentation
- Start Sphinx with `docker-compose -f local.yml up docs`.
- Regenerate API docs via `docker run --rm docs make apidocs`.
