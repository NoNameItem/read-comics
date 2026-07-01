# Person E2E Tests in `read_comics/people/tests/test_e2e.py`

## Summary

End-to-end API tests verifying complete workflows for Person endpoints including list, detail, count, and technical-info actions with various filters, ordering, pagination, and authorization scenarios.

**Pytest marks:** `pytestmark = pytest.mark.django_db`

## Test Classes

- [`TestPeopleCount`](#testpeoplecount) - Count endpoint tests
- [`TestPeopleList`](#testpeoplelist) - List endpoint tests
- [`TestPersonDetail`](#testpersondetail) - Detail endpoint tests
- [`TestPersonTechnicalInfo`](#testpersontechnicalinfo) - Technical info authorization tests
- [`TestPeopleParametrized`](#testpeopleparametrized) - Parametrized ordering tests
- [`TestPeopleEdgeCases`](#testpeopleedgecases) - Edge case tests
- [`TestPeopleConsistency`](#testpeopleconsistency) - Consistency tests
- [`TestPeopleHTTPMethods`](#testpeoplehttpmethods) - HTTP method validation

## Reference

### TestPeopleCount

**test_count:** Verifies default count excludes people without issues.

**test_count_all:** Verifies show-all filter includes all people.

### TestPeopleList

**Expected response fields:** `slug`, `image`, `name`, `short_description`, `issues_count`, `volumes_count`

**Test methods:** Covers no_show_all, show_all, data validation, default ordering, ordering by name/issues_count/volumes_count (asc/desc), invalid ordering field, pagination invalid page.

### TestPersonDetail

**test_with_first_issue:** Verifies all detail fields present and accurate.

**test_no_first_issue:** Verifies behavior when people has no related issues.

**test_not_found:** Verifies 404 response for non-existent slug.

### TestPersonTechnicalInfo

**Expected response fields (staff/superuser only):** `id`, `comicvine_id`, `comicvine_status`, `comicvine_last_match`, `created_dt`, `modified_dt`

**Test methods:** test_no_auth (401), test_regular_user (403), test_staff (200), test_superuser (200 with data validation).

### TestPeopleParametrized

**test_ordering_parametrized:** Parametrized test for all ordering fields (name, issues_count, volumes_count) in both directions.

### TestPeopleEdgeCases

Tests pagination boundaries, large page_size, response structure validation.

### TestPeopleConsistency

**test_list_detail_field_consistency:** Verifies list fields exist in detail response.

**test_count_vs_list_count_consistency:** Verifies count endpoint matches list count.

### TestPeopleHTTPMethods

Tests verifying read-only endpoint restrictions (rejects POST, PUT, PATCH, DELETE).

## Running Tests

```bash
# Run all E2E tests
docker-compose -f local.yml run --rm backend pytest read_comics/people/tests/test_e2e.py

# Run specific test class
docker-compose -f local.yml run --rm backend pytest read_comics/people/tests/test_e2e.py::TestPeopleList
```

## Related Components

- **ViewSet:** [`PersonViewSet`](../api/viewsets.md#personviewset)
- **Serializers:** [`PeopleListSerializer`](../api/serializers.md), [`PersonDetailSerializer`](../api/serializers.md)
- **Model:** [`Person`](../models.md#person)
- **Fixtures:** [Person Fixtures](fixtures.md)
