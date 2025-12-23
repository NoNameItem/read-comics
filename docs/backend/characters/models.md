# Character model in `characters/models.py`

## Summary

- [`Character`](#character) — comic book character model with ComicVine synchronization, image management, relationship tracking (friends/enemies, teams), and download support.

## `Character`

Extends: [`ComicvineSyncModel`](../utils/models.md#comicvinesyncmodel), [`ImageMixin`](../utils/model_mixins.md#imagemixin), [`DownloadSizeMixin`](../utils/model_mixins.md#downloadsizemixin), [`AliasesListMixin`](../utils/model_mixins.md#aliaseslistmixin)

Stores detailed character information: name, real name, aliases, gender, birth date, origin, descriptions. Manages relationships with publishers, other characters (friends/enemies), teams (membership/enemies/friends), creators, and powers.

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

**Custom Fields (defined in Character model):**

| Field | Type | Purpose |
|---|---|---|
| `name` | TextField | Character name |
| `real_name` | TextField | Character's real identity name (nullable) |
| `aliases` | TextField | Character aliases (newline-separated, nullable) |
| `short_description` | TextField | Brief character description from ComicVine (nullable) |
| `html_description` | TextField | Full HTML-formatted description (nullable) |
| `gender` | IntegerField with Gender choices | Character gender (nullable) |
| `birth` | DateField | Birth date (nullable) |
| `origin` | TextField | Character origin description (nullable) |
| `thumb_url` | URLField | Thumbnail image URL (max 1000 chars, nullable) |
| `image_url` | URLField | Full-size image URL (max 1000 chars, nullable) |
| `publisher` | ForeignKey → Publisher | Publisher owning character (nullable, CASCADE delete) |
| `character_enemies` | ManyToManyField (self) | Enemy characters |
| `character_friends` | ManyToManyField (self) | Friend characters |
| `teams` | ManyToManyField → Team | Teams character is member of |
| `team_enemies` | ManyToManyField → Team | Enemy teams |
| `team_friends` | ManyToManyField → Team | Friendly teams |
| `first_issue_name` | TextField | Text name of first appearance issue (nullable) |
| `first_issue` | ForeignKey → Issue | First appearance issue (nullable, SET_NULL) |
| `first_issue_comicvine_id` | IntegerField | ComicVine ID of first issue (nullable) |
| `creators` | ManyToManyField → Person | Character creators (writers, artists) |
| `powers` | ManyToManyField → Power | Character superpowers |
| `slug` | AutoSlugField | URL-safe slug (unique, auto-generated from publisher and name) |
| `watchers` | GenericRelation → WatchedItem | Users watching character for missing issues |
| `tracker` | FieldTracker | Tracks field changes for synchronization |

### Class attributes for ComicVine integration

- `MONGO_COLLECTION = "comicvine_characters"`: MongoDB collection name for caching ComicVine data.
- `MONGO_PROJECTION`: Dictionary excluding unused fields from MongoDB queries (`count_of_issue_appearances`, `date_added`, `date_last_updated`, `issue_credits`, `issues_died_in`, `movies`, `story_arc_credits`, `volume_credits`).
- `FIELD_MAPPING`: Maps ComicVine JSON fields to Django model fields:
  - `"real_name"`: Character's real name
  - `"gender"`: Character gender
  - `"birth"`: Birth date (converted via `convert_date` method)
  - `"origin"`: Origin from `origin.name` path
  - `"character_enemies"`: Enemy characters (via `get_character` helper)
  - `"character_friends"`: Friend characters (via `get_character` helper)
  - `"teams"`: Team memberships (via `get_team` helper)
  - `"team_enemies"`: Enemy teams (via `get_team` helper)
  - `"team_friends"`: Friendly teams (via `get_team` helper)
  - `"publisher"`: Publisher (via `get_publisher` helper)
  - `"creators"`: Character creators (via `get_person` helper)
  - `"powers"`: Character powers (via `get_power` helper)
- `COMICVINE_INFO_TASK`: References `character_comicvine_info_task` for background synchronization.
- `COMICVINE_API_URL`: Template URL for requesting character details from ComicVine API, including fields: `id`, `api_detail_url`, `site_detail_url`, `name`, `aliases`, `deck`, `description`, `image`, `first_appeared_in_issue`, `real_name`, `gender`, `birth`, `origin`, `character_friends`, `character_enemies`, `teams`, `team_enemies`, `team_friends`, `publisher`, `creators`, `powers`.

### Inner classes

#### `Gender` (IntegerChoices)

Enumeration for character gender values:
- `OTHER = 0, "Other"`: Other/unspecified gender
- `MALE = 1, "Male"`: Male gender
- `FEMALE = 2, "Female"`: Female gender

### Meta options

- `ordering = ("name",)`: Default ordering by character name.

### Methods

- `__str__(self) -> str`
  - Returns string representation of the character.
  - Format: `"Name (Publisher)"` if publisher exists, otherwise just `"Name"`.
  - Returns empty string if name is not set.

- `get_publisher_name(self) -> str | None`
  - Retrieves the publisher's name for this character.
  - Returns `publisher.name` or `None` if no publisher is set.
  - Used during slug generation to include publisher name in URL.

- `get_absolute_url(self)`
  - Generates absolute URL for the character detail page.
  - Returns URL pattern: `/characters/<slug>/` (via `characters:detail` route).

- `convert_date(s)` (static method)
  - Converts ComicVine date string to datetime object.
  - `s`: Date string in format `"Dec 31, 2023"` or `None`.
  - Returns `datetime` object if valid, otherwise `None`.
  - Format: `"%b %d, %Y"` (abbreviated month, day, year).

- `pre_save(self, force_insert=False, force_update=False, using=None, update_fields=None)`
  - Lifecycle hook called before saving the model (part of [`ComicvineSyncModel`](../utils/models.md#comicvinesyncmodel) lifecycle).
  - Parameters: Standard Django `Model.save()` parameters.
  - Behavior:
    - Checks if `first_issue_comicvine_id` changed using `tracker`.
    - If changed, attempts to find matching `Issue` by `comicvine_id` and sets `first_issue` relation.
    - Sets `first_issue = None` if issue not found (`Issue.DoesNotExist`).
  - Purpose: Automatic synchronization of `first_issue` relation when `first_issue_comicvine_id` changes.

### Properties

- `download_link -> str`
  - Generates URL for downloading character's issues.
  - Returns URL pattern: `/characters/<slug>/download/` (via `characters:download` route).
  - Provides link to download archive of all character issues.