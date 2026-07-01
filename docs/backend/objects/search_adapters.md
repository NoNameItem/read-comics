# Objects Search Adapters

## Summary

- [`ObjectSearchAdapter`](#objectsearchadapter) — Provides full-text search integration for artifacts and equipment

## Reference

### `ObjectSearchAdapter`

Integrates Object model with django-watson full-text search system.

**Configuration:**

```python
SECTION = "Object"
ICON = "fa-swords"
```

**Inherited Methods (from BaseSearchAdapter):**

The adapter inherits search behavior from `BaseSearchAdapter`:

- `get_title(obj)` — Returns searchable title
- `get_description(obj)` — Returns searchable description
- `get_content(obj)` — Returns full text content for indexing
- `get_meta(obj)` — Returns search result metadata

**Default Behavior:**

- Title from `name` field
- Description from `short_description` field
- Content from full text fields (aliases, html_description, etc.)
- Icon: crossed swords (fa-swords)

**Usage:**

Objects are indexed by django-watson and searchable via:
- Global full-text search endpoint
- Filtering search results by section "Object"
- Icon display in search results
