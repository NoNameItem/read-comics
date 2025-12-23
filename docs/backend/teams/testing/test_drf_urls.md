# Team URL Tests in `read_comics/teams/tests/test_drf_urls.py`

## Summary

URL routing tests verifying correct URL patterns and reverse resolution for all Team API endpoints.

## Test Class

### TestTeamsApiUrls

Static test class containing four URL routing tests for teams endpoints.

## Test Methods

### test_list
**Endpoint:** `GET /api/teams/` | **Fixtures:** None

Verifies `reverse("api:team-list")` returns `/api/teams/` and `resolve` returns view name `api:team-list`.

### test_detail
**Endpoint:** `GET /api/teams/{slug}/` | **Fixtures:** `team_with_issues`

Verifies detail URL pattern accepts slug parameter and correctly resolves to `api:team-detail`.

### test_technical_info
**Endpoint:** `GET /api/teams/{slug}/technical-info/` | **Fixtures:** `team_with_issues`

Verifies custom action URL pattern registered correctly with slug parameter.

### test_count
**Endpoint:** `GET /api/teams/count/` | **Fixtures:** None

Verifies count action URL pattern registered as list route with view name `api:team-count`.

## URL Pattern Structure

| Endpoint | URL Pattern | View Name | HTTP Method |
|---|---|---|---|
| List | `/api/teams/` | `api:team-list` | GET |
| Detail | `/api/teams/{slug}/` | `api:team-detail` | GET |
| Count | `/api/teams/count/` | `api:team-count` | GET |
| Technical Info | `/api/teams/{slug}/technical-info/` | `api:team-technical-info` | GET |

## Running Tests

```bash
docker-compose -f local.yml run --rm backend pytest read_comics/teams/tests/test_drf_urls.py
```

## Related Components

- **ViewSet:** [`TeamViewSet`](../api/viewsets.md#teamviewset)
- **Endpoints:** [Team API Endpoints](../api/endpoints.md)
