# Repository Guidelines

## Project Structure & Module Organization
- `read_comics/` contains Django apps (e.g., `issues/`, `spiders/`, `users/`) plus shared utilities and templates.
- `config/` holds Django settings, URLs, WSGI, and Celery app wiring.
- `frontend/` is the Nuxt 3 client with pages, components, stores, and assets.
- `docs/` contains Sphinx documentation sources; `compose/` and `local.yml` support Docker workflows.
- `requirements/` and `pyproject.toml` define Python dependencies and tooling; `staticfiles/` stores collected static assets.

## Build, Test, and Development Commands
- Backend (Docker, from repo root):
  - `docker-compose -f local.yml up` starts the Django stack and dependencies.
  - `docker-compose -f local.yml run --rm django python manage.py createsuperuser` creates an admin user.
  - `docker-compose -f local.yml run --rm django pytest` runs the test suite.
  - `docker-compose -f local.yml run --rm django coverage run -m pytest` runs tests with coverage.
  - `docker-compose -f local.yml run --rm django mypy read_comics` runs type checks.
  - `docker-compose -f local.yml up celeryworker` starts a Celery worker.
- Frontend (run in `frontend/`):
  - `pnpm install` installs dependencies.
  - `pnpm dev` starts the Nuxt dev server.
  - `pnpm build` builds for production; `pnpm preview` serves the build.
  - `pnpm lint`/`pnpm lint:check` run ESLint.
- Docs: `docker-compose -f local.yml up docs` builds and serves Sphinx docs; `docker run --rm docs make apidocs` regenerates API docs.

## Coding Style & Naming Conventions
- Python: Black with 120-char lines, flake8 and isort configured in `setup.cfg`; prefer double quotes.
- Type hints are encouraged; mypy uses Django/DRF plugins.
- Frontend: ESLint with Antfu config; `lint-staged` runs `eslint --fix` on commits.

## Testing Guidelines
- Pytest is configured in `pytest.ini` with `--ds=config.settings.test --reuse-db`.
- Test files should be named `test_*.py` or `tests.py`.
- There is no documented frontend test runner; use linting and manual checks for UI changes.

## Commit & Pull Request Guidelines
- Follow Conventional Commits: `type(scope): summary` (types/scopes in `conventionalcommit.json`, e.g., `feat(core): ...`, `fix(spiders): ...`).
- No PR template is defined; include a short description, testing notes, and screenshots for UI changes when applicable.

## Configuration Notes
- Django settings live in `config/settings/`; environment-driven values (Celery, email, etc.) are expected for local and production runs.
