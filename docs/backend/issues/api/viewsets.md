# Issues ViewSet

## Summary

- [`IssueViewSet`](#issueviewset) — Read-only viewset for issues with filtering, ordering, navigation, and finished tracking

## Reference

### `IssueViewSet`

Read-only REST API viewset for browsing comic issues with pagination, filtering, and user progress tracking.

**Base Classes:**

1. `DetailSerializerMixin` — Uses separate serializer for detail endpoint
2. `TechnicalInfoActionMixin` — Adds `tech-info` action for admin metadata
3. `CountActionMixin` — Adds `count` action for total count
4. `ReadOnlyModelViewSet` — Base DRF viewset (list, retrieve only)

**Configuration:**

- `serializer_class = IssuesListSerializer` — For list endpoint
- `serializer_detail_class = IssueDetailSerializer` — For detail endpoint
- `serializer_tech_info_class = IssueTechnicalInfoSerializer` — For tech-info action
- `lookup_field = "slug"` — Use slug instead of pk for routing
- `ordering_fields` — `["volume__name", "volume__start_year", "numerical_number", "number", "cover_date"]`
- `ordering` — Default sort order (by cover_date, volume, number)
- `filter_backends = [UniqueOrderingFilter]` — Consistent pagination across sort changes

**QuerySet:**

Returns `Issue.objects.was_matched().select_related("volume", "volume__publisher")` — only ComicVine-matched issues with optimized queries.

**List-Only Fields:**

For list endpoint, only these fields are selected from database (performance optimization):
- `slug`, `image_url`, `thumb_url`
- `volume__publisher__name`, `volume__publisher__slug`, `volume__publisher__thumb_url`
- `volume_id`, `volume__name`, `volume__start_year`, `volume__slug`
- `number`, `name`, `short_description`, `cover_date`

**Filtering & Sorting:**

- Uses `UniqueOrderingFilter` for consistent pagination
- Default sort: by cover_date, then volume name, year, number
- Supports `?hide-finished=yes|no` to filter finished issues (default: hide finished)

**User Progress Tracking:**

In `get_queryset()`:
- Annotates `finished_flg` for authenticated users (count of finished instances: 0 or 1)
- Unauthenticated users get `finished_flg=None`
- List endpoint hides finished issues by default (`?hide-finished=yes`)

**Navigation (Previous/Next Issue):**

For detail endpoint, computes previous/next issue slugs based on current sorting:

- `get_serializer_context()` — Adds navigation and position context
- `get_orderings()` — Extracts active orderings from filter backend
- `get_next_issue_slug(instance)` → slug of next issue in sort order
- `get_prev_issue_slug(instance)` → slug of previous issue in sort order
- `get_number_in_sublist(instance)` → position in current sort (1-indexed)

These handle multi-field ordering correctly (e.g., volume name, then number).

**Endpoints:**

| Method | URL | Action | Serializer |
|--------|-----|--------|-----------|
| GET | `/issues/` | list | IssuesListSerializer |
| GET | `/issues/{slug}/` | retrieve | IssueDetailSerializer |
| GET | `/issues/count/` | count | (returns `{"count": int}`) |
| GET | `/issues/{slug}/tech-info/` | tech_info | IssueTechnicalInfoSerializer |