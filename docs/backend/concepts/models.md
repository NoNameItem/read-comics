# Concept Model

The `Concept` model represents comic book concepts, themes, and abstract ideas that appear in issues.

Extends: `ImageMixin`, `DownloadSizeMixin`, `AliasesListMixin`, `ComicvineSyncModel`

**Inherited Fields from ComicvineSyncModel:**

| Field | Type | Purpose |
|---|---|---|
| `id` | Integer (PK) | Django primary key |
| `comicvine_id` | Integer (unique) | ComicVine API identifier |
| `api_detail_url` | URLField | ComicVine API endpoint URL |
| `site_detail_url` | URLField | ComicVine website URL |
| `crawl_source` | CharField | Either "list" or "detail" indicating data completeness |
| `comicvine_status` | CharField | Status: Not Matched, Queued, or Matched |
| `comicvine_last_match` | DateTimeField | Timestamp of last successful sync |
| `created_dt` | DateTimeField | Record creation timestamp (auto-set) |
| `modified_dt` | DateTimeField | Last modification timestamp (auto-updated) |

**Custom Fields (defined in Concept model):**

| Field | Type | Description |
|-------|------|-------------|
| `name` | TextField | Concept name (nullable) |
| `aliases` | TextField | Pipe-separated alias names (nullable) |
| `short_description` | TextField | Brief description from ComicVine (nullable) |
| `html_description` | TextField | HTML-formatted description (nullable) |
| `start_year` | IntegerField | Year concept was introduced (nullable) |
| `first_issue_name` | TextField | Name of first appearance issue (nullable, fallback) |
| `first_issue` | ForeignKey → Issue | First appearance issue (nullable, SET_NULL) |
| `first_issue_comicvine_id` | IntegerField | ComicVine ID of first issue (nullable) |
| `thumb_url` | URLField | Small image URL from ComicVine (nullable) |
| `image_url` | URLField | Full-size image URL from ComicVine (nullable) |
| `slug` | AutoSlugField | URL-safe identifier (auto-generated from name, unique) |
| `watchers` | GenericRelation → WatchedItem | Users watching this concept |
| `tracker` | FieldTracker | Tracks field changes for change detection |

## Key Methods

### `__str__() → str`
Returns the concept name for string representation.

### `pre_save(force_insert, force_update, using, update_fields) → None`
Called before saving. Automatically resolves `first_issue_comicvine_id` to the actual `Issue` FK reference:
- Queries Issue by `comicvine_id` if `first_issue_comicvine_id` was changed
- Sets `first_issue` to the matched issue or None if not found
- Allows graceful handling of issues that may not yet exist in database

### `get_absolute_url() → str`
Returns URL to concept's detail page:
```python
/concepts/{slug}/
```

### `download_link` property → str
Returns reverse URL for concept download:
```python
/concepts/{slug}/download/
```

## Model Metadata

- **Ordering**: By `name` (alphabetical)
- **Related names**:
  - `first_appearance_concepts` — Issues using this concept as first appearance
  - Through GenericRelation: users can watch this concept

## Usage Example

```python
from read_comics.concepts.models import Concept

# Get a concept by slug
concept = Concept.objects.get(slug="magic")

# Access first appearance
print(concept.first_issue.display_name)  # "Amazing Spider-Man #1"

# Get all issues with this concept
all_issues = concept.issues.all()

# Check if matches were found
if concept.was_matched():
    print(f"{concept.name} has been synced from ComicVine")

# List aliases
aliases = concept.get_aliases_list()  # ["Magic", "Sorcery", "Witchcraft"]
```

## Relationships

- **one-to-many** with Issue: `first_issue` (nullable FK)
- **many-to-many** (via Issue) with Volume, Publisher, Character, Team, etc.
- **GenericRelation** with WatchedItem for user following