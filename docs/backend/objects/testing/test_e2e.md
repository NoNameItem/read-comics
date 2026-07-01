# Object E2E Tests in `read_comics/objects/tests/test_e2e.py`

## Summary

End-to-end API tests verifying complete workflows for Object endpoints including list, detail, count, and technical-info actions with various filters, ordering, pagination, and authorization scenarios.

**Pytest marks:** `pytestmark = pytest.mark.django_db`

## Test Classes

- [`TestObjectsCount`](#testobjectscount) - Count endpoint tests
- [`TestObjectsList`](#testobjectslist) - List endpoint tests
- [`TestObjectDetail`](#testobjectdetail) - Detail endpoint tests
- [`TestObjectTechnicalInfo`](#testobjecttechnicalinfo) - Technical info authorization tests
- [`TestObjectsParametrized`](#testobjectsparametrized) - Parametrized ordering tests
- [`TestObjectsEdgeCases`](#testobjectsedgecases) - Edge case tests
- [`TestObjectsConsistency`](#testobjectsconsistency) - Consistency tests
- [`TestObjectsHTTPMethods`](#testobjectshttpmethods) - HTTP method validation

## Reference

### TestObjectsCount

**test_count:** Verifies default count excludes objects without issues.

**test_count_all:** Verifies show-all filter includes all objects.

### TestObjectsList

**Expected response fields:** `slug`, `image`, `name`, `short_description`, `issues_count`, `volumes_count`

**Test methods:** Covers no_show_all, show_all, data validation, default ordering, ordering by name/issues_count/volumes_count (asc/desc), invalid ordering field, pagination invalid page.

### TestObjectDetail

**test_with_first_issue:** Verifies all detail fields present and accurate.

**test_no_first_issue:** Verifies behavior when objects has no related issues.

**test_not_found:** Verifies 404 response for non-existent slug.

### TestObjectTechnicalInfo

**Expected response fields (staff/superuser only):** `id`, `comicvine_id`, `comicvine_status`, `comicvine_last_match`, `created_dt`, `modified_dt`

**Test methods:** test_no_auth (401), test_regular_user (403), test_staff (200), test_superuser (200 with data validation).

### TestObjectsParametrized

**test_ordering_parametrized:** Parametrized test for all ordering fields (name, issues_count, volumes_count) in both directions.

### TestObjectsEdgeCases

Tests pagination boundaries, large page_size, response structure validation.

### TestObjectsConsistency

**test_list_detail_field_consistency:** Verifies list fields exist in detail response.

**test_count_vs_list_count_consistency:** Verifies count endpoint matches list count.

### TestObjectsHTTPMethods

Tests verifying read-only endpoint restrictions (rejects POST, PUT, PATCH, DELETE).

## Running Tests

```bash
# Run all E2E tests
docker-compose -f local.yml run --rm backend pytest read_comics/objects/tests/test_e2e.py

# Run specific test class
docker-compose -f local.yml run --rm backend pytest read_comics/objects/tests/test_e2e.py::TestObjectsList
```

## Related Components

- **ViewSet:** [`ObjectViewSet`](../api/viewsets.md#objectviewset)
- **Serializers:** [`ObjectsListSerializer`](../api/serializers.md), [`ObjectDetailSerializer`](../api/serializers.md)
- **Model:** [`Object`](../models.md#object)
- **Fixtures:** [Object Fixtures](fixtures.md)
