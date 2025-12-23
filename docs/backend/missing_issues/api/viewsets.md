# Missing Issues ViewSet

## Summary

- **`MissingIssueViewSet`** — Read-only ViewSet with count endpoint for missing issues

## Reference

### MissingIssueViewSet

Read-only ViewSet for accessing missing issue records (filtered to exclude skipped issues).

**Base Classes**:
1. `CountActionMixin` — Adds `/count/` endpoint for total count
2. `ReadOnlyModelViewSet` — DRF base (list/retrieve not fully implemented)

**Configuration**:
- **Model**: `MissingIssue`
- **Queryset**: `MissingIssue.objects.filter(skip=False)` (excludes skipped issues)
- **Default serializer**: Auto-generated ModelSerializer (no explicit serializer defined)

#### Implemented Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/missing-issues/count/` | Total count of non-skipped missing issues |

#### Design Notes

- **Skip filtering** — Only counts/accesses issues with `skip=False`
- **Count endpoint** — Primary implemented endpoint via `CountActionMixin`
- **Auto-generated serialization** — Uses DRF's default ModelSerializer with MissingIssue fields