# Location URL Tests in `read_comics/locations/tests/test_drf_urls.py`

## Summary

URL routing tests verifying correct URL patterns and reverse resolution for all Location API endpoints.

## Test Class

### TestLocationsApiUrls

Static test class containing four URL routing tests for locations endpoints.

## Test Methods

### test_list
**Endpoint:** `GET /api/locations/` | **Fixtures:** None

Verifies `reverse("api:location-list")` returns `/api/locations/` and `resolve` returns view name `api:location-list`.

### test_detail
**Endpoint:** `GET /api/locations/{slug}/` | **Fixtures:** `location_with_issues`

Verifies detail URL pattern accepts slug parameter and correctly resolves to `api:location-detail`.

### test_technical_info
**Endpoint:** `GET /api/locations/{slug}/technical-info/` | **Fixtures:** `location_with_issues`

Verifies custom action URL pattern registered correctly with slug parameter.

### test_count
**Endpoint:** `GET /api/locations/count/` | **Fixtures:** None

Verifies count action URL pattern registered as list route with view name `api:location-count`.

## URL Pattern Structure

| Endpoint | URL Pattern | View Name | HTTP Method |
|---|---|---|---|
| List | `/api/locations/` | `api:location-list` | GET |
| Detail | `/api/locations/{slug}/` | `api:location-detail` | GET |
| Count | `/api/locations/count/` | `api:location-count` | GET |
| Technical Info | `/api/locations/{slug}/technical-info/` | `api:location-technical-info` | GET |

## Running Tests

```bash
docker-compose -f local.yml run --rm backend pytest read_comics/locations/tests/test_drf_urls.py
```

## Related Components

- **ViewSet:** [`LocationViewSet`](../api/viewsets.md#locationviewset)
- **Endpoints:** [Location API Endpoints](../api/endpoints.md)
