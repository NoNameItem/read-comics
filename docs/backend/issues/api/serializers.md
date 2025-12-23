# Issues Serializers

## Summary

- [`IssuesListSerializer`](#issueslistserializer) — Compact fields for list endpoint with finished flag
- [`IssueDetailSerializer`](#issuedetailserializer) — Full details with navigation slugs and position info
- [`IssueTechnicalInfoSerializer`](#issuetech icalinfoserializer) — Admin metadata (id, comicvine_id, status, timestamps)

## Reference

### `IssuesListSerializer`

Compact representation for list endpoint, optimized for bulk rendering.

**Fields:**

| Field | Source | Type | Description |
|-------|--------|------|-------------|
| `slug` | Issue.slug | str | Unique identifier for routing |
| `image` | Issue.square_medium | str | Square thumbnail image URL |
| `publisher` | volume.publisher | NestedPublisherSerializer | Nested publisher data |
| `name` | Issue.display_name | str | Formatted full name (e.g., "Volume (2020) #42") |
| `short_description` | Issue.short_description | str | Brief summary |
| `cover_date` | Issue.cover_date | date | Publication cover date |
| `volume` | Issue.volume | NestedVolumeSerializer | Nested volume data |
| `is_finished` | computed | bool or null | User's completion status |

**Method:**

- `get_is_finished(obj)` — Returns boolean or None based on `obj.finished_flg` annotation (user-specific)

---

### `IssueDetailSerializer`

Full representation for detail endpoint with navigation and position information.

**Fields:**

| Field | Source | Type | Description |
|-------|--------|------|-------------|
| `slug` | Issue.slug | str | Unique identifier |
| `image` | Issue.full_size_url | str | Full size image URL |
| `square_image` | Issue.square_medium | str | Square thumbnail URL |
| `publisher` | volume.publisher | NestedPublisherSerializer | Publisher data |
| `volume` | Issue.volume | NestedVolumeSerializer | Volume data |
| `number` | Issue.number | str | Issue number (e.g., "42", "½") |
| `volume_last_number` | Issue.volume_last_number | str | Last issue number in volume |
| `name` | Issue.name | str | Issue title |
| `cover_date` | Issue.cover_date | date | Cover date |
| `store_date` | Issue.store_date | date | Store release date |
| `short_description` | Issue.short_description | str | Brief summary |
| `description` | Issue.html_description | str | Full HTML description |
| `comicvine_url` | Issue.comicvine_url | str | Link to ComicVine page |
| `download_link` | Issue.download_link | str | DigitalOcean Space download URL |
| `download_size` | Issue.download_size | str | Human-readable file size |
| `is_finished` | computed | bool or null | Completion status |
| `prev_issue_slug` | context | str or null | Previous issue slug for navigation |
| `next_issue_slug` | context | str or null | Next issue slug for navigation |
| `number_in_sublist` | computed | int | Position in filtered/ordered list |
| `total_in_sublist` | context | int | Total issues in filtered list |

**Methods:**

- `get_is_finished(obj)` — Returns completion status for user or None
- `get_prev_issue_slug(_obj)` — Returns `context["prev_issue_slug"]` from viewset
- `get_next_issue_slug(_obj)` — Returns `context["next_issue_slug"]` from viewset
- `get_number_in_sublist(_obj)` — Returns `context["number_in_sublist"]` (1-indexed position)
- `get_total_in_sublist(_obj)` — Returns `context["total_in_sublist"]` (list size)

---

### `IssueTechnicalInfoSerializer`

Admin-only metadata serializer for technical information and ComicVine sync status.

**Fields:**

| Field | Source | Type | Description |
|-------|--------|------|-------------|
| `id` | Issue.id | int | Primary key |
| `comicvine_id` | Issue.comicvine_id | int | ComicVine API ID |
| `comicvine_status` | Issue.get_comicvine_status_display | str | Human-readable status (MATCHED/NOT_MATCHED/QUEUED) |
| `comicvine_last_match` | Issue.comicvine_last_match | datetime | Last sync timestamp |
| `created_dt` | Issue.created_dt | datetime | Record creation timestamp |
| `modified_dt` | Issue.modified_dt | datetime | Last modification timestamp |

**Access:** Via `/issues/{slug}/tech-info/` endpoint (TechnicalInfoActionMixin).