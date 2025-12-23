# People Models

## Summary

- **`Person`** — Creator/contributor model with biographical data, ComicVine sync, and watchable status

## Reference

### Person

Creator, artist, and industry contributor model with biographical information and ComicVine integration.

**Inheritance**: `ImageMixin`, `ComicvineSyncModel`

#### Fields

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
| `image_url` | URLField | Full-size image URL (from ImageMixin) |
| `slug` | AutoSlugField | URL-safe identifier, auto-generated from name |
| `watchers` | GenericRelation | Users watching this person for missing issues |

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