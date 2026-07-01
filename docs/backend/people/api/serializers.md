# People Serializers

## Summary

- **`PeopleListSerializer`** — List response serializer with name, images, and aggregated counts

## Reference

### PeopleListSerializer

Serializer for people list endpoint responses.

**Model**: `Person`

**Read-only fields**:
- `issues_count` — Aggregated count of issues featuring this person (computed by QuerySet mixin)
- `volumes_count` — Aggregated count of volumes featuring this person (computed by QuerySet mixin)
- `image` — Maps to `square_medium` property (from ImageMixin)

| Field | Type | Source |
|-------|------|--------|
| `slug` | CharField | Model field |
| `image` | CharField (RO) | `square_medium` property |
| `name` | TextField | Model field |
| `short_description` | TextField | Model field |
| `issues_count` | IntegerField (RO) | QuerySet annotation |
| `volumes_count` | IntegerField (RO) | QuerySet annotation |

#### Design Notes

- **List-only API** — No separate detail serializer; `PeopleViewSet` uses `ListOnlyQuerySetMixin` to exclude detail endpoint
- **Computed counts** — `issues_count` and `volumes_count` are not stored fields but computed by `IssuesCountQuerySetMixin` and `VolumesCountQuerySetMixin`
- **Image handling** — Uses `square_medium` property from `ImageMixin` for responsive thumbnails