# Publisher URL Tests in `read_comics/publishers/tests/test_drf_urls.py`

## Summary

URL routing tests verifying correct URL patterns and reverse resolution for all Publisher API endpoints.

## Test Class

### TestPublishersApiUrls

Static test class containing four URL routing tests for publishers endpoints.

## Test Methods

### test_list
**Endpoint:** `GET /api/publishers/` | **Fixtures:** None

Verifies `reverse("api:publisher-list")` returns `/api/publishers/` and `resolve` returns view name `api:publisher-list`.

### test_detail
**Endpoint:** `GET /api/publishers/{slug}/` | **Fixtures:** `publisher_with_issues`

Verifies detail URL pattern accepts slug parameter and correctly resolves to `api:publisher-detail`.

### test_technical_info
**Endpoint:** `GET /api/publishers/{slug}/technical-info/` | **Fixtures:** `publisher_with_issues`

Verifies custom action URL pattern registered correctly with slug parameter.

### test_count
**Endpoint:** `GET /api/publishers/count/` | **Fixtures:** None

Verifies count action URL pattern registered as list route with view name `api:publisher-count`.

## URL Pattern Structure

| Endpoint | URL Pattern | View Name | HTTP Method |
|---|---|---|---|
| List | `/api/publishers/` | `api:publisher-list` | GET |
| Detail | `/api/publishers/{slug}/` | `api:publisher-detail` | GET |
| Count | `/api/publishers/count/` | `api:publisher-count` | GET |
| Technical Info | `/api/publishers/{slug}/technical-info/` | `api:publisher-technical-info` | GET |

## Running Tests

```bash
docker-compose -f local.yml run --rm backend pytest read_comics/publishers/tests/test_drf_urls.py
```

## Related Components

- **ViewSet:** [`PublisherViewSet`](../api/viewsets.md#publisherviewset)
- **Endpoints:** [Publisher API Endpoints](../api/endpoints.md)
