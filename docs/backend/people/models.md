# People Models

## Summary

- **`Person`** — Creator/contributor model with biographical data, ComicVine sync, and watchable status

## Reference

### Person

Creator, artist, and industry contributor model with biographical information and ComicVine integration.

Extends: `ImageMixin`, `ComicvineSyncModel`

**Inherited Fields from ComicvineSyncModel:**

| Field | Type | Purpose |
|-------|------|---------|
| `id` | Integer (PK) | Django primary key |
| `comicvine_id` | Integer (unique) | ComicVine API identifier |
| `api_detail_url` | URLField | ComicVine API endpoint URL |
| `site_detail_url` | URLField | ComicVine website URL |
| `crawl_source` | CharField | Either "list" or "detail" indicating data completeness |
| `comicvine_status` | CharField | Status: Not Matched, Queued, or Matched |
| `comicvine_last_match` | DateTimeField | Timestamp of last successful sync |
| `created_dt` | DateTimeField | Record creation timestamp (auto-set) |
| `modified_dt` | DateTimeField | Last modification timestamp (auto-updated) |

**Custom Fields (defined in Person model):**

| Field | Type | Purpose |
|-------|------|---------|
| `name` | TextField | Person's name |
| `aliases` | TextField | Alternate names (newline-separated) |
| `short_description` | TextField | Brief description/tagline |
| `html_description` | TextField | Formatted description |
| `birth_date` | DateField | Birth date (synced from ComicVine) |
| `death_date` | DateField | Death date (synced from ComicVine) |
| `hometown` | TextField | Hometown/residence |
| `country` | TextField | Country of origin |
| `thumb_url` | URLField | Thumbnail image URL |
| `image_url` | URLField | Full-size image URL |
| `slug` | AutoSlugField | URL-safe identifier, auto-generated from name |
| `watchers` | GenericRelation → WatchedItem | Users watching this person |
| `tracker` | FieldTracker | Tracks field changes for synchronization |

#### ComicVine Sync Configuration

```python
MONGO_COLLECTION = "comicvine_people"
COMICVINE_INFO_TASK = person_comicvine_info_task
COMICVINE_API_URL = "https://comicvine.gamespot.com/api/person/4040-{id}/?..."
```

**Field Mapping** (`FIELD_MAPPING`):
- `birth_date` ← ComicVine `birth` (converted via `convert_date`)
- `death_date` ← ComicVine `death.date` (converted via `convert_date`)
- `country` ← ComicVine `country`
- `hometown` ← ComicVine `hometown`

**Excluded from MongoDB sync** (`MONGO_PROJECTION`):
- count_of_issue_appearances
- date_added, date_last_updated
- issues, story_arc_credits, volume_credits
- created_characters
- email, gender

#### Methods

| Method | Purpose |
|--------|---------|
| `__str__()` | Returns person's name |
| `convert_date(s)` | Static method — converts ISO datetime string to Python `datetime` object |
| `get_absolute_url()` | Returns URL to person detail page (`people:detail` route) |
| `get_aliases_list()` | Returns list of aliases by splitting `aliases` field on newlines |
| `download_link` (property) | Returns URL to person download endpoint (`people:download` route) |

#### Ordering

Default ordering by `name` (alphabetical).