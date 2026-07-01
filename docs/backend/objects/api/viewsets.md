# Objects ViewSet

## Summary

- [`ObjectViewSet`](#objectviewset) — Read-only viewset for objects with counting and filtering by related issues/volumes

## Reference

### `ObjectViewSet`

Read-only REST API viewset for browsing comic objects/artifacts with filtering and aggregated counting. Note: List-only endpoint (no separate detail view).

**Base Classes:**

1. `CountActionMixin` — Adds `count` action for total count
2. `OnlyWithIssuesQuerySetMixin` — Filters to objects with at least one issue
3. `IssuesCountQuerySetMixin` — Adds `issues_count` annotation
4. `VolumesCountQuerySetMixin` — Adds `volumes_count` annotation
5. `ListOnlyQuerySetMixin` — Restricts list endpoint to selected fields
6. `ReadOnlyModelViewSet` — Base DRF viewset (list, retrieve only)

**Configuration:**

- `serializer_class = ObjectsListSerializer` — For list endpoint
- `list_only = ["slug", "thumb_url", "name", "short_description"]` — Fields selected for list
- `ordering_fields` — `["name", "issues_count", "volumes_count"]`
- `ordering` — Default sort by name (alphabetical)
- `filter_backends = [UniqueOrderingFilter]` — Consistent pagination across sort changes

**QuerySet:**

Returns `Object.objects.was_matched()` — only ComicVine-matched objects.

**QuerySet Mixins:**

- `OnlyWithIssuesQuerySetMixin` — Ensures object has at least one linked issue
- `IssuesCountQuerySetMixin` — Adds `issues_count` aggregation
- `VolumesCountQuerySetMixin` — Adds `volumes_count` aggregation
- `ListOnlyQuerySetMixin` — Restricts fields on list endpoint for performance

**Filtering & Sorting:**

- Uses `UniqueOrderingFilter` for consistent pagination
- Default sort: alphabetical by name
- Supports sorting by `name`, `issues_count`, or `volumes_count`

**Endpoints:**

| Method | URL | Action | Serializer |
|--------|-----|--------|-----------|
| GET | `/objects/` | list | ObjectsListSerializer |
| GET | `/objects/count/` | count | (returns `{"count": int}`) |

**Note:** No detail endpoint (retrieve) — Objects only expose list view via API.
