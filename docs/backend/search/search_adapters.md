# Search adapter in `search/search_adapters.py`

## Summary

- [`BaseSearchAdapter`](#basesearchadapter) — base watson search adapter class providing shared indexing configuration and metadata extraction for all searchable domain models; subclassed by app-specific adapters (e.g., `CharacterSearchAdapter`).

## Reference

### `BaseSearchAdapter`

- Extends django-watson's `SearchAdapter` class to provide consistent search behavior across all searchable entities.
- Defines common methods for extracting title, description, content, and metadata from domain models.
- Subclassed by entity-specific adapters (Character, Issue, Volume, etc.) which configure section labels and icons.

#### Class attributes

- `SECTION = None`: Logical section/category name displayed in search result grouping. Must be overridden by subclasses (e.g., "Character", "Issue").
- `ICON = None`: Font Awesome icon class for visual representation in search results (e.g., "fa-bat", "fa-book"). Must be overridden by subclasses.

#### Methods

- `get_title(self, obj)` — extracts searchable title from a model instance.
  - Returns character/entity name combined with aliases if available; aliases are separated by newline character.
  - If `aliases` attribute doesn't exist or is empty, returns just the name.
  - Used as primary search match target.

- `get_description(self, obj)` — extracts brief description for search result display.
  - Returns `short_description` field if available, otherwise empty string.
  - Displayed alongside the title in search results.

- `get_content(self, obj)` — extracts searchable content body.
  - Returns empty string by default; subclasses may override to add additional searchable content.
  - Not used in basic character/entity search.

- `get_meta(self, obj)` — builds metadata dictionary for search result presentation.
  - Calls parent `SearchAdapter.get_meta()` to get watson base metadata.
  - Adds custom fields:
    - `section`: Value of class attribute `SECTION` (e.g., "Character").
    - `search_display`: String representation of the object (via `str(obj)`).
    - `icon`: Value of class attribute `ICON` (Font Awesome class).
    - `img_url`: Thumbnail image URL from `square_tiny` property (assumes object is `ImageMixin` subclass).
  - Returns enriched metadata dict.

## Search adapter registration

Adapters are registered automatically when the Django app is loaded:

```python
# in app's AppConfig.ready() or via registration signal
from watson import search
search.register(CharacterSearchAdapter(), fields=['name', 'aliases', 'short_description'])
```

## Example metadata output

For a Character instance with all metadata fields:

```python
{
  'section': 'Character',
  'search_display': 'Spider-Man (Marvel)',
  'icon': 'fa-bat',
  'img_url': 'https://cdn.example.com/spider-man-tiny.jpg',
  # ... watson base metadata fields
}
```

## Subclasses

- [`CharacterSearchAdapter`](../characters/search_adapters.md#charactersearchadapter) — configures search for Character models.
- Similar adapters exist for Issue, Volume, Publisher, and other searchable entities.

## Related documentation

- [django-watson search framework](https://github.com/etianen/django-watson)
- [Search module README](README.md)