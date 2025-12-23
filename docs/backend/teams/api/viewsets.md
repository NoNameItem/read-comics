# Teams API ViewSet

## Summary

- `TeamsViewSet` — Read-only API with list and count endpoints

## Reference

### TeamsViewSet

Read-only REST API ViewSet for browsing teams.

#### Base Classes (5 mixins + base)

| Class | Provides |
|---|---|
| `CountActionMixin` | `/count/` endpoint returning total team count |
| `OnlyWithIssuesQuerySetMixin` | Filters to teams that appear in at least one issue |
| `IssuesCountQuerySetMixin` | Annotation for `issues_count` field |
| `VolumesCountQuerySetMixin` | Annotation for `volumes_count` field |
| `ListOnlyQuerySetMixin` | Disables `/detail/` endpoint — only list view available |
| `ReadOnlyModelViewSet` | Base DRF read-only viewset |

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `list_only` | List of 7 field names | Fields only available in list response (performance optimization) |
| `serializer_class` | `TeamsListSerializer` | Primary serializer for list responses |
| `filter_backends` | `[UniqueOrderingFilter]` | Custom ordering with deduplication |
| `ordering_fields` | `["name", "issues_count", "volumes_count"]` | Allowed sort columns |
| `ordering` | `["name"]` | Default sort (alphabetical by name) |

#### QuerySet

```python
queryset = Team.objects.was_matched().select_related("publisher")
```

- `was_matched()` — Filters to teams that have been synced and linked to at least one issue
- `select_related("publisher")` — Eager-loads publisher FK to avoid N+1 queries

#### Endpoints

**List View** (`GET /api/teams/`)
- Default ordering: alphabetical by name
- Supports ordering by: name, issues_count, volumes_count
- Returns: Array of `TeamsListSerializer` objects

**Count Endpoint** (`GET /api/teams/count/`)
- Returns: `{"count": <integer>}` with total team count

#### Fields Configuration

**list_only** fields (7 fields):
```python
[
    "slug",                    # URL slug
    "thumb_url",               # Thumbnail URL
    "name",                    # Team name
    "publisher__thumb_url",    # Publisher thumbnail
    "publisher__name",         # Publisher name
    "publisher__slug",         # Publisher slug
    "short_description",       # Summary text
]
```

Performance optimization: These fields are only fetched in list queries, not for detail requests (which don't exist due to `ListOnlyQuerySetMixin`).

#### Features

- **No detail endpoint**: `ListOnlyQuerySetMixin` disables retrieve action
- **Count endpoint**: Quick query for displaying total team count in UI
- **Sorting**: Multiple sort options for browsing
- **Publisher filtering**: Teams grouped by publisher in queries

## References

- [serializers.md](serializers.md) — Serializer field definitions
- [../models.md](../models.md) — Team model
- [../tasks.md](../tasks.md) — Background sync tasks
