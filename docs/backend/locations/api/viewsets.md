# Locations ViewSet

## Summary

- [`LocationViewSet`](#locationviewset) — Read-only viewset for locations with counting and filtering by related issues/volumes

## Reference

### `LocationViewSet`

Read-only REST API viewset for browsing comic locations with filtering and aggregated counting.

**Base Classes:**

1. `DetailSerializerMixin` — Uses separate serializer for detail endpoint
2. `TechnicalInfoActionMixin` — Adds `tech-info` action for admin metadata
3. `CountActionMixin` — Adds `count` action for total count
4. `OnlyWithIssuesQuerySetMixin` — Filters to locations with at least one issue
5. `IssuesCountQuerySetMixin` — Adds `issues_count` annotation
6. `VolumesCountQuerySetMixin` — Adds `volumes_count` annotation
7. `ListOnlyQuerySetMixin` — Restricts list endpoint to selected fields
8. `ReadOnlyModelViewSet` — Base DRF viewset (list, retrieve only)

**Configuration:**

- `serializer_class = LocationsListSerializer` — For list endpoint
- `serializer_detail_class = LocationDetailSerializer` — For detail endpoint
- `serializer_tech_info_class = ConceptTechnicalInfoSerializer` — For tech-info action
- `lookup_field = "slug"` — Use slug instead of pk for routing
- `list_only = ["slug", "thumb_url", "name", "short_description"]` — Fields selected for list
- `ordering_fields` — `["name", "issues_count", "volumes_count"]`
- `ordering` — Default sort by name (alphabetical)
- `filter_backends = [UniqueOrderingFilter]` — Consistent pagination across sort changes

**QuerySet:**

Returns `Location.objects.was_matched()` — only ComicVine-matched locations.

**QuerySet Mixins:**

- `OnlyWithIssuesQuerySetMixin` — Ensures location has at least one linked issue
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
| GET | `/locations/` | list | LocationsListSerializer |
| GET | `/locations/{slug}/` | retrieve | LocationDetailSerializer |
| GET | `/locations/count/` | count | (returns `{"count": int}`) |
| GET | `/locations/{slug}/tech-info/` | tech_info | ConceptTechnicalInfoSerializer |