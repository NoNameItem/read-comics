# Search adapter in `characters/search_adapters.py`

## Summary

- [`CharacterSearchAdapter`](#charactersearchadapter) — django-watson search adapter for [`Character`](models.md#character) models; configures full-text indexing with aliases support, display title, description, metadata, and UI presentation (section name and icon).

## Reference

### `CharacterSearchAdapter`

- Subclass of [`BaseSearchAdapter`](../search/search_adapters.md) that integrates [`Character`](models.md#character) models with django-watson full-text search.
- Registered automatically via Django's app configuration when watson indexes are built.
- Provides configuration for how character data is indexed, displayed in search results, and presented in the UI.

#### Class attributes

- `SECTION = "Character"`: Section/category label displayed in search result grouping. Used to organize results by entity type.
- `ICON = "fa-bat"`: Font Awesome icon class name (Font Awesome 4/5 prefix `fa-` with `bat` icon) for visual representation in search results.

#### Inherited behavior

- Inherits from [`BaseSearchAdapter`](../search/search_adapters.md) which extends watson's `SearchAdapter`.
- Uses base adapter methods:
  - `get_title(obj)` — returns character name plus aliases if available; aliases are separated by newline.
  - `get_description(obj)` — returns `short_description` field from character or empty string if not available.
  - `get_content(obj)` — returns empty string (no additional searchable content beyond title/description).
  - `get_meta(obj)` — aggregates metadata dict including `section`, `search_display` (string representation), `icon`, and `img_url` (thumbnail image from `square_tiny` property).

## How it works

When django-watson's search index is built:

1. All `Character` instances are indexed with full-text search support.
2. The adapter extracts title (name + aliases) and description (short_description) for each character.
3. Metadata is attached including the section label ("Character"), icon class ("fa-bat"), and thumbnail image.
4. Search queries match against indexed titles/descriptions and return results grouped by section.
5. UI displays results with the configured icon, section label, and character thumbnail.

## Example search result

When searching for "Spider-Man", watson indexes and retrieves:

```json
{
  "title": "Spider-Man\nSpidey, Web-Slinger",
  "description": "Your friendly neighborhood Spider-Man.",
  "section": "Character",
  "icon": "fa-bat",
  "img_url": "https://cdn.example.com/spider-man-tiny.jpg",
  "search_display": "Spider-Man (Marvel)"
}
```

## Related documentation

- [`BaseSearchAdapter` base class](../search/search_adapters.md)
- [`Character` model](models.md#character)
- [Full-text search overview](../search/README.md)