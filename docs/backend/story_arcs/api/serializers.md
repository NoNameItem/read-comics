# Story Arcs API Serializers

## Summary

- `StoryArcsListSerializer` — List view serializer with 9 fields including computed counts
- `StartedStoryArcSerializer` — Custom serializer for user's started story arcs (progress tracking)

## Reference

### StoryArcsListSerializer

List view serializer for story arc browsing and search.

#### Fields

| Field Name | Type | Source | Description |
|---|---|---|---|
| `slug` | CharField | Model | URL-safe slug for linking |
| `image` | URLField | RO | Square medium image (from `square_medium` property) |
| `publisher` | Object | RO | Nested publisher object using NestedPublisherSerializer |
| `name` | CharField | Model | Story arc name |
| `short_description` | TextField | Model | Short summary from ComicVine deck |
| `issues_count` | Integer | RO | Number of issues in this arc (QuerySet annotation) |
| `finished_count` | Integer | RO | Number of issues user has finished reading |
| `volumes_count` | Integer | RO | Number of distinct volumes covered by arc |
| `is_finished` | Boolean | RO | Whether user has finished all issues in arc |

#### Field Details

- **image**: Uses `square_medium` property from ImageMixin. Provides consistent sizing for list displays.
- **publisher**: Nested serializer showing publisher reference with basic fields.
- **issues_count**: Computed by `IssuesCountQuerySetMixin` annotation on QuerySet.
- **finished_count**: Computed by `FinishedQuerySetMixin` annotation (requires user context from request).
- **volumes_count**: Computed by `VolumesCountQuerySetMixin` annotation.
- **is_finished**: Computed boolean indicating if `finished_count >= issues_count`.

#### Meta Configuration

- **model**: StoryArc
- **fields**: 9 fields listed above (all read-only)

---

### StartedStoryArcSerializer

Specialized serializer for story arcs that a user has started reading (partial progress).

#### Fields

| Field Name | Type | Source | Description |
|---|---|---|---|
| `slug` | CharField | Model | URL-safe slug for linking |
| `display_name` | CharField | RO | Story arc name (or "Publisher Name - Story Arc Name" if has publisher) |
| `image` | URLField | RO | Square medium image (from `square_medium` property) |
| `max_finished_date` | DateTimeField | RO | Date user finished most recent issue in arc |
| `finished_count` | Integer | RO | Number of issues user has finished |
| `issues_count` | Integer | RO | Total number of issues in arc |

#### Field Details

- **display_name**: Enhanced display name including publisher context if available.
- **max_finished_date**: Latest completion date among all issues (used for sorting by recency).
- **finished_count** and **issues_count**: Show progress ratio for UI display (e.g., "3 of 5").

#### Meta Configuration

- **model**: StoryArc
- **fields**: 6 fields listed above (all read-only)

#### Usage Context

Used by `/api/story-arcs/started/` endpoint to show user's reading progress across multiple story arcs.

## Details

### List vs Started Serializers

**StoryArcsListSerializer** (for `/api/story-arcs/`):
- Comprehensive listing with all story arc metadata
- Shows volumes_count and full completion status
- Used for story arc discovery/browsing

**StartedStoryArcSerializer** (for `/api/story-arcs/started/`):
- Lightweight progress tracking
- Emphasizes temporal context (when user started/finished)
- Used for "continue reading" workflows

### Computed Fields in QuerySet

All `RO` (read-only) fields are computed at database level via QuerySet mixins:
- Annotations added by ViewSet queryset properties
- Reduces N+1 queries and improves performance
- Fields appear as model properties in serialized response

### Image Handling

Both serializers use `square_medium` source:
- Automatically generated thumbnail from primary image
- Consistent sizing across API responses
- Lazy-loaded from ImageMixin property

## References

- [viewsets.md](viewsets.md) — ViewSet configuration and mixins
- [../models.md](../models.md) — StoryArc model definition
- [../../publishers/api/serializers.md](../../publishers/api/serializers.md) — NestedPublisherSerializer reference
