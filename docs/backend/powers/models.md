# Powers Models

## Summary

- **`Power`** — Superpower/ability model with ComicVine sync and slug-based identification

## Reference

### Power

Superpower or ability model representing comic superpowers (e.g., "Flight", "Super Strength").

**Inheritance**: `ComicvineSyncModel`

#### Fields

| Field | Type | Purpose |
|-------|------|---------|
| `name` | TextField | Power name |
| `aliases` | TextField | Alternate names (newline-separated) |
| `html_description` | TextField | Formatted description |
| `thumb_url` | URLField | Thumbnail image URL |
| `image_url` | URLField | Full-size image URL (from ImageMixin) |
| `slug` | AutoSlugField | URL-safe identifier, auto-generated from name |

#### ComicVine Sync Configuration

```python
MONGO_COLLECTION = "comicvine_powers"
COMICVINE_INFO_TASK = power_comicvine_info_task
COMICVINE_API_URL = "https://comicvine.gamespot.com/api/power/4035-{id}/?..."
```

**Field Mapping** (`FIELD_MAPPING`): None (all fields mapped via standard ComicvineSyncModel logic based on field names)

**Excluded from MongoDB sync** (`MONGO_PROJECTION`):
- count_of_issue_appearances
- date_added, date_last_updated
- characters

#### Methods

| Method | Purpose |
|--------|---------|
| `__str__()` | Returns power name |

#### Ordering

Default ordering by `name` (alphabetical).

#### Notes

- **Reference data** — Powers are reference entities without direct issue appearances tracking (unlike Character, Location, Object models)
- **No watchers** — Users cannot watch powers for missing issues
- **No first appearance** — No tracking of first appearance issue