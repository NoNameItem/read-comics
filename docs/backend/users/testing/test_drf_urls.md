# User URL Tests in `read_comics/users/tests/test_drf_urls.py`

## Summary

URL routing tests verifying correct URL patterns and reverse resolution for all User API endpoints.

## Test Class

### TestUsersApiUrls

Static test class containing four URL routing tests for users endpoints.

## Test Methods

### test_list
**Endpoint:** `GET /api/users/` | **Fixtures:** None

Verifies `reverse("api:user-list")` returns `/api/users/` and `resolve` returns view name `api:user-list`.

### test_detail
**Endpoint:** `GET /api/users/{slug}/` | **Fixtures:** `user_with_issues`

Verifies detail URL pattern accepts slug parameter and correctly resolves to `api:user-detail`.

### test_technical_info
**Endpoint:** `GET /api/users/{slug}/technical-info/` | **Fixtures:** `user_with_issues`

Verifies custom action URL pattern registered correctly with slug parameter.

### test_count
**Endpoint:** `GET /api/users/count/` | **Fixtures:** None

Verifies count action URL pattern registered as list route with view name `api:user-count`.

## URL Pattern Structure

| Endpoint | URL Pattern | View Name | HTTP Method |
|---|---|---|---|
| List | `/api/users/` | `api:user-list` | GET |
| Detail | `/api/users/{slug}/` | `api:user-detail` | GET |
| Count | `/api/users/count/` | `api:user-count` | GET |
| Technical Info | `/api/users/{slug}/technical-info/` | `api:user-technical-info` | GET |

## Running Tests

```bash
docker-compose -f local.yml run --rm backend pytest read_comics/users/tests/test_drf_urls.py
```

## Related Components

- **ViewSet:** [`UserViewSet`](../api/viewsets.md#userviewset)
- **Endpoints:** [User API Endpoints](../api/endpoints.md)
