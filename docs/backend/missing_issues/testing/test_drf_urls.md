# MissingIssue URL Tests in `read_comics/missing_issues/tests/test_drf_urls.py`

## Summary

URL routing tests verifying correct URL patterns and reverse resolution for all MissingIssue API endpoints.

## Test Class

### TestMissingIssuesApiUrls

Static test class containing four URL routing tests for missing_issues endpoints.

## Test Methods

### test_list
**Endpoint:** `GET /api/missing_issues/` | **Fixtures:** None

Verifies `reverse("api:missingissue-list")` returns `/api/missing_issues/` and `resolve` returns view name `api:missingissue-list`.

### test_detail
**Endpoint:** `GET /api/missing_issues/{slug}/` | **Fixtures:** `missingissue_with_issues`

Verifies detail URL pattern accepts slug parameter and correctly resolves to `api:missingissue-detail`.

### test_technical_info
**Endpoint:** `GET /api/missing_issues/{slug}/technical-info/` | **Fixtures:** `missingissue_with_issues`

Verifies custom action URL pattern registered correctly with slug parameter.

### test_count
**Endpoint:** `GET /api/missing_issues/count/` | **Fixtures:** None

Verifies count action URL pattern registered as list route with view name `api:missingissue-count`.

## URL Pattern Structure

| Endpoint | URL Pattern | View Name | HTTP Method |
|---|---|---|---|
| List | `/api/missing_issues/` | `api:missingissue-list` | GET |
| Detail | `/api/missing_issues/{slug}/` | `api:missingissue-detail` | GET |
| Count | `/api/missing_issues/count/` | `api:missingissue-count` | GET |
| Technical Info | `/api/missing_issues/{slug}/technical-info/` | `api:missingissue-technical-info` | GET |

## Running Tests

```bash
docker-compose -f local.yml run --rm backend pytest read_comics/missing_issues/tests/test_drf_urls.py
```

## Related Components

- **ViewSet:** [`MissingIssueViewSet`](../api/viewsets.md#missingissueviewset)
- **Endpoints:** [MissingIssue API Endpoints](../api/endpoints.md)
