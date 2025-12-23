# Concept Serializers

Three serializers for different API endpoints with varying levels of detail.

## Summary

- [`ConceptsListSerializer`](#conceptslistserializer) — Compact serializer for list endpoint
- [`ConceptDetailSerializer`](#conceptdetailserializer) — Full details for detail endpoint
- [`ConceptTechnicalInfoSerializer`](#concepttechnicalinfoserializer) — Metadata for admin

---

## Reference

### `ConceptsListSerializer`

Used for `/api/concepts/` list endpoint. Returns compact concept data with aggregated counts.

**Fields:**

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `slug` | String | Model | URL-safe identifier for concept |
| `image` | String (ReadOnly) | `square_medium` | Square medium-size image URL |
| `name` | String | Model | Concept name |
| `short_description` | String | Model | Brief description from ComicVine |
| `issues_count` | Integer (ReadOnly) | Aggregated | Number of issues with this concept |
| `volumes_count` | Integer (ReadOnly) | Aggregated | Number of volumes containing this concept |

**Example Response:**
```json
{
  "slug": "magic",
  "image": "https://comicvine.gamespot.com/api/image/.../magic-square.jpg",
  "name": "Magic",
  "short_description": "The use of supernatural forces",
  "issues_count": 245,
  "volumes_count": 89
}
```

---

### `ConceptDetailSerializer`

Used for `/api/concepts/{slug}/` detail endpoint. Returns comprehensive concept information including relationships and download links.

**Fields:**

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `slug` | String | Model | URL-safe identifier |
| `name` | String | Model | Concept name |
| `image` | String (ReadOnly) | `full_size_url` | Full-size image URL |
| `square_image` | String (ReadOnly) | `square_medium` | Square medium-size image URL |
| `aliases` | Array (ReadOnly) | `get_aliases_list()` | Parsed alternative names |
| `start_year` | Integer | Model | Year concept was introduced |
| `first_issue_name` | String (Method) | `get_first_issue_name()` | Display name of first appearance issue |
| `first_issue_slug` | String (Method) | `get_first_issue_slug()` | URL slug of first appearance issue |
| `comicvine_url` | String | Model | Link to ComicVine page |
| `short_description` | String | Model | Brief description |
| `description` | String | Model | Full HTML description |
| `download_link` | String (Method) | `get_download_link()` | Absolute URL to download concept data |
| `download_size` | String | Mixin | Human-readable download size (e.g., "2.5 MB") |

**SerializerMethodField Methods:**

#### `get_first_issue_name(obj: Concept) → str | None`
Returns display name of the first appearance issue:
- If `first_issue` FK exists: returns `first_issue.display_name`
- Fallback: returns `first_issue_name` field value
- None if neither exists

#### `get_first_issue_slug(obj: Concept) → str | None`
Returns slug of the first appearance issue:
- If `first_issue` FK exists: returns `first_issue.slug`
- Otherwise: returns None (stored slug not used)

#### `get_download_link(self, obj: Concept) → str`
Returns absolute URL for downloading concept data files:
- Uses request context to build full URL
- Points to `/concepts/{slug}/download/`

**Example Response:**
```json
{
  "slug": "magic",
  "name": "Magic",
  "image": "https://comicvine.gamespot.com/api/image/.../magic-full.jpg",
  "square_image": "https://comicvine.gamespot.com/api/image/.../magic-square.jpg",
  "aliases": ["Magic", "Sorcery", "Witchcraft"],
  "start_year": 1962,
  "first_issue_name": "Journey into Mystery #83",
  "first_issue_slug": "journey-into-mystery-83",
  "comicvine_url": "https://comicvine.gamespot.com/concept/magic/",
  "short_description": "The use of supernatural forces",
  "description": "<p>Magic is the use of supernatural forces...</p>",
  "download_link": "http://api.example.com/concepts/magic/download/",
  "download_size": "2.5 MB"
}
```

---

### `ConceptTechnicalInfoSerializer`

Used for `/api/concepts/{slug}/technical-info/` endpoint (staff/superuser only). Returns metadata about the concept's ComicVine sync status.

**Fields:**

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `id` | Integer | Model | Database primary key |
| `comicvine_id` | Integer | Model | ComicVine API ID |
| `comicvine_status` | String (ReadOnly) | `get_comicvine_status_display()` | Display value of sync status (e.g., "synced", "syncing", "failed") |
| `comicvine_last_match` | DateTime | Model | ISO timestamp of last successful sync |
| `created_dt` | DateTime | Model | ISO timestamp of database record creation |
| `modified_dt` | DateTime | Model | ISO timestamp of last modification |

**Example Response:**
```json
{
  "id": 42,
  "comicvine_id": 75632,
  "comicvine_status": "synced",
  "comicvine_last_match": "2024-12-20T15:30:45.123456+00:00",
  "created_dt": "2024-01-15T10:00:00.000000+00:00",
  "modified_dt": "2024-12-20T15:30:50.000000+00:00"
}
```

---

## Notes

- All `ReadOnlyField` sources use properties or methods to compute values from related data
- `SerializerMethodField` methods are static where possible for performance
- Image URLs are conditional based on Mixin's image availability
- Download size is humanized format (e.g., "1.2 MB", "45 bytes")
- Timestamps in detail/technical endpoints are localized to request timezone