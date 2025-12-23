# Issue URL Tests in `read_comics/issues/tests/test_drf_urls.py`

## Summary

URL routing tests verifying correct URL patterns and reverse resolution for all Issue API endpoints.

## Test Class

### TestIssuesApiUrls

Static test class containing four URL routing tests for issues endpoints.

## Test Methods

### test_list
**Endpoint:** `GET /api/issues/` | **Fixtures:** None

Verifies `reverse("api:issue-list")` returns `/api/issues/` and `resolve` returns view name `api:issue-list`.

### test_detail
**Endpoint:** `GET /api/issues/{slug}/` | **Fixtures:** `issue_with_issues`

Verifies detail URL pattern accepts slug parameter and correctly resolves to `api:issue-detail`.

### test_technical_info
**Endpoint:** `GET /api/issues/{slug}/technical-info/` | **Fixtures:** `issue_with_issues`

Verifies custom action URL pattern registered correctly with slug parameter.

### test_count
**Endpoint:** `GET /api/issues/count/` | **Fixtures:** None

Verifies count action URL pattern registered as list route with view name `api:issue-count`.

## URL Pattern Structure

| Endpoint | URL Pattern | View Name | HTTP Method |
|---|---|---|---|
| List | `/api/issues/` | `api:issue-list` | GET |
| Detail | `/api/issues/{slug}/` | `api:issue-detail` | GET |
| Count | `/api/issues/count/` | `api:issue-count` | GET |
| Technical Info | `/api/issues/{slug}/technical-info/` | `api:issue-technical-info` | GET |

## Running Tests

```bash
docker-compose -f local.yml run --rm backend pytest read_comics/issues/tests/test_drf_urls.py
```

## Related Components

- **ViewSet:** [`IssueViewSet`](../api/viewsets.md#issueviewset)
- **Endpoints:** [Issue API Endpoints](../api/endpoints.md)
