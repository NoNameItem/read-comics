# Volumes API ViewSet

## Summary

- `VolumesViewSet` — Read-only API with list, started (custom action), and count endpoints

## Reference

### VolumesViewSet

Read-only REST API ViewSet for browsing comic volumes and tracking reading progress.

#### Base Classes (7 mixins + base)

| Class | Provides |
|---|---|
| `StartedActionMixin` | `/started/` endpoint showing user's in-progress volumes |
| `CountActionMixin` | `/count/` endpoint returning total volume count |
| `HideFinishedQuerySetMixin` | Query parameter `hide_finished=true` to filter out completed volumes |
| `FinishedQuerySetMixin` | Annotation for `finished_count` and `is_finished` fields |
| `IssuesCountQuerySetMixin` | Annotation for `issues_count` field (total issues in volume) |
| `ListOnlyQuerySetMixin` | Disables `/detail/` endpoint — only list view available |
| `ReadOnlyModelViewSet` | Base DRF read-only viewset |

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `list_only` | List of 7 field names | Fields only available in list response (performance optimization) |
| `serializer_class` | `VolumesListSerializer` | Primary serializer for list responses |
| `started_serializer` | `StartedVolumeSerializer` | Custom serializer for `/started/` endpoint |
| `filter_backends` | `[UniqueOrderingFilter]` | Custom ordering with deduplication |
| `ordering_fields` | `["name", "issues_count", "start_year"]` | Allowed sort columns |
| `ordering` | `["start_year"]` | Default sort (by publication year) |

#### QuerySet

```python
queryset = Volume.objects.was_matched().select_related("publisher")
```

- `was_matched()` — Filters to volumes that have been synced and linked to at least one issue
- `select_related("publisher")` — Eager-loads publisher FK to avoid N+1 queries

#### Endpoints

**List View** (`GET /api/volumes/`)
- Default ordering: by start_year (chronological)
- Supports ordering by: name, issues_count, start_year
- Supports filtering: `hide_finished=true` to exclude completed volumes
- Returns: Array of `VolumesListSerializer` objects

**Count Endpoint** (`GET /api/volumes/count/`)
- Returns: `{"count": <integer>}` with total volume count

**Started Action** (`GET /api/volumes/started/`)
- Returns user's volumes with reading progress
- Serializer: `StartedVolumeSerializer`
- Shows: slug, display_name, image, max_finished_date, finished_count, issues_count
- Sorted by recency of last finished issue

#### Fields Configuration

**list_only** fields (7 fields):
```python
[
    "slug",                    # URL slug
    "thumb_url",               # Thumbnail URL
    "name",                    # Volume name
    "publisher__thumb_url",    # Publisher thumbnail
    "publisher__name",         # Publisher name
    "publisher__slug",         # Publisher slug
    "short_description",       # Summary text
]
```

Performance optimization: These fields only fetched in list queries, not for detail (which don't exist).

#### Features

- **No detail endpoint**: `ListOnlyQuerySetMixin` disables retrieve action
- **Progress tracking**: `started_serializer` shows which volumes user is reading
- **Count endpoint**: Quick query for displaying total volume count in UI
- **Hide finished filter**: `hide_finished=true` query parameter hides completed volumes
- **Chronological ordering**: Default sort by publication year
- **Sorting flexibility**: Can sort by name, issues_count, start_year

## Details

### Why No Detail Endpoint?

Volumes are primarily used for:
1. Discovery/browsing (list view with filtering and sorting)
2. Progress tracking (started view showing user's reading)
3. Related content in other entities (issue detail pages show volume)

A dedicated detail view would be redundant. Issue-level detail pages show which volume they belong to.

### Finished Tracking

The `finished_count` and `is_finished` fields require user context:
- Computed from user's reading progress on related issues
- Requires authentication (not available for anonymous users)
- Via `FinishedQuerySetMixin` annotation

### Performance Optimizations

1. **select_related("publisher")** — Prevents N+1 query for publisher data
2. **list_only** fields — Prevents unnecessary field fetches
3. **Annotations** — Count fields computed at database level
4. **hide_finished filter** — Reduces result set when enabled

### Default Ordering

Default sort by `start_year` (chronological publication order):
- Allows users to browse volumes chronologically
- Can be overridden with `ordering` query parameter
- Useful for understanding publication history

### Filter Backend

`UniqueOrderingFilter` ensures ordering doesn't produce duplicate results when multiple sort fields have identical values.

## References

- [serializers.md](serializers.md) — Serializer field definitions
- [../models.md](../models.md) — Volume model
- [../tasks.md](../tasks.md) — Background sync tasks
