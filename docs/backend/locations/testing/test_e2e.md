# Location E2E Tests in `read_comics/locations/tests/test_e2e.py`

## Summary

End-to-end API tests verifying complete workflows for Location endpoints including list, detail, count, and technical-info actions with various filters, ordering, pagination, and authorization scenarios.

**Pytest marks:** `pytestmark = pytest.mark.django_db`

## Test Classes

- [`TestLocationsCount`](#testlocationscount) - Count endpoint tests
- [`TestLocationsList`](#testlocationslist) - List endpoint tests
- [`TestLocationDetail`](#testlocationdetail) - Detail endpoint tests
- [`TestLocationTechnicalInfo`](#testlocationtechnicalinfo) - Technical info authorization tests
- [`TestLocationsParametrized`](#testlocationsparametrized) - Parametrized ordering tests
- [`TestLocationsEdgeCases`](#testlocationsedgecases) - Edge case tests
- [`TestLocationsConsistency`](#testlocationsconsistency) - Consistency tests
- [`TestLocationsHTTPMethods`](#testlocationshttpmethods) - HTTP method validation

## Reference

### TestLocationsCount

**test_count:** Verifies default count excludes locations without issues.

**test_count_all:** Verifies show-all filter includes all locations.

### TestLocationsList

**Expected response fields:** `slug`, `image`, `name`, `short_description`, `issues_count`, `volumes_count`

**Test methods:** Covers no_show_all, show_all, data validation, default ordering, ordering by name/issues_count/volumes_count (asc/desc), invalid ordering field, pagination invalid page.

### TestLocationDetail

**test_with_first_issue:** Verifies all detail fields present and accurate.

**test_no_first_issue:** Verifies behavior when locations has no related issues.

**test_not_found:** Verifies 404 response for non-existent slug.

### TestLocationTechnicalInfo

**Expected response fields (staff/superuser only):** `id`, `comicvine_id`, `comicvine_status`, `comicvine_last_match`, `created_dt`, `modified_dt`

**Test methods:** test_no_auth (401), test_regular_user (403), test_staff (200), test_superuser (200 with data validation).

### TestLocationsParametrized

**test_ordering_parametrized:** Parametrized test for all ordering fields (name, issues_count, volumes_count) in both directions.

### TestLocationsEdgeCases

Tests pagination boundaries, large page_size, response structure validation.

### TestLocationsConsistency

**test_list_detail_field_consistency:** Verifies list fields exist in detail response.

**test_count_vs_list_count_consistency:** Verifies count endpoint matches list count.

### TestLocationsHTTPMethods

Tests verifying read-only endpoint restrictions (rejects POST, PUT, PATCH, DELETE).

## Running Tests

```bash
# Run all E2E tests
docker-compose -f local.yml run --rm backend pytest read_comics/locations/tests/test_e2e.py

# Run specific test class
docker-compose -f local.yml run --rm backend pytest read_comics/locations/tests/test_e2e.py::TestLocationsList
```

## Related Components

- **ViewSet:** [`LocationViewSet`](../api/viewsets.md#locationviewset)
- **Serializers:** [`LocationsListSerializer`](../api/serializers.md), [`LocationDetailSerializer`](../api/serializers.md)
- **Model:** [`Location`](../models.md#location)
- **Fixtures:** [Location Fixtures](fixtures.md)
