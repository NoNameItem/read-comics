# Person URL Tests in `read_comics/people/tests/test_drf_urls.py`

## Summary

URL routing tests verifying correct URL patterns and reverse resolution for all Person API endpoints.

## Test Class

### TestPeopleApiUrls

Static test class containing four URL routing tests for people endpoints.

## Test Methods

### test_list
**Endpoint:** `GET /api/people/` | **Fixtures:** None

Verifies `reverse("api:person-list")` returns `/api/people/` and `resolve` returns view name `api:person-list`.

### test_detail
**Endpoint:** `GET /api/people/{slug}/` | **Fixtures:** `person_with_issues`

Verifies detail URL pattern accepts slug parameter and correctly resolves to `api:person-detail`.

### test_technical_info
**Endpoint:** `GET /api/people/{slug}/technical-info/` | **Fixtures:** `person_with_issues`

Verifies custom action URL pattern registered correctly with slug parameter.

### test_count
**Endpoint:** `GET /api/people/count/` | **Fixtures:** None

Verifies count action URL pattern registered as list route with view name `api:person-count`.

## URL Pattern Structure

| Endpoint | URL Pattern | View Name | HTTP Method |
|---|---|---|---|
| List | `/api/people/` | `api:person-list` | GET |
| Detail | `/api/people/{slug}/` | `api:person-detail` | GET |
| Count | `/api/people/count/` | `api:person-count` | GET |
| Technical Info | `/api/people/{slug}/technical-info/` | `api:person-technical-info` | GET |

## Running Tests

```bash
docker-compose -f local.yml run --rm backend pytest read_comics/people/tests/test_drf_urls.py
```

## Related Components

- **ViewSet:** [`PersonViewSet`](../api/viewsets.md#personviewset)
- **Endpoints:** [Person API Endpoints](../api/endpoints.md)
