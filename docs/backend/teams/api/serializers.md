# Teams API Serializers

## Summary

- `TeamsListSerializer` — List view serializer with 7 fields including computed counts

## Reference

### TeamsListSerializer

List view serializer for team browsing and search.

#### Fields

| Field Name | Type | Source | Description |
|---|---|---|---|
| `slug` | CharField | Model | URL-safe slug for linking |
| `image` | URLField | RO | Square medium image (from `square_medium` property) |
| `publisher` | Object | RO | Nested publisher object using NestedPublisherSerializer |
| `name` | CharField | Model | Team name |
| `short_description` | TextField | Model | Short summary from ComicVine deck |
| `issues_count` | Integer | RO | Number of issues featuring this team (QuerySet annotation) |
| `volumes_count` | Integer | RO | Number of distinct volumes containing team (QuerySet annotation) |

#### Field Details

- **image**: Uses `square_medium` property from ImageMixin. Provides consistent sizing for list displays.
- **publisher**: Nested serializer showing publisher reference with basic fields.
- **issues_count**: Computed by `IssuesCountQuerySetMixin` annotation on QuerySet.
- **volumes_count**: Computed by `VolumesCountQuerySetMixin` annotation.

#### Meta Configuration

- **model**: Team
- **fields**: 7 fields listed above (all read-only)

## Details

### List-Only Design

Teams API provides only list view (no detail endpoint):
- Teams are typically viewed in context of issues/volumes
- Browsing mode for discovering and searching teams
- Issue-level detail pages show related teams

## References

- [viewsets.md](viewsets.md) — ViewSet configuration and mixins
- [../models.md](../models.md) — Team model definition
- [../../publishers/api/serializers.md](../../publishers/api/serializers.md) — NestedPublisherSerializer reference
