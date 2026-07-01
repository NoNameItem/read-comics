# Publisher E2E Tests in `read_comics/publishers/tests/test_e2e.py`

## Summary

End-to-end API tests verifying complete workflows for Publisher endpoints including list, detail, count, and technical-info actions with various filters, ordering, pagination, and authorization scenarios.

**Pytest marks:** `pytestmark = pytest.mark.django_db`

## Test Classes

- [`TestPublishersCount`](#testpublisherscount) - Count endpoint tests
- [`TestPublishersList`](#testpublisherslist) - List endpoint tests
- [`TestPublisherDetail`](#testpublisherdetail) - Detail endpoint tests
- [`TestPublisherTechnicalInfo`](#testpublishertechnicalinfo) - Technical info authorization tests
- [`TestPublishersParametrized`](#testpublishersparametrized) - Parametrized ordering tests
- [`TestPublishersEdgeCases`](#testpublishersedgecases) - Edge case tests
- [`TestPublishersConsistency`](#testpublishersconsistency) - Consistency tests
- [`TestPublishersHTTPMethods`](#testpublishershttpmethods) - HTTP method validation

## Reference

### TestPublishersCount

**test_count:** Verifies default count excludes publishers without issues.

**test_count_all:** Verifies show-all filter includes all publishers.

### TestPublishersList

**Expected response fields:** `slug`, `image`, `name`, `short_description`, `issues_count`, `volumes_count`

**Test methods:** Covers no_show_all, show_all, data validation, default ordering, ordering by name/issues_count/volumes_count (asc/desc), invalid ordering field, pagination invalid page.

### TestPublisherDetail

**test_with_first_issue:** Verifies all detail fields present and accurate.

**test_no_first_issue:** Verifies behavior when publishers has no related issues.

**test_not_found:** Verifies 404 response for non-existent slug.

### TestPublisherTechnicalInfo

**Expected response fields (staff/superuser only):** `id`, `comicvine_id`, `comicvine_status`, `comicvine_last_match`, `created_dt`, `modified_dt`

**Test methods:** test_no_auth (401), test_regular_user (403), test_staff (200), test_superuser (200 with data validation).

### TestPublishersParametrized

**test_ordering_parametrized:** Parametrized test for all ordering fields (name, issues_count, volumes_count) in both directions.

### TestPublishersEdgeCases

Tests pagination boundaries, large page_size, response structure validation.

### TestPublishersConsistency

**test_list_detail_field_consistency:** Verifies list fields exist in detail response.

**test_count_vs_list_count_consistency:** Verifies count endpoint matches list count.

### TestPublishersHTTPMethods

Tests verifying read-only endpoint restrictions (rejects POST, PUT, PATCH, DELETE).

## Running Tests

```bash
# Run all E2E tests
docker-compose -f local.yml run --rm backend pytest read_comics/publishers/tests/test_e2e.py

# Run specific test class
docker-compose -f local.yml run --rm backend pytest read_comics/publishers/tests/test_e2e.py::TestPublishersList
```

## Related Components

- **ViewSet:** [`PublisherViewSet`](../api/viewsets.md#publisherviewset)
- **Serializers:** [`PublishersListSerializer`](../api/serializers.md), [`PublisherDetailSerializer`](../api/serializers.md)
- **Model:** [`Publisher`](../models.md#publisher)
- **Fixtures:** [Publisher Fixtures](fixtures.md)
