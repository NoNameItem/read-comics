# Objects Serializers

## Summary

- [`ObjectsListSerializer`](#objectslistserializer) — Compact fields for list endpoint with issue/volume counts

## Reference

### `ObjectsListSerializer`

Compact representation for list endpoint, optimized for bulk rendering with aggregated counts.

**Fields:**

| Field | Source | Type | Description |
|-------|--------|------|-------------|
| `slug` | Object.slug | str | Unique identifier for routing |
| `image` | Object.square_medium | str | Square thumbnail image URL |
| `name` | Object.name | str | Object/artifact name |
| `short_description` | Object.short_description | str | Brief summary |
| `issues_count` | computed | int | Count of issues featuring this object |
| `volumes_count` | computed | int | Count of volumes featuring this object |

**Computed Fields (via QuerySet mixins):**

- `issues_count` — Aggregated from IssuesCountQuerySetMixin
- `volumes_count` — Aggregated from VolumesCountQuerySetMixin
