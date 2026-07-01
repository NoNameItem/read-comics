# Issue E2E Tests in `read_comics/issues/tests/test_e2e.py`

## Summary

End-to-end API tests verifying complete workflows for Issue endpoints including list, detail, count, and technical-info actions with various filters, ordering, pagination, and authorization scenarios.

**Pytest marks:** `pytestmark = pytest.mark.django_db`

## Test Classes

- [`TestIssuesCount`](#testissuescount) - Count endpoint tests
- [`TestIssuesList`](#testissueslist) - List endpoint tests
- [`TestIssueDetail`](#testissuedetail) - Detail endpoint tests
- [`TestIssueTechnicalInfo`](#testissuetechnicalinfo) - Technical info authorization tests
- [`TestIssuesParametrized`](#testissuesparametrized) - Parametrized ordering tests
- [`TestIssuesEdgeCases`](#testissuesedgecases) - Edge case tests
- [`TestIssuesConsistency`](#testissuesconsistency) - Consistency tests
- [`TestIssuesHTTPMethods`](#testissueshttpmethods) - HTTP method validation

## Reference

### TestIssuesCount

**test_count:** Verifies default count excludes issues without issues.

**test_count_all:** Verifies show-all filter includes all issues.

### TestIssuesList

**Expected response fields:** `slug`, `image`, `name`, `short_description`, `issues_count`, `volumes_count`

**Test methods:** Covers no_show_all, show_all, data validation, default ordering, ordering by name/issues_count/volumes_count (asc/desc), invalid ordering field, pagination invalid page.

### TestIssueDetail

**test_with_first_issue:** Verifies all detail fields present and accurate.

**test_no_first_issue:** Verifies behavior when issues has no related issues.

**test_not_found:** Verifies 404 response for non-existent slug.

### TestIssueTechnicalInfo

**Expected response fields (staff/superuser only):** `id`, `comicvine_id`, `comicvine_status`, `comicvine_last_match`, `created_dt`, `modified_dt`

**Test methods:** test_no_auth (401), test_regular_user (403), test_staff (200), test_superuser (200 with data validation).

### TestIssuesParametrized

**test_ordering_parametrized:** Parametrized test for all ordering fields (name, issues_count, volumes_count) in both directions.

### TestIssuesEdgeCases

Tests pagination boundaries, large page_size, response structure validation.

### TestIssuesConsistency

**test_list_detail_field_consistency:** Verifies list fields exist in detail response.

**test_count_vs_list_count_consistency:** Verifies count endpoint matches list count.

### TestIssuesHTTPMethods

Tests verifying read-only endpoint restrictions (rejects POST, PUT, PATCH, DELETE).

## Running Tests

```bash
# Run all E2E tests
docker-compose -f local.yml run --rm backend pytest read_comics/issues/tests/test_e2e.py

# Run specific test class
docker-compose -f local.yml run --rm backend pytest read_comics/issues/tests/test_e2e.py::TestIssuesList
```

## Related Components

- **ViewSet:** [`IssueViewSet`](../api/viewsets.md#issueviewset)
- **Serializers:** [`IssuesListSerializer`](../api/serializers.md), [`IssueDetailSerializer`](../api/serializers.md)
- **Model:** [`Issue`](../models.md#issue)
- **Fixtures:** [Issue Fixtures](fixtures.md)
