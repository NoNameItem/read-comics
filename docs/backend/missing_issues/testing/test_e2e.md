# MissingIssue E2E Tests in `read_comics/missing_issues/tests/test_e2e.py`

## Summary

End-to-end API tests verifying complete workflows for MissingIssue endpoints including list, detail, count, and technical-info actions with various filters, ordering, pagination, and authorization scenarios.

**Pytest marks:** `pytestmark = pytest.mark.django_db`

## Test Classes

- [`TestMissingIssuesCount`](#testmissingissuescount) - Count endpoint tests
- [`TestMissingIssuesList`](#testmissingissueslist) - List endpoint tests
- [`TestMissingIssueDetail`](#testmissingissuedetail) - Detail endpoint tests
- [`TestMissingIssueTechnicalInfo`](#testmissingissuetechnicalinfo) - Technical info authorization tests
- [`TestMissingIssuesParametrized`](#testmissingissuesparametrized) - Parametrized ordering tests
- [`TestMissingIssuesEdgeCases`](#testmissingissuesedgecases) - Edge case tests
- [`TestMissingIssuesConsistency`](#testmissingissuesconsistency) - Consistency tests
- [`TestMissingIssuesHTTPMethods`](#testmissingissueshttpmethods) - HTTP method validation

## Reference

### TestMissingIssuesCount

**test_count:** Verifies default count excludes missing_issues without issues.

**test_count_all:** Verifies show-all filter includes all missing_issues.

### TestMissingIssuesList

**Expected response fields:** `slug`, `image`, `name`, `short_description`, `issues_count`, `volumes_count`

**Test methods:** Covers no_show_all, show_all, data validation, default ordering, ordering by name/issues_count/volumes_count (asc/desc), invalid ordering field, pagination invalid page.

### TestMissingIssueDetail

**test_with_first_issue:** Verifies all detail fields present and accurate.

**test_no_first_issue:** Verifies behavior when missing_issues has no related issues.

**test_not_found:** Verifies 404 response for non-existent slug.

### TestMissingIssueTechnicalInfo

**Expected response fields (staff/superuser only):** `id`, `comicvine_id`, `comicvine_status`, `comicvine_last_match`, `created_dt`, `modified_dt`

**Test methods:** test_no_auth (401), test_regular_user (403), test_staff (200), test_superuser (200 with data validation).

### TestMissingIssuesParametrized

**test_ordering_parametrized:** Parametrized test for all ordering fields (name, issues_count, volumes_count) in both directions.

### TestMissingIssuesEdgeCases

Tests pagination boundaries, large page_size, response structure validation.

### TestMissingIssuesConsistency

**test_list_detail_field_consistency:** Verifies list fields exist in detail response.

**test_count_vs_list_count_consistency:** Verifies count endpoint matches list count.

### TestMissingIssuesHTTPMethods

Tests verifying read-only endpoint restrictions (rejects POST, PUT, PATCH, DELETE).

## Running Tests

```bash
# Run all E2E tests
docker-compose -f local.yml run --rm backend pytest read_comics/missing_issues/tests/test_e2e.py

# Run specific test class
docker-compose -f local.yml run --rm backend pytest read_comics/missing_issues/tests/test_e2e.py::TestMissingIssuesList
```

## Related Components

- **ViewSet:** [`MissingIssueViewSet`](../api/viewsets.md#missingissueviewset)
- **Serializers:** [`MissingIssuesListSerializer`](../api/serializers.md), [`MissingIssueDetailSerializer`](../api/serializers.md)
- **Model:** [`MissingIssue`](../models.md#missingissue)
- **Fixtures:** [MissingIssue Fixtures](fixtures.md)
