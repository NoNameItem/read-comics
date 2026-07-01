# Concept ViewSet

## Summary

- [`ConceptViewSet`](#conceptviewset) — Read-only ViewSet for managing Concept resources with aggregated counts, technical info, and list-only filtering

## Reference

### `ConceptViewSet`

**Base Classes:** `DetailSerializerMixin`, `TechnicalInfoActionMixin`, `CountActionMixin`, `OnlyWithIssuesQuerySetMixin`, `IssuesCountQuerySetMixin`, `VolumesCountQuerySetMixin`, `ListOnlyQuerySetMixin`, `ReadOnlyModelViewSet`

**Configuration:**

| Property | Value | Purpose |
|----------|-------|---------|
| `serializer_class` | `ConceptsListSerializer` | Default serializer for list action |
| `serializer_detail_class` | `ConceptDetailSerializer` | Serializer for retrieve action |
| `serializer_tech_info_class` | `ConceptTechnicalInfoSerializer` | Serializer for technical-info action |
| `filter_backends` | `[UniqueOrderingFilter]` | Stable ordering with tie-breaking by ID |
| `ordering_fields` | `["name", "issues_count", "volumes_count"]` | Available sorting fields |
| `ordering` | `["name"]` | Default sort order (alphabetical) |
| `lookup_field` | `"slug"` | URL parameter for detail lookup |
| `lookup_url_kwarg` | `"slug"` | URL kwarg name |
| `list_only` | `["slug", "thumb_url", "name", "short_description"]` | Fields exposed in list action |

**QuerySet:**

Returns `Concept.objects.was_matched()` — only concepts successfully synced with ComicVine.

**Mixins:**

- **DetailSerializerMixin** — Switches between `ConceptsListSerializer` (list) and `ConceptDetailSerializer` (retrieve)
- **TechnicalInfoActionMixin** — Adds `/technical-info/` action for staff, returns `ConceptTechnicalInfoSerializer`
- **CountActionMixin** — Adds `/count/` action returning `{"count": <number>}`
- **OnlyWithIssuesQuerySetMixin** — Filters to concepts with matched issues; `?show-all=yes` includes empty
- **IssuesCountQuerySetMixin** — Annotates issue count aggregation
- **VolumesCountQuerySetMixin** — Annotates volume count aggregation
- **ListOnlyQuerySetMixin** — Limits list action fields to slug, thumb_url, name, short_description