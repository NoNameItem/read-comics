# Character model in `characters/models.py`

## Summary

- [`Character`](#character) — comic book character model with ComicVine synchronization, image management, relationship tracking (friends/enemies, teams), and download support.

## `Character`

- Django model inheriting from [`ComicvineSyncModel`](../utils/models.md#comicvinesyncmodel) with [`ImageMixin`](../utils/model_mixins.md#imagemixin), [`DownloadSizeMixin`](../utils/model_mixins.md#downloadsizemixin), and [`AliasesListMixin`](../utils/model_mixins.md#aliaseslistmixin).
- Stores detailed character information: name, real name, aliases, gender, birth date, origin, descriptions.
- Manages relationships with publishers, other characters (friends/enemies), teams (membership/enemies/friends), creators, and powers.
- Tracks first appearance through foreign key to [`Issue`](../issues/models.md) model.
- Supports automatic slug generation based on publisher name and character name.
- Integrates with [`WatchedItem`](../missing_issues/models.md) for user notifications.
- Uses `FieldTracker` to monitor field changes (e.g., `first_issue_comicvine_id`).

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

### Model fields

#### Basic text fields

- `name` (TextField, nullable): Character name.
- `real_name` (TextField, nullable): Character's real name (not superhero alias).
- `aliases` (TextField, nullable): Character aliases separated by newlines.
- `short_description` (TextField, nullable): Brief character description (deck from ComicVine).
- `html_description` (TextField, nullable): Full HTML description of the character.

#### Character attributes

- `gender` (IntegerField with `Gender.choices`, nullable): Character gender.
- `birth` (DateField, nullable): Character birth date.
- `origin` (TextField, nullable): Character origin description.

#### Image fields

- `thumb_url` (URLField, max_length=1000, nullable): Thumbnail image URL.
- `image_url` (URLField, max_length=1000, nullable): Full-size image URL.

#### Publisher relationship

- `publisher` (ForeignKey to `publishers.Publisher`, nullable, CASCADE): Publisher owning this character. Deleting the publisher cascades to all characters. Reverse relation: `publisher.characters`.

#### Character relationships

- `character_enemies` (ManyToManyField to `self`): Enemy characters.
- `character_friends` (ManyToManyField to `self`): Friend characters.

#### Team relationships

- `teams` (ManyToManyField to `teams.Team`): Teams the character is a member of. Reverse relation: `team.characters`.
- `team_enemies` (ManyToManyField to `teams.Team`): Enemy teams. Reverse relation: `team.character_enemies`.
- `team_friends` (ManyToManyField to `teams.Team`): Friendly teams. Reverse relation: `team.character_friends`.

#### First appearance

- `first_issue_name` (TextField, nullable): Text name of the first issue where the character appeared.
- `first_issue` (ForeignKey to `issues.Issue`, nullable, SET_NULL): Reference to the first issue. Sets to `NULL` on issue deletion. Reverse relation: `issue.first_appearance_characters`.
- `first_issue_comicvine_id` (IntegerField, nullable): ComicVine ID of the first issue for tracking and synchronization.

#### Creators and powers

- `creators` (ManyToManyField to `people.Person`): Character creators (writers, artists). Reverse relation: `person.created_characters`.
- `powers` (ManyToManyField to `powers.Power`): Character superpowers. Reverse relation: `power.characters`.

#### Utility fields

- `slug` (AutoSlugField): Auto-generated slug based on publisher name and character name. Configuration:
  - `populate_from=["get_publisher_name", "name"]`: Sources for slug generation.
  - `slugify_function=slugify_function`: Slugification function (preserves case).
  - `overwrite=True`: Regenerates when sources change.
  - `max_length=1000`: Maximum length.
  - `unique=True`: Ensures uniqueness.
- `watchers` (GenericRelation to `WatchedItem`): Users watching this character for notifications.
- `tracker` (FieldTracker): Tracks field changes (used in `pre_save`).

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