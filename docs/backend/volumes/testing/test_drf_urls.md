# Volumes DRF URLs Tests

URL routing tests for volumes API endpoints (`test_drf_urls.py`).

## Overview

Verifies that Django URL names map correctly to URL paths using `reverse()` and `resolve()`.

## Test Class: TestVolumesApiUrls

### test_count

**Endpoint**: GET /api/volumes/count/

**Name**: `api:volume-count`

**Verified**:
- `reverse("api:volume-count")` returns `/api/volumes/count/`
- `resolve("/api/volumes/count/")` returns `api:volume-count`

**Purpose**: Count action endpoint (from `CountActionMixin`)

**Assertion pattern**:
```python
assert reverse("api:volume-count") == "/api/volumes/count/"
assert resolve("/api/volumes/count/").view_name == "api:volume-count"
```

### test_list

**Endpoint**: GET /api/volumes/

**Name**: `api:volume-list`

**Verified**:
- `reverse("api:volume-list")` returns `/api/volumes/`
- `resolve("/api/volumes/")` returns `api:volume-list`

**Purpose**: Standard REST list endpoint

**Assertion pattern**:
```python
assert reverse("api:volume-list") == "/api/volumes/"
assert resolve("/api/volumes/").view_name == "api:volume-list"
```

### test_started

**Endpoint**: GET /api/volumes/started/

**Name**: `api:volume-started`

**Verified**:
- `reverse("api:volume-started")` returns `/api/volumes/started/`
- `resolve("/api/volumes/started/")` returns `api:volume-started`

**Purpose**: Started items action (from `StartedActionMixin`)

**Assertion pattern**:
```python
assert reverse("api:volume-started") == "/api/volumes/started/"
assert resolve("/api/volumes/started/").view_name == "api:volume-started"
```

## Test Execution

**Run URL tests**:
```bash
pytest read_comics/volumes/tests/test_drf_urls.py
```

**Run specific test**:
```bash
pytest read_comics/volumes/tests/test_drf_urls.py::TestVolumesApiUrls::test_count
```

## What's Tested

| Aspect | Tested | Purpose |
|--------|--------|---------|
| URL path | Yes | Ensures URL matches convention |
| URL name | Yes | Ensures name available for reverse() |
| Bidirectional | Yes | Both reverse() and resolve() verified |
| ViewSet connection | No | (Tested in E2E tests) |
| Permissions | No | (Tested in E2E tests) |

## Why These Tests

URL tests catch:
- **Typos** in route definitions
- **Missing** action decorators
- **Accidental** URL path changes
- **Broken** reverse() calls in templates

They run **fast** (no database access) and serve as quick smoke tests for routing configuration.

## Related Configuration

These tests depend on:
- DRF `VolumesViewSet` in `api/viewsets.py`
- `api_router.register()` calls in `config/api_router.py`
- Mixins: `CountActionMixin`, `StartedActionMixin`

## Adding New URL Tests

When adding new endpoints:

1. Add custom action to ViewSet:
   ```python
   class VolumesViewSet(ViewSet):
       @action(detail=False)
       def my_action(self, request):
           ...
   ```

2. Add corresponding URL test:
   ```python
   def test_my_action(self):
       assert reverse("api:volume-my_action") == "/api/volumes/my_action/"
       assert resolve("/api/volumes/my_action/").view_name == "api:volume-my_action"
   ```
