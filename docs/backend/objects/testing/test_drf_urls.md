# Object URL Tests in `read_comics/objects/tests/test_drf_urls.py`

## Summary

URL routing tests verifying correct URL patterns and reverse resolution for all Object API endpoints.

## Test Class

### TestObjectsApiUrls

Static test class containing four URL routing tests for objects endpoints.

## Test Methods

### test_list
**Endpoint:** `GET /api/objects/` | **Fixtures:** None

Verifies `reverse("api:object-list")` returns `/api/objects/` and `resolve` returns view name `api:object-list`.

### test_detail
**Endpoint:** `GET /api/objects/{slug}/` | **Fixtures:** `object_with_issues`

Verifies detail URL pattern accepts slug parameter and correctly resolves to `api:object-detail`.

### test_technical_info
**Endpoint:** `GET /api/objects/{slug}/technical-info/` | **Fixtures:** `object_with_issues`

Verifies custom action URL pattern registered correctly with slug parameter.

### test_count
**Endpoint:** `GET /api/objects/count/` | **Fixtures:** None

Verifies count action URL pattern registered as list route with view name `api:object-count`.

## URL Pattern Structure

| Endpoint | URL Pattern | View Name | HTTP Method |
|---|---|---|---|
| List | `/api/objects/` | `api:object-list` | GET |
| Detail | `/api/objects/{slug}/` | `api:object-detail` | GET |
| Count | `/api/objects/count/` | `api:object-count` | GET |
| Technical Info | `/api/objects/{slug}/technical-info/` | `api:object-technical-info` | GET |

## Running Tests

```bash
docker-compose -f local.yml run --rm backend pytest read_comics/objects/tests/test_drf_urls.py
```

## Related Components

- **ViewSet:** [`ObjectViewSet`](../api/viewsets.md#objectviewset)
- **Endpoints:** [Object API Endpoints](../api/endpoints.md)
