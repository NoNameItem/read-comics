# Volumes API Serializers

## Summary

- `NestedVolumeSerializer` — Minimal volume reference (4 fields)
- `VolumesListSerializer` — List view with 9 fields including progress tracking
- `StartedVolumeSerializer` — User's started volumes with progress (6 fields)

## Reference

### NestedVolumeSerializer

Minimal serializer for embedding volume references in other serializers.

#### Fields

| Field Name | Type | Source | Description |
|---|---|---|---|
| `slug` | CharField | Model | URL-safe slug for linking |
| `display_name` | CharField | RO | Formatted name with year: "Name (year)" |
| `start_year` | IntegerField | Model | Year series started |
| `name` | CharField | Model | Series name |

#### Meta Configuration

- **model**: Volume
- **fields**: 4 fields listed above (read-only)

#### Usage

Used in serializers for Issue, Character, and other entities that reference volumes.

---

### VolumesListSerializer

Comprehensive list view serializer for volume browsing and discovery.

#### Fields

| Field Name | Type | Source | Description |
|---|---|---|---|
| `slug` | CharField | Model | URL-safe slug for linking |
| `image` | URLField | RO | Square medium image (from `square_medium` property) |
| `publisher` | Object | RO | Nested publisher using NestedPublisherSerializer |
| `name` | CharField | Model | Series name |
| `short_description` | TextField | Model | Short summary from ComicVine deck |
| `issues_count` | Integer | RO | Total issues in series (QuerySet annotation) |
| `finished_count` | Integer | RO | Issues user has finished (QuerySet annotation) |
| `is_finished` | Boolean | RO | Whether user finished all issues (computed) |
| `start_year` | IntegerField | Model | Year series started |

#### Field Details

- **image**: Uses `square_medium` property from ImageMixin
- **publisher**: Nested serializer with publisher details
- **issues_count**: Computed by `IssuesCountQuerySetMixin`
- **finished_count**: Computed by `FinishedQuerySetMixin` (requires user context)
- **is_finished**: Boolean computed as `finished_count >= issues_count`

#### Meta Configuration

- **model**: Volume
- **fields**: 9 fields listed above (all read-only except model fields)

---

### StartedVolumeSerializer

Lightweight serializer for user's in-progress volumes with progress tracking.

#### Fields

| Field Name | Type | Source | Description |
|---|---|---|---|
| `slug` | CharField | Model | URL-safe slug for linking |
| `display_name` | CharField | RO | Formatted display name with year |
| `image` | URLField | RO | Square medium image thumbnail |
| `max_finished_date` | DateTimeField | RO | Most recent issue completion date |
| `finished_count` | Integer | RO | Number of issues user finished |
| `issues_count` | Integer | RO | Total issues in volume |

#### Field Details

- **display_name**: "Name (year or 'Unknown')" format
- **max_finished_date**: Latest date among user's finished issues (for sorting by recency)
- **finished_count** and **issues_count**: Show progress ratio "3 of 12"

#### Meta Configuration

- **model**: Volume
- **fields**: 6 fields listed above (all read-only)

#### Usage Context

Used by `/api/volumes/started/` endpoint to show user's reading progress.

---

## Serializer Comparison

| Serializer | Use Case | Fields | Progress |
|---|---|---|---|
| NestedVolumeSerializer | Embedded references | 4 (minimal) | No |
| VolumesListSerializer | List browsing | 9 (comprehensive) | Yes (full) |
| StartedVolumeSerializer | Progress tracking | 6 (lightweight) | Yes (date + counts) |

## Details

### Computed Fields

All `RO` (read-only) fields computed at database level via QuerySet mixins:
- Annotations added by ViewSet queryset properties
- Reduces N+1 queries and improves performance
- Fields appear as model properties in serialized response

### Image Handling

Both VolumesListSerializer and StartedVolumeSerializer use `square_medium`:
- Automatically generated thumbnail from primary image
- Consistent sizing across API responses
- Lazy-loaded from ImageMixin property

### Progress Representation

**VolumesListSerializer:**
- Shows full completion status: issues_count, finished_count, is_finished
- Suitable for discovery/browsing

**StartedVolumeSerializer:**
- Shows temporal context: max_finished_date (when user last finished issue)
- Progress ratio: finished_count / issues_count
- Used for "continue reading" workflows

## References

- [viewsets.md](viewsets.md) — ViewSet configuration and mixins
- [../models.md](../models.md) — Volume model definition
- [../../publishers/api/serializers.md](../../publishers/api/serializers.md) — NestedPublisherSerializer reference
