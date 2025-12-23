# Objects Models

## Summary

- [`Object`](#object) — Artifact/equipment entity with ComicVine sync, first appearance tracking, and watchable status

## Reference

### `Object`

Represents an artifact, equipment, or item appearing in comic issues. Inherits from `ImageMixin` and `ComicvineSyncModel` for image handling and ComicVine synchronization.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | TextField | Object/artifact name |
| `aliases` | TextField | Alternative names (newline-separated) |
| `short_description` | TextField | Brief summary |
| `html_description` | TextField | Full HTML description |
| `start_year` | IntegerField | Year object first appeared |
| `first_issue_name` | TextField | Cached first issue name (fallback) |
| `first_issue` | ForeignKey | First issue where object appeared (SET_NULL) |
| `first_issue_comicvine_id` | IntegerField | ComicVine ID for first issue lookup |
| `thumb_url` | URLField | Thumbnail image URL |
| `image_url` | URLField | Full size image URL |
| `slug` | AutoSlugField | Unique slug (auto-generated from name) |

**Relationships:**

- `first_issue` (ForeignKey) — Issue where object first appeared (optional, SET_NULL if issue deleted)
- `issues` (M2M) — Issues featuring this object (reverse from Issue model)
- `watchers` (GenericRelation) — Users watching this object for missing issues

**ComicVine Configuration:**

- `MONGO_COLLECTION = "comicvine_objects"` — MongoDB collection for cached object data
- `FIELD_MAPPING = {"start_year": "start_year"}` — Simple field mapping to ComicVine field
- `COMICVINE_FORCE_DETAIL_INFO = False` [inherited] — OK to use list API data

**Key Methods:**

- `__str__()` → Object name
- `get_absolute_url()` → Django URL for object detail page
- `get_aliases_list()` → Returns aliases split by newline or empty list
- `pre_save()` — Resolves `first_issue_comicvine_id` to `first_issue` FK when changed

**Properties:**

- `download_link` → Django URL for downloading object data

**Meta:**

- Default ordering: `("name",)` — Alphabetical
