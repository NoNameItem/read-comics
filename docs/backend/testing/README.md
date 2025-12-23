# Backend Testing Infrastructure

Overview of the ReadComics Django backend testing organization, structure, and patterns.

## Testing Architecture

### Directory Structure

Each Django app follows a consistent testing pattern:

```
<app>/tests/
├── __init__.py                # Test package marker
├── conftest.py                # pytest fixtures (app-specific)
├── factories.py               # Factory Boy model factories
├── test_drf_urls.py           # URL routing & DRF endpoint tests
└── test_e2e.py                # End-to-end API integration tests
```

**Additional global testing files:**
- `read_comics/conftest.py` — Root-level fixtures (API clients, users, storage)
- `read_comics/utils/test_utils/factories.py` — Shared base factory for ComicVine models

### Test Types

| Type | File | Purpose | DB Access |
|------|------|---------|-----------|
| **URL Tests** | `test_drf_urls.py` | Verify Django URL routing | No |
| **E2E Tests** | `test_e2e.py` | Test complete API workflows | Yes |
| **Factories** | `factories.py` | Create model instances | Yes (on creation) |
| **Fixtures** | `conftest.py` | Provide test data | Via factories |

## Testing Patterns

### Database Access

Tests requiring database are marked with `@pytest.mark.django_db` or `pytestmark = pytest.mark.django_db` at class level.

**Root conftest** provides:
- Autouse `media_storage` fixture — Redirects to tmpdir (no S3 writes)
- Autouse `stop_s3_update` fixture — Mocks S3 metadata operations

### Test Data Creation

**Hierarchy**:
1. **Global factories** — Base classes for common patterns (`ComicvineSyncModelFactory`)
2. **App factories** — Model-specific creation (`VolumeFactory`, `IssueFactory`)
3. **Global fixtures** — Users and clients (`user`, `authenticated_api_client`)
4. **App fixtures** — Entity-specific data (`volumes_with_issues`, `finished_volume`)

**Data flow**: Test → Fixture (parametrizes) → Factory (creates) → Database

### Authentication

API testing uses JWT Bearer tokens:
- Root conftest generates tokens via `RefreshToken.for_user(user)`
- Clients set Authorization header automatically
- Three client types: unauthenticated, authenticated (regular user), staff, superuser

## Core Concepts

### Factories
- Create model instances with fake data (Faker library)
- Support relationships via SubFactory
- Use post_generation for complex setup
- Reusable across all tests (DRY principle)

**See**: [factories.md](factories.md)

### Fixtures
- Inject test data via pytest parameter injection
- Abstract factory calls
- Enable fixture composition (fixtures depending on other fixtures)
- Document test intent through naming

**See**: [fixtures.md](fixtures.md)

### URL Tests
- Verify bidirectional URL mapping (reverse ↔ resolve)
- No database access (fast)
- Catch routing regressions early
- Test both standard and custom action endpoints

### E2E Tests
- Test complete workflows (HTTP → ViewSet → Database → Serializer → Response)
- Validate authentication, filtering, response structure
- Test business logic and computed fields
- Use realistic test data from fixtures

## Running Tests

### Common Commands

**All tests**:
```bash
docker-compose -f local.yml run --rm backend pytest
```

**Specific test file**:
```bash
docker-compose -f local.yml run --rm backend pytest read_comics/volumes/tests/test_e2e.py
```

**Specific test with output**:
```bash
docker-compose -f local.yml run --rm backend pytest -vv -s read_comics/volumes/tests/test_e2e.py::TestVolumesList::test_hide_finished
```

**Coverage report**:
```bash
docker-compose -f local.yml run --rm backend coverage run -m pytest
docker-compose -f local.yml run --rm backend coverage html
```

### Test Discovery

Pytest configuration in `pytest.ini`:
- Discovers files matching `test_*.py` or `*_tests.py`
- Discovers test classes matching `Test*`
- Discovers test functions matching `test_*`

## Best Practices

1. **Use fixtures** — Avoid manual object creation in tests
2. **One concern per test** — Single assertion focus
3. **Realistic testing** — Test full stack (URL → ViewSet → Serializer)
4. **Clear naming** — Test names describe behavior (`test_hide_finished_by_default`)
5. **Parametrize** — Use `@pytest.mark.parametrize` for multiple scenarios
6. **Validate structure** — Check response fields, not just values
7. **Mark appropriately** — `@pytest.mark.django_db` only when needed

## App-Specific Testing

Each major app has dedicated testing documentation:

- [Characters Testing](../characters/testing/README.md)
- [Concepts Testing](../concepts/testing/README.md)
- [Issues Testing](../issues/testing/README.md)
- [Locations Testing](../locations/testing/README.md)
- [Objects Testing](../objects/testing/README.md)
- [People Testing](../people/testing/README.md)
- [Publishers Testing](../publishers/testing/README.md)
- [Story Arcs Testing](../story_arcs/testing/README.md)
- [Teams Testing](../teams/testing/README.md)
- [Users Testing](../users/testing/README.md)
- [Volumes Testing](../volumes/testing/README.md)

Each includes:
- Factory parameters and usage
- Fixture descriptions
- Test patterns and scenarios
- Examples specific to that model

## Documentation References

- [Global Factories](factories.md) — Base factory classes and patterns
- [Global Fixtures](fixtures.md) — Root conftest fixtures
- [Doc Style Guide](../doc-style.md) — Documentation standards
