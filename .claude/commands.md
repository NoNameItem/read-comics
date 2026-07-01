# Development Commands

## Backend (Docker Compose)

All commands use `docker compose -f local.yml`:

| Command | Description |
|---------|-------------|
| `up` | Start all services |
| `run --rm backend pytest` | Run tests |
| `run --rm backend pytest -v -s` | Tests with debug output |
| `run --rm backend coverage run -m pytest && coverage html` | Coverage report |
| `run --rm backend mypy read_comics` | Type checking |
| `run --rm backend python manage.py migrate` | Run migrations |
| `run --rm backend python manage.py createsuperuser` | Create admin |
| `run --rm backend python manage.py shell` | Django shell |
| `up celeryworker` | Start Celery |

**Services:**
- Backend: localhost:8000
- PostgreSQL: localhost:5432
- MongoDB: localhost:27017
- RabbitMQ: localhost:15672
- MailHog: localhost:8026
- Flower: localhost:5555

## Frontend (pnpm)

Run from `frontend/` directory:

| Command | Description |
|---------|-------------|
| `pnpm dev` | Dev server (localhost:3000) |
| `pnpm build` | Production build |
| `pnpm lint:fix` | Lint and fix |
| `pnpm format:fix` | Format code |
| `pnpm typecheck` | TypeScript check |
