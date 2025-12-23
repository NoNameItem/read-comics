# Concept URL Tests in `read_comics/concepts/tests/test_drf_urls.py`

## Summary

URL routing tests verifying correct URL patterns and reverse resolution for all Concept API endpoints.

## Test Class

### TestConceptsApiUrls

Static test class containing four URL routing tests for concept endpoints.

## Test Methods

### test_list
**Endpoint:** `GET /api/concepts/` | **Fixtures:** None

Verifies `reverse("api:concept-list")` returns `/api/concepts/` and `resolve` returns view name `api:concept-list`.

### test_detail
**Endpoint:** `GET /api/concepts/{slug}/` | **Fixtures:** `concept_with_issues`

Verifies detail URL pattern accepts slug parameter and correctly resolves to `api:concept-detail`.

### test_technical_info
**Endpoint:** `GET /api/concepts/{slug}/technical-info/` | **Fixtures:** `concept_with_issues`

Verifies custom action URL pattern registered correctly with slug parameter.

### test_count
**Endpoint:** `GET /api/concepts/count/` | **Fixtures:** None

Verifies count action URL pattern registered as list route with view name `api:concept-count`.

## URL Pattern Structure

| Endpoint | URL Pattern | View Name | HTTP Method |
|---|---|---|---|
| List | `/api/concepts/` | `api:concept-list` | GET |
| Detail | `/api/concepts/{slug}/` | `api:concept-detail` | GET |
| Count | `/api/concepts/count/` | `api:concept-count` | GET |
| Technical Info | `/api/concepts/{slug}/technical-info/` | `api:concept-technical-info` | GET |

## Running Tests

```bash
docker-compose -f local.yml run --rm backend pytest read_comics/concepts/tests/test_drf_urls.py
```

## Related Components

- **ViewSet:** [`ConceptViewSet`](../api/viewsets.md#conceptviewset)
- **Endpoints:** [Concept API Endpoints](../api/endpoints.md)