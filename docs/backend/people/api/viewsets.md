# People ViewSet

## Summary

- **`PeopleViewSet`** — Read-only ViewSet with list endpoint, aggregated counts, and ComicVine filtering

## Reference

### PeopleViewSet

Read-only ViewSet for browsing creators/contributors with aggregated issue and volume counts.

**Base Classes** (in order):
1. `CountActionMixin` — Adds `/count/` endpoint for total count
2. `OnlyWithIssuesQuerySetMixin` — Filters to exclude persons without issues
3. `IssuesCountQuerySetMixin` — Annotates each person with aggregated issue count
4. `VolumesCountQuerySetMixin` — Annotates each person with aggregated volume count
5. `ListOnlyQuerySetMixin` — Disables detail endpoint (no `/people/{slug}/`)
6. `ReadOnlyModelViewSet` — DRF base with list/retrieve actions (retrieve disabled by ListOnlyQuerySetMixin)

**Configuration**:
- **Serializer**: `PeopleListSerializer`
- **Queryset**: `Person.objects.was_matched()` (ComicVine-synced persons only)
- **Filtering**: `UniqueOrderingFilter`
- **Ordering fields**: `name`, `issues_count`, `volumes_count`
- **Default ordering**: `name` (alphabetical)
- **List-only fields**: `slug`, `thumb_url`, `name`, `short_description`

#### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/people/` | List all creators with counts (paginated) |
| `GET` | `/api/people/count/` | Total count of creators |

#### Design Notes

- **List-only API** — No separate detail endpoint; retrieve action is disabled via `ListOnlyQuerySetMixin`
- **ComicVine filtering** — QuerySet limited to `was_matched()` persons (persons that have been synced from ComicVine API)
- **Aggregated counts** — Issues and volumes counts are computed per-person by QuerySet mixins, not stored in database
- **Ordering options** — Clients can sort by name, issues_count, or volumes_count via query parameter