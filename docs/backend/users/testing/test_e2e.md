# User E2E Tests in `read_comics/users/tests/test_e2e.py`

## Summary

End-to-end API tests verifying complete workflows for User endpoints including list, detail, count, and technical-info actions with various filters, ordering, pagination, and authorization scenarios.

**Pytest marks:** `pytestmark = pytest.mark.django_db`

## Test Classes

- [`TestUsersCount`](#testuserscount) - Count endpoint tests
- [`TestUsersList`](#testuserslist) - List endpoint tests
- [`TestUserDetail`](#testuserdetail) - Detail endpoint tests
- [`TestUserTechnicalInfo`](#testusertechnicalinfo) - Technical info authorization tests
- [`TestUsersParametrized`](#testusersparametrized) - Parametrized ordering tests
- [`TestUsersEdgeCases`](#testusersedgecases) - Edge case tests
- [`TestUsersConsistency`](#testusersconsistency) - Consistency tests
- [`TestUsersHTTPMethods`](#testusershttpmethods) - HTTP method validation

## Reference

### TestUsersCount

**test_count:** Verifies default count excludes users without issues.

**test_count_all:** Verifies show-all filter includes all users.

### TestUsersList

**Expected response fields:** `slug`, `image`, `name`, `short_description`, `issues_count`, `volumes_count`

**Test methods:** Covers no_show_all, show_all, data validation, default ordering, ordering by name/issues_count/volumes_count (asc/desc), invalid ordering field, pagination invalid page.

### TestUserDetail

**test_with_first_issue:** Verifies all detail fields present and accurate.

**test_no_first_issue:** Verifies behavior when users has no related issues.

**test_not_found:** Verifies 404 response for non-existent slug.

### TestUserTechnicalInfo

**Expected response fields (staff/superuser only):** `id`, `comicvine_id`, `comicvine_status`, `comicvine_last_match`, `created_dt`, `modified_dt`

**Test methods:** test_no_auth (401), test_regular_user (403), test_staff (200), test_superuser (200 with data validation).

### TestUsersParametrized

**test_ordering_parametrized:** Parametrized test for all ordering fields (name, issues_count, volumes_count) in both directions.

### TestUsersEdgeCases

Tests pagination boundaries, large page_size, response structure validation.

### TestUsersConsistency

**test_list_detail_field_consistency:** Verifies list fields exist in detail response.

**test_count_vs_list_count_consistency:** Verifies count endpoint matches list count.

### TestUsersHTTPMethods

Tests verifying read-only endpoint restrictions (rejects POST, PUT, PATCH, DELETE).

## Running Tests

```bash
# Run all E2E tests
docker-compose -f local.yml run --rm backend pytest read_comics/users/tests/test_e2e.py

# Run specific test class
docker-compose -f local.yml run --rm backend pytest read_comics/users/tests/test_e2e.py::TestUsersList
```

## Related Components

- **ViewSet:** [`UserViewSet`](../api/viewsets.md#userviewset)
- **Serializers:** [`UsersListSerializer`](../api/serializers.md), [`UserDetailSerializer`](../api/serializers.md)
- **Model:** [`User`](../models.md#user)
- **Fixtures:** [User Fixtures](fixtures.md)
