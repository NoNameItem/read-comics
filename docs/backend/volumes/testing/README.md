# Volumes Testing

Testing documentation for the volumes app.

## Overview

The volumes app includes:
- **2 test modules**: URL routing tests, E2E API tests
- **1 factory**: VolumeFactory (with related issues creation)
- **6 fixtures**: Single/batch volumes, with/without issues, finished variants

## Test Files

| File | Purpose | Tests |
|------|---------|-------|
| `test_drf_urls.py` | URL routing verification | 3 endpoint routes |
| `test_e2e.py` | API workflow testing | List, count, filtering, authorization |

## Factories

### VolumeFactory

Creates Volume model instances with optional related issues.

**Parameters**:
- `name` — Volume name (Faker word)
- `short_description` — Description (Faker paragraph)
- `start_year` — Publication year (Faker year)
- `publisher` — Related Publisher (auto-created if not provided)
- `add_issues` — Number of related issues to create (post-generation)

**Usage**:
```python
# Simple volume
volume = VolumeFactory()

# With custom name and year
volume = VolumeFactory(name="Amazing Spider-Man", start_year=1963)

# With related issues
volume = VolumeFactory(add_issues=5)

# Batch creation
volumes = VolumeFactory.create_batch(size=10, add_issues=2)
```

**See**: [factories.md](factories.md)

## Fixtures

### Single Volume Fixtures

- `volume_no_issues()` — Single volume without related issues
- `volume_with_issues()` — Single volume with 1-2 random issues

### Batch Volume Fixtures

- `volumes_no_issues()` — 2-9 volumes without issues
- `volumes_with_issues()` — 2-9 volumes, each with 1-2 issues

### Finished Volume Fixtures

User-dependent fixtures for testing user progress:

- `finished_volume(user)` — Single volume where user finished all issues
- `finished_volumes(user)` — List of volumes where user finished all issues

**Usage**:
```python
def test_hide_finished(volumes_with_issues, finished_volumes, authenticated_api_client):
    # finished_volumes should be hidden by default
    response = authenticated_api_client.get("/api/volumes/")
    assert response.data["count"] == len(volumes_with_issues)
```

**See**: [fixtures.md](fixtures.md)

## Tests

### URL Tests (`test_drf_urls.py`)

Verify DRF endpoint routing:
- `test_count()` — GET /api/volumes/count/
- `test_list()` — GET /api/volumes/
- `test_started()` — GET /api/volumes/started/

**See**: [tests.md](tests.md#url-tests)

### E2E Tests (`test_e2e.py`)

Complete API workflow testing:

#### TestVolumesCount
- `test_count()` — Verify count endpoint returns total volumes

#### TestVolumesList
- `test_dont_hide_finished()` — Show all volumes with ?hide-finished=no
- `test_hide_finished()` — Hide finished by default
- `test_finished_mark()` — Mark finished volumes correctly
- `test_no_finished_mark()` — Mark non-finished volumes correctly
- `test_no_auth_finished_mark()` — Unauthenticated sees None
- `test_data()` — Verify response data structure

**See**: [tests.md](tests.md#e2e-tests)

## Documentation References

- [factories.md](factories.md) — VolumeFactory parameters and usage
- [fixtures.md](fixtures.md) — Volume fixtures patterns and combinations
- [tests.md](tests.md) — Test cases and scenarios
- [../testing/README.md](../testing/README.md) — Global testing overview