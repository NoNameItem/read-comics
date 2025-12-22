# Serializers in `characters/api/serializers.py`

## Summary

- [`CharactersListSerializer`](#characterslistserializer) — DRF serializer for character list responses; returns compact fields including slug, image, publisher, name, and issue/volume counts.
- [`CharacterDetailSerializer`](#characterdetailserializer) — comprehensive serializer for character detail responses; exposes full metadata including aliases, birth date, gender, powers, first issue references, and download information.
- [`CharacterTechnicalInfoSerializer`](#charactertechnicalinfoserializer) — technical metadata serializer restricted to staff/superuser; returns ComicVine sync status, timestamps, and database IDs.

## Reference

### `CharactersListSerializer`

- Django REST Framework `ModelSerializer` subclass for [`Character`](../models.md#character) list/search responses.
- Optimized for compact representation with image thumbnails and basic metadata.
- Used by `CharacterViewSet.list` action.

#### Fields

- `slug` (str, read-only): Auto-generated URL-safe identifier combining publisher and character name.
- `image` (str, read-only): Medium-sized image URL derived from `square_medium` property (via `ImageMixin`).
- `publisher` (nested object, read-only): [`NestedPublisherSerializer`](../publishers/serializers.md) containing publisher name, image, and slug.
- `name` (str, read-only): Character name.
- `short_description` (str, read-only): Brief character description (deck from ComicVine).
- `issues_count` (int, read-only): Total number of issues featuring this character (populated by `IssuesCountQuerySetMixin`).
- `volumes_count` (int, read-only): Total number of volumes containing this character (populated by `VolumesCountQuerySetMixin`).

#### Meta

- `model = Character`
- `fields` = `["slug", "image", "publisher", "name", "short_description", "issues_count", "volumes_count"]`

### `CharacterDetailSerializer`

- Django REST Framework `ModelSerializer` subclass for [`Character`](../models.md#character) detail/retrieve responses.
- Provides comprehensive character information including aliases, abilities, first appearance, and download metadata.
- Used by `CharacterViewSet.retrieve` action.

#### Fields

- `slug` (str, read-only): URL-safe character identifier.
- `name` (str, read-only): Character name.
- `real_name` (str, read-only): Real name of the character (not superhero alias).
- `image` (str, read-only): Full-size character image URL via `full_size_url` property.
- `square_image` (str, read-only): Medium square image URL via `square_medium` property for UI consistency.
- `publisher` (nested object, read-only): Nested publisher metadata via `NestedPublisherSerializer`.
- `aliases` (list[str], read-only): Character aliases from `get_aliases_list()` method; splits newline-delimited aliases field.
- `gender` (str, read-only): Human-readable gender display via `get_gender_display()` (maps to `Gender.choices`).
- `powers` (list[str], read-only): List of character superpowers as string representations of related `Power` objects.
- `birth` (date, read-only): Character birth date in ISO 8601 format.
- `first_issue_name` (str, read-only): Name/title of the issue where character first appeared (via `get_first_issue_name` method).
- `first_issue_slug` (str, read-only): Slug of the first issue for URL lookup (via `get_first_issue_slug` method).
- `comicvine_url` (str, read-only): URL to character page on ComicVine.
- `short_description` (str, read-only): Brief description from ComicVine.
- `description` (str, read-only): Full HTML description via `description` property (sanitized and image-reflow aware).
- `download_link` (str, read-only): Absolute URL for downloading character's issues (context-aware via request).
- `download_size` (str, read-only): Total size of downloadable issues in human-readable format via `DownloadSizeMixin`.

#### SerializerMethodField methods

- `get_first_issue_name(obj: Character) -> str | None`
  - Returns the issue's `display_name` if `first_issue` is set, otherwise the stored `first_issue_name` text.
  - Handles cases where related issue may be deleted but name is retained.

- `get_first_issue_slug(obj: Character) -> str | None`
  - Returns the `slug` of the related first issue, or `None` if not found.

- `get_download_link(self, obj: Character) -> str`
  - Builds absolute URI using `request.build_absolute_uri()` with the character's `download_link` property.
  - Ensures links work in external contexts (mobile apps, emails, etc.).

#### Meta

- `model = Character`
- `fields` = `["slug", "name", "real_name", "image", "square_image", "publisher", "aliases", "birth", "gender", "powers", "first_issue_name", "first_issue_slug", "comicvine_url", "short_description", "description", "download_link", "download_size"]`

### `CharacterTechnicalInfoSerializer`

- Django REST Framework `ModelSerializer` subclass for technical/administrative character metadata.
- Restricted to staff and superuser access via `TechnicalInfoActionMixin` permission checks.
- Used by `CharacterViewSet.technical_info` custom action.

#### Fields

- `id` (int, read-only): Primary key in PostgreSQL database.
- `comicvine_id` (int, read-only): Unique identifier from ComicVine API.
- `comicvine_status` (str, read-only): Human-readable ComicVine synchronization status via `get_comicvine_status_display()` (maps `ComicvineStatus` choices: `"Not matched"`, `"Waiting in queue"`, `"Matched"`).
- `comicvine_last_match` (datetime, read-only): Timestamp of last successful ComicVine API synchronization (ISO 8601 format).
- `created_dt` (datetime, read-only): Record creation timestamp.
- `modified_dt` (datetime, read-only): Last modification timestamp.

#### Meta

- `model = Character`
- `fields` = `["id", "comicvine_id", "comicvine_status", "comicvine_last_match", "created_dt", "modified_dt"]`

## Usage context

- **`CharactersListSerializer`** is the default serializer for `/api/characters/` list/search responses.
- **`CharacterDetailSerializer`** is activated for `/api/characters/{slug}/` detail responses via `DetailSerializerMixin`.
- **`CharacterTechnicalInfoSerializer`** is used only for the `/api/characters/{slug}/technical-info/` admin action.