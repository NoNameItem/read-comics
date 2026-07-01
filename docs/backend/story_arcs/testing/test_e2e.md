# StoryArc E2E Tests in `read_comics/story_arcs/tests/test_e2e.py`

## Summary

End-to-end API tests verifying complete workflows for StoryArc endpoints including list, detail, count, and technical-info actions with various filters, ordering, pagination, and authorization scenarios.

**Pytest marks:** `pytestmark = pytest.mark.django_db`

## Test Classes

- [`TestStoryArcsCount`](#teststoryarcscount) - Count endpoint tests
- [`TestStoryArcsList`](#teststoryarcslist) - List endpoint tests
- [`TestStoryArcDetail`](#teststoryarcdetail) - Detail endpoint tests
- [`TestStoryArcTechnicalInfo`](#teststoryarctechnicalinfo) - Technical info authorization tests
- [`TestStoryArcsParametrized`](#teststoryarcsparametrized) - Parametrized ordering tests
- [`TestStoryArcsEdgeCases`](#teststoryarcsedgecases) - Edge case tests
- [`TestStoryArcsConsistency`](#teststoryarcsconsistency) - Consistency tests
- [`TestStoryArcsHTTPMethods`](#teststoryarcshttpmethods) - HTTP method validation

## Reference

### TestStoryArcsCount

**test_count:** Verifies default count excludes story_arcs without issues.

**test_count_all:** Verifies show-all filter includes all story_arcs.

### TestStoryArcsList

**Expected response fields:** `slug`, `image`, `name`, `short_description`, `issues_count`, `volumes_count`

**Test methods:** Covers no_show_all, show_all, data validation, default ordering, ordering by name/issues_count/volumes_count (asc/desc), invalid ordering field, pagination invalid page.

### TestStoryArcDetail

**test_with_first_issue:** Verifies all detail fields present and accurate.

**test_no_first_issue:** Verifies behavior when story_arcs has no related issues.

**test_not_found:** Verifies 404 response for non-existent slug.

### TestStoryArcTechnicalInfo

**Expected response fields (staff/superuser only):** `id`, `comicvine_id`, `comicvine_status`, `comicvine_last_match`, `created_dt`, `modified_dt`

**Test methods:** test_no_auth (401), test_regular_user (403), test_staff (200), test_superuser (200 with data validation).

### TestStoryArcsParametrized

**test_ordering_parametrized:** Parametrized test for all ordering fields (name, issues_count, volumes_count) in both directions.

### TestStoryArcsEdgeCases

Tests pagination boundaries, large page_size, response structure validation.

### TestStoryArcsConsistency

**test_list_detail_field_consistency:** Verifies list fields exist in detail response.

**test_count_vs_list_count_consistency:** Verifies count endpoint matches list count.

### TestStoryArcsHTTPMethods

Tests verifying read-only endpoint restrictions (rejects POST, PUT, PATCH, DELETE).

## Running Tests

```bash
# Run all E2E tests
docker-compose -f local.yml run --rm backend pytest read_comics/story_arcs/tests/test_e2e.py

# Run specific test class
docker-compose -f local.yml run --rm backend pytest read_comics/story_arcs/tests/test_e2e.py::TestStoryArcsList
```

## Related Components

- **ViewSet:** [`StoryArcViewSet`](../api/viewsets.md#storyarcviewset)
- **Serializers:** [`StoryArcsListSerializer`](../api/serializers.md), [`StoryArcDetailSerializer`](../api/serializers.md)
- **Model:** [`StoryArc`](../models.md#storyarc)
- **Fixtures:** [StoryArc Fixtures](fixtures.md)
