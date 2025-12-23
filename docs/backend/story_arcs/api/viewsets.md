# Story Arcs API ViewSet

## Summary

- `StoryArcsViewSet` — Read-only API with list, started (custom action), and count endpoints

## Reference

### StoryArcsViewSet

Read-only REST API ViewSet for browsing story arcs and tracking reading progress.

#### Base Classes (7 mixins + base)

| Class | Provides |
|---|---|
| `StartedActionMixin` | `/started/` endpoint showing user's in-progress story arcs |
| `CountActionMixin` | `/count/` endpoint returning total story arc count |
| `HideFinishedQuerySetMixin` | Query parameter `hide_finished=true` to filter out completed arcs |
| `FinishedQuerySetMixin` | Annotation for `finished_count` and `is_finished` fields |
| `IssuesCountQuerySetMixin` | Annotation for `issues_count` field (total issues in arc) |
| `VolumesCountQuerySetMixin` | Annotation for `volumes_count` field (distinct volumes) |
| `ListOnlyQuerySetMixin` | Disables `/detail/` endpoint — only list view available |
| `ReadOnlyModelViewSet` | Base DRF read-only viewset |

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `list_only` | List of 7 field names | Fields only available in list response (performance optimization) |
| `serializer_class` | `StoryArcsListSerializer` | Primary serializer for list responses |
| `started_serializer` | `StartedStoryArcSerializer` | Custom serializer for `/started/` endpoint |
| `filter_backends` | `[UniqueOrderingFilter]` | Custom ordering with deduplication |
| `ordering_fields` | `["name", "issues_count", "volumes_count"]` | Allowed sort columns |
| `ordering` | `["name"]` | Default sort (alphabetical by name) |

#### QuerySet

```python
queryset = StoryArc.objects.was_matched().select_related("publisher")
```

- `was_matched()` — Filters to story arcs that have been synced and linked to at least one issue
- `select_related("publisher")` — Eager-loads publisher FK to avoid N+1 queries

#### Endpoints

**List View** (`GET /api/story-arcs/`)
- Default ordering: alphabetical by name
- Supports ordering by: name, issues_count, volumes_count
- Supports filtering: `hide_finished=true` to exclude completed story arcs
- Returns: Array of `StoryArcsListSerializer` objects

**Count Endpoint** (`GET /api/story-arcs/count/`)
- Returns: `{"count": <integer>}` with total story arc count

**Started Action** (`GET /api/story-arcs/started/`)
- Returns user's story arcs with reading progress
- Serializer: `StartedStoryArcSerializer`
- Shows: slug, display_name, image, max_finished_date, finished_count, issues_count
- Sorted by recency of last finished issue

#### Fields Configuration

**list_only** fields (7 fields):
```python
[
    "slug",                    # URL slug
    "thumb_url",               # Thumbnail URL
    "name",                    # Story arc name
    "publisher__thumb_url",    # Publisher thumbnail
    "publisher__name",         # Publisher name
    "publisher__slug",         # Publisher slug
    "short_description",       # Summary text
]
```

Performance optimization: These fields are only fetched in list queries, not for detail requests (which don't exist anyway due to `ListOnlyQuerySetMixin`).

#### Features

- **No detail endpoint**: `ListOnlyQuerySetMixin` disables retrieve action (no `GET /api/story-arcs/{slug}/`)
- **Progress tracking**: `started_serializer` shows which arcs user is reading
- **Count endpoint**: Quick query for displaying total arc count in UI
- **Hide finished filter**: `hide_finished=true` query parameter hides completed arcs
- **Sorting**: Multiple sort options for browsing and searching

## Details

### Why No Detail Endpoint?

Story arcs are primarily used for:
1. Discovery/browsing (list view)
2. Progress tracking (started view)
3. Related content in other entities (character/team/issue detail pages)

A dedicated detail view would be redundant. Issue-level detail pages show which story arcs contain them.

### Finished Tracking

The `finished_count` and `is_finished` fields require user context:
- Computed from user's reading progress on related issues
- Requires authentication (not available for anonymous users)
- Via `FinishedQuerySetMixin` annotation

### Performance Optimizations

1. **select_related("publisher")** — Prevents N+1 query for publisher data
2. **list_only** fields — Prevents unnecessary field fetches
3. **Annotations** — Count fields computed at database level
4. **hide_finished filter** — Reduces result set size when enabled

### Filter Backend

`UniqueOrderingFilter` ensures ordering doesn't produce duplicate results when multiple sort fields have same values.

## References

- [serializers.md](serializers.md) — Serializer field definitions
- [../models.md](../models.md) — StoryArc model
- [../tasks.md](../tasks.md) — Background sync tasks
