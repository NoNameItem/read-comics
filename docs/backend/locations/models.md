# Locations Models

## Summary

- [`Location`](#location) — Geographic location entity with ComicVine sync, first appearance tracking, and watchable status

## Reference

### `Location`

Represents a geographic location appearing in comic issues. Inherits from `ImageMixin`, `DownloadSizeMixin`, `AliasesListMixin`, and `ComicvineSyncModel` for image handling, file management, aliases parsing, and ComicVine synchronization.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | TextField | Location name |
| `aliases` | TextField | Alternative names (newline-separated) |
| `short_description` | TextField | Brief summary |
| `html_description` | TextField | Full HTML description |
| `start_year` | IntegerField | Year location first appeared |
| `first_issue_name` | TextField | Cached first issue name (fallback) |
| `first_issue` | ForeignKey | First issue where location appeared (SET_NULL) |
| `first_issue_comicvine_id` | IntegerField | ComicVine ID for first issue lookup |
| `thumb_url` | URLField | Thumbnail image URL |
| `image_url` | URLField | Full size image URL |
| `slug` | AutoSlugField | Unique slug (auto-generated from name) |

**Relationships:**

- `first_issue` (ForeignKey) — Issue where location first appeared (optional, SET_NULL if issue deleted)
- `issues` (M2M) — Issues featuring this location (reverse from Issue model)
- `watchers` (GenericRelation) — Users watching this location for missing issues

**ComicVine Configuration:**

- `MONGO_COLLECTION = "comicvine_locations"` — MongoDB collection for cached location data
- `FIELD_MAPPING = {"start_year": "start_year"}` — Simple field mapping to ComicVine field
- `COMICVINE_FORCE_DETAIL_INFO = False` [inherited] — OK to use list API data

**Key Methods:**

- `__str__()` → Location name
- `get_absolute_url()` → Django URL for location detail page
- `get_aliases_list()` → Returns aliases split by newline or empty list
- `pre_save()` — Resolves `first_issue_comicvine_id` to `first_issue` FK when changed

**Properties:**

- `download_link` → Django URL for downloading location data
- `download_size` → Human-readable file size (inherited from DownloadSizeMixin)

**Meta:**

- Default ordering: `("name",)` — Alphabetical
