# Team E2E Tests in `read_comics/teams/tests/test_e2e.py`

## Summary

End-to-end API tests verifying complete workflows for Team endpoints including list, detail, count, and technical-info actions with various filters, ordering, pagination, and authorization scenarios.

**Pytest marks:** `pytestmark = pytest.mark.django_db`

## Test Classes

- [`TestTeamsCount`](#testteamscount) - Count endpoint tests
- [`TestTeamsList`](#testteamslist) - List endpoint tests
- [`TestTeamDetail`](#testteamdetail) - Detail endpoint tests
- [`TestTeamTechnicalInfo`](#testteamtechnicalinfo) - Technical info authorization tests
- [`TestTeamsParametrized`](#testteamsparametrized) - Parametrized ordering tests
- [`TestTeamsEdgeCases`](#testteamsedgecases) - Edge case tests
- [`TestTeamsConsistency`](#testteamsconsistency) - Consistency tests
- [`TestTeamsHTTPMethods`](#testteamshttpmethods) - HTTP method validation

## Reference

### TestTeamsCount

**test_count:** Verifies default count excludes teams without issues.

**test_count_all:** Verifies show-all filter includes all teams.

### TestTeamsList

**Expected response fields:** `slug`, `image`, `name`, `short_description`, `issues_count`, `volumes_count`

**Test methods:** Covers no_show_all, show_all, data validation, default ordering, ordering by name/issues_count/volumes_count (asc/desc), invalid ordering field, pagination invalid page.

### TestTeamDetail

**test_with_first_issue:** Verifies all detail fields present and accurate.

**test_no_first_issue:** Verifies behavior when teams has no related issues.

**test_not_found:** Verifies 404 response for non-existent slug.

### TestTeamTechnicalInfo

**Expected response fields (staff/superuser only):** `id`, `comicvine_id`, `comicvine_status`, `comicvine_last_match`, `created_dt`, `modified_dt`

**Test methods:** test_no_auth (401), test_regular_user (403), test_staff (200), test_superuser (200 with data validation).

### TestTeamsParametrized

**test_ordering_parametrized:** Parametrized test for all ordering fields (name, issues_count, volumes_count) in both directions.

### TestTeamsEdgeCases

Tests pagination boundaries, large page_size, response structure validation.

### TestTeamsConsistency

**test_list_detail_field_consistency:** Verifies list fields exist in detail response.

**test_count_vs_list_count_consistency:** Verifies count endpoint matches list count.

### TestTeamsHTTPMethods

Tests verifying read-only endpoint restrictions (rejects POST, PUT, PATCH, DELETE).

## Running Tests

```bash
# Run all E2E tests
docker-compose -f local.yml run --rm backend pytest read_comics/teams/tests/test_e2e.py

# Run specific test class
docker-compose -f local.yml run --rm backend pytest read_comics/teams/tests/test_e2e.py::TestTeamsList
```

## Related Components

- **ViewSet:** [`TeamViewSet`](../api/viewsets.md#teamviewset)
- **Serializers:** [`TeamsListSerializer`](../api/serializers.md), [`TeamDetailSerializer`](../api/serializers.md)
- **Model:** [`Team`](../models.md#team)
- **Fixtures:** [Team Fixtures](fixtures.md)
