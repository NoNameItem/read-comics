# Tests, type checks, and background workflow

## Tests and coverage
- `docker-compose -f local.yml run --rm django pytest`
- `docker-compose -f local.yml run --rm django coverage run -m pytest`
- Pytest config in `pytest.ini` adds `--ds=config.settings.test --reuse-db` for local runs.

## Type checks
- `docker-compose -f local.yml run --rm django mypy read_comics`
- Mypy configuration is shared between `pyproject.toml` and `setup.cfg`.

## Background tasks and Celery
- Celery app is instantiated in `config/celery.py`.
- Start the worker with `docker-compose -f local.yml up celeryworker`.
- Brokers and periodic tasks are configured through `config/settings/` modules.

## Documentation helpers
- `docker-compose -f local.yml up docs` boots the Sphinx service.
- API docs can be regenerated via `docker run --rm docs make apidocs`.
