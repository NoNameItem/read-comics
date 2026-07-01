# Issues Models

## Summary

- [`Issue`](#issue) — Main comic issue entity with ComicVine sync, relationships, and downloadable file metadata
- [`IssuePerson`](#issueperson) — Through model for Issue-Person relationships with role information
- [`FinishedIssue`](#finishedissue) — Track which users have finished reading specific issues

## Reference

### `Issue`

Main entity representing a comic book issue.

Extends: `ImageMixin`, `ComicvineSyncModel`

**Inherited Fields from ComicvineSyncModel:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (PK) | Django primary key |
| `comicvine_id` | Integer (unique) | ComicVine API identifier |
| `api_detail_url` | URLField | ComicVine API endpoint URL |
| `site_detail_url` | URLField | ComicVine website URL |
| `crawl_source` | CharField | Either "list" or "detail" indicating data completeness |
| `comicvine_status` | CharField | Status: Not Matched, Queued, or Matched |
| `comicvine_last_match` | DateTimeField | Timestamp of last successful sync |
| `created_dt` | DateTimeField | Record creation timestamp (auto-set) |
| `modified_dt` | DateTimeField | Last modification timestamp (auto-updated) |

**Custom Fields (defined in Issue model):**

| Field | Type | Description |
|-------|------|-------------|
| `name` | TextField | Issue title/name |
| `aliases` | TextField | Alternative names |
| `short_description` | TextField | Brief summary |
| `html_description` | TextField | Full HTML description |
| `number` | CharField | Issue number (e.g., "#1", "½", "1-2") |
| `numerical_number` | FloatField | Parsed numeric version (0.5 for "½") |
| `cover_date` | DateField | Cover publication date |
| `store_date` | DateField | Store release date |
| `thumb_url` | URLField | Thumbnail image URL |
| `image_url` | URLField | Full size image URL |
| `variant_covers` | ArrayField | List of variant cover URLs |
| `space_key` | CharField | DigitalOcean Space file key |
| `size` | IntegerField | File size in bytes |
| `slug` | AutoSlugField | Unique slug (auto-generated from publisher/volume/number/name) |
| `volume` | ForeignKey → Volume | Parent Volume (CASCADE delete) |
| `watchers` | GenericRelation → WatchedItem | Users watching this issue |
| `tracker` | FieldTracker | Tracks field changes for synchronization |

**Relationships:**

- `volume` (ForeignKey) — Parent Volume (CASCADE delete)
- `characters` (M2M) — Characters featured in issue
- `characters_died` (M2M) — Characters who died in issue
- `concepts` (M2M) — Story concepts
- `locations` (M2M) — Locations featured
- `objects_in` (M2M) — Objects/artifacts featured
- `people` (M2M via IssuePerson) — Authors, editors, etc. with roles
- `story_arcs` (M2M) — Story arcs this issue belongs to
- `teams` (M2M) — Teams featured
- `disbanded_teams` (M2M) — Teams that disbanded in this issue
- `finished_users` (M2M via FinishedIssue) — Users who finished reading

**ComicVine Configuration:**

```python
MONGO_COLLECTION = "comicvine_issues"
FIELD_MAPPING = {
    "html_description": {"path": "description", "method": "get_description"},
    "number": "issue_number",
    "cover_date": {"path": "cover_date", "method": "convert_date"},
    # ... 11 other mappings for characters, concepts, locations, objects, people, story_arcs, teams, volume, variant_covers
}
COMICVINE_FORCE_DETAIL_INFO = True  # Always fetch full details
```

**Key Methods:**

#### `__str__()`
Returns display name: `"{full_name} ({publisher_name})"` or just `"{full_name}"` if no publisher.

#### `get_full_name(volume_name=None, volume_start_year=None)`
Returns formatted name: `"Volume Name (2020) #42 Issue Title"` or `"Volume Name (2020) #42"` if no title.

#### `get_publisher_name()`
Returns publisher name from related volume, or `None` if no volume/publisher.

#### `get_volume_name()`
Returns volume name or `None`.

#### `get_volume_start_year()`
Returns volume start year or `None`.

#### `set_numerical_number()`
Parses `number` field and sets `numerical_number`:
- "½" → 0.5
- "42" → 42.0
- "42.5" → 42.5
- Non-numeric → 0

#### `create_links()`
Updates related models to set this issue as their `first_issue`:
- Characters/Concepts/Locations/Objects/StoryArcs/Teams/Volumes with matching `first_issue_comicvine_id`
- Volumes with matching `last_issue_comicvine_id`

#### `post_save()`
Called after save:
1. Calls `create_links()`
2. Deletes related `MissingIssue` and `IgnoredIssue` records

#### `pre_save()`
Called before save:
1. If status is MATCHED and number/name/volume changed: updates DigitalOcean Space metadata
2. Calls `set_numerical_number()`

#### `update_do_metadata(volume_name=None, volume_start_year=None)`
Updates DigitalOcean Space S3 metadata for downloadable file with proper filename and content disposition.

#### `get_description(text)` [static]
Strips HTML from description: removes `<a>` tags and covers table markup.

#### `convert_date(s)` [static]
Converts ISO format date string to datetime object.

#### `get_author(comicvine_author)` [static]
Parses ComicVine author object, gets/creates Person model, returns `(person, {"role": role})`.

#### `get_variant_covers(value)` [static]
Extracts list of variant cover URLs from ComicVine associated_images array.

**Properties:**

- `display_name: str` — Returns `get_full_name()`
- `download_link: str` — Formatted DigitalOcean Space URL with URI escaping
- `download_size: str` — Human-readable file size (e.g., "42.5 MB") or "size unknown"
- `volume_last_number: str` — Volume's last issue number or "unknown"

**Methods for Pagination (DetailSerializerMixin):**

Used by `IssueViewSet` to generate previous/next issue slugs based on ordering:

- `get_next_filters(orderings, instance)` → Q filter for next issue
- `get_prev_filters(orderings, instance)` → Q filter for previous issue
- `get_next_issue_slug(instance)` → slug or None
- `get_prev_issue_slug(instance)` → slug or None
- `get_number_in_sublist(instance)` → position in filtered list

---

### `IssuePerson`

Through model for Issue ↔ Person relationships, storing the author/editor role.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `issue` | ForeignKey | Issue (CASCADE delete) |
| `person` | ForeignKey | Person (CASCADE delete) |
| `role` | CharField | Role (e.g., "Writer", "Penciller") |

**Access:**

- From Issue: `issue.people.all()` or `issue.authors.all()` (through related_name)
- From Person: `person.issues.all()` or `person.authored_issues.all()`

---

### `FinishedIssue`

Tracks which users have completed reading specific issues. Automatically records finish date.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | User (CASCADE delete) |
| `issue` | ForeignKey | Issue (CASCADE delete) |
| `finish_date` | DateTimeField | When issue was marked finished (auto-set on creation) |

**Constraints:**

- `unique_together = (("user", "issue"),)` — Each user can only finish an issue once

**Access:**

- From User: `user.finished_issues.all()` or `user.finished.all()`
- From Issue: `issue.finished_users.all()` or `issue.finished.all()`
