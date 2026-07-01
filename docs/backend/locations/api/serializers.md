# Locations Serializers

## Summary

- [`LocationsListSerializer`](#locationslistserializer) — Compact fields for list endpoint with issue/volume counts
- [`LocationDetailSerializer`](#locationdetailserializer) — Full details with first issue and download link
- [`ConceptTechnicalInfoSerializer`](#concepttechnicalinfoserializer) — Admin metadata (id, comicvine_id, status, timestamps)

## Reference

### `LocationsListSerializer`

Compact representation for list endpoint, optimized for bulk rendering with aggregated counts.

**Fields:**

| Field | Source | Type | Description |
|-------|--------|------|-------------|
| `slug` | Location.slug | str | Unique identifier for routing |
| `image` | Location.square_medium | str | Square thumbnail image URL |
| `name` | Location.name | str | Location name |
| `short_description` | Location.short_description | str | Brief summary |
| `issues_count` | computed | int | Count of issues featuring this location |
| `volumes_count` | computed | int | Count of volumes featuring this location |

**Computed Fields (via QuerySet mixins):**

- `issues_count` — Aggregated from IssuesCountQuerySetMixin
- `volumes_count` — Aggregated from VolumesCountQuerySetMixin

---

### `LocationDetailSerializer`

Full representation for detail endpoint with first issue reference and download capability.

**Fields:**

| Field | Source | Type | Description |
|-------|--------|------|-------------|
| `slug` | Location.slug | str | Unique identifier |
| `name` | Location.name | str | Location name |
| `image` | Location.full_size_url | str | Full size image URL |
| `square_image` | Location.square_medium | str | Square thumbnail URL |
| `aliases` | Location.get_aliases_list | list[str] | Alternative names |
| `start_year` | Location.start_year | int or null | Year first appeared |
| `first_issue_name` | computed | str or null | Name of first issue |
| `first_issue_slug` | computed | str or null | Slug of first issue for navigation |
| `comicvine_url` | Location.comicvine_url | str | Link to ComicVine page |
| `short_description` | Location.short_description | str | Brief summary |
| `description` | Location.html_description | str | Full HTML description |
| `download_link` | computed | str | Absolute URL for location download |
| `download_size` | Location.download_size | str | Human-readable file size |

**Methods:**

- `get_first_issue_name(obj)` [static] — Returns `obj.first_issue.display_name` if available, else cached `obj.first_issue_name`
- `get_first_issue_slug(obj)` [static] — Returns `obj.first_issue.slug` or None
- `get_download_link(obj)` — Returns absolute URL using request context

---

### `ConceptTechnicalInfoSerializer`

Admin-only metadata serializer for technical information and ComicVine sync status.

**Note:** Class name is "ConceptTechnicalInfoSerializer" but used for Location (likely a copy-paste error in source).

**Fields:**

| Field | Source | Type | Description |
|-------|--------|------|-------------|
| `id` | Location.id | int | Primary key |
| `comicvine_id` | Location.comicvine_id | int | ComicVine API ID |
| `comicvine_status` | Location.get_comicvine_status_display | str | Human-readable status (MATCHED/NOT_MATCHED/QUEUED) |
| `comicvine_last_match` | Location.comicvine_last_match | datetime | Last sync timestamp |
| `created_dt` | Location.created_dt | datetime | Record creation timestamp |
| `modified_dt` | Location.modified_dt | datetime | Last modification timestamp |

**Access:** Via `/locations/{slug}/tech-info/` endpoint (TechnicalInfoActionMixin).