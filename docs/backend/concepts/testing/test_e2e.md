# Concept E2E Tests in `read_comics/concepts/tests/test_e2e.py`

## Summary

End-to-end API tests verifying complete workflows for Concept endpoints including list, detail, count, and technical-info actions with various filters, ordering, pagination, and authorization scenarios.

**Pytest marks:** `pytestmark = pytest.mark.django_db`

## Test Classes

- [`TestConceptsCount`](#testconceptscount) - Count endpoint tests (2 methods)
- [`TestConceptsList`](#testconceptslist) - List endpoint tests (11 methods)
- [`TestConceptDetail`](#testconceptdetail) - Detail endpoint tests (3 methods)
- [`TestConceptTechnicalInfo`](#testconcepttechnicalinfo) - Technical info authorization tests (4 methods)
- [`TestConceptsParametrized`](#testconceptsparametrized) - Parametrized ordering tests (1 method, 6 variations)
- [`TestConceptsEdgeCases`](#testconceptsedgecases) - Edge case tests (5 methods)
- [`TestConceptsConsistency`](#testconceptsconsistency) - Consistency tests (2 methods)
- [`TestConceptsHTTPMethods`](#testconceptshttpmethods) - HTTP method validation (3 methods)

## Reference

### TestConceptsCount

#### test_count
**Endpoint:** `GET /api/concepts/count/` | **Fixtures:** `api_client`, `concepts_no_issues`, `concepts_with_issues`

Verifies default count excludes concepts without issues.

#### test_count_all
**Endpoint:** `GET /api/concepts/count/?show-all=yes` | **Fixtures:** `api_client`, `concepts_no_issues`, `concepts_with_issues`

Verifies show-all filter includes all concepts.

### TestConceptsList

**Expected response fields:**

| Field | Type | Purpose |
|---|---|---|
| `slug` | String | Concept URL slug |
| `image` | String | Concept image URL |
| `name` | String | Concept name |
| `short_description` | Text | Brief description |
| `issues_count` | Integer | Count of related issues |
| `volumes_count` | Integer | Count of distinct volumes |

**Test methods:** 11 tests covering no_show_all, show_all, data validation, default ordering, ordering by name (asc/desc), ordering by issues_count (asc/desc), ordering by volumes_count (asc/desc), invalid ordering field, pagination invalid page.

### TestConceptDetail

#### test_with_first_issue
**Endpoint:** `GET /api/concepts/{slug}/` | **Fixtures:** `api_client`, `concept_with_issues`

Verifies all detail fields present and accurate: slug, name, aliases (converted to list), start_year, first_issue_name/slug, comicvine_url, descriptions, download_size, download_link.

#### test_no_first_issue
**Endpoint:** `GET /api/concepts/{slug}/` | **Fixtures:** `api_client`, `concept_no_issues`

Verifies first issue slug is None when no related issue, download size shows "0 bytes".

#### test_not_found
**Endpoint:** `GET /api/concepts/does-not-exist/` | **Fixtures:** `api_client`

Verifies 404 response for non-existent slug.

### TestConceptTechnicalInfo

**Expected response fields (staff/superuser only):**

| Field | Type | Purpose |
|---|---|---|
| `id` | Integer | Database primary key |
| `comicvine_id` | Integer | ComicVine API ID |
| `comicvine_status` | String | Sync status display value |
| `comicvine_last_match` | DateTime | Last sync timestamp (ISO format) |
| `created_dt` | DateTime | Creation timestamp |
| `modified_dt` | DateTime | Last modification timestamp |

**Test methods:** test_no_auth (401), test_regular_user (403), test_staff (200), test_superuser (200 with data validation, Python 3.12+).

### TestConceptsParametrized

**test_ordering_parametrized:** Parametrized test for all ordering fields (name, issues_count, volumes_count) in both directions.

### TestConceptsEdgeCases

Tests pagination boundaries (page=1, page=0, page=-1), large page_size, response structure validation.

### TestConceptsConsistency

**test_list_detail_field_consistency:** Verifies list fields exist in detail response.

**test_count_vs_list_count_consistency:** Verifies count endpoint matches list count.

### TestConceptsHTTPMethods

**Tests:** list_endpoint_rejects_post, detail_endpoint_rejects_put, response_content_type_is_json.

## Running Tests

```bash
# Run all E2E tests
docker-compose -f local.yml run --rm backend pytest read_comics/concepts/tests/test_e2e.py

# Run specific test class
docker-compose -f local.yml run --rm backend pytest read_comics/concepts/tests/test_e2e.py::TestConceptsList
```

## Related Components

- **ViewSet:** [`ConceptViewSet`](../api/viewsets.md#conceptviewset)
- **Serializers:** [`ConceptsListSerializer`](../api/serializers.md#conceptslistserializer), [`ConceptDetailSerializer`](../api/serializers.md#conceptdetailserializer)
- **Model:** [`Concept`](../models.md#concept)
- **Fixtures:** [Concept Fixtures](fixtures.md)