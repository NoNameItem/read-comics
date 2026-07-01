# Locations Search Adapters

## Summary

- [`LocationSearchAdapter`](#locationsearchadapter) — Provides full-text search integration for geographic locations

## Reference

### `LocationSearchAdapter`

Integrates Location model with django-watson full-text search system.

**Configuration:**

```python
SECTION = "Location"
ICON = "fa-map-marker-alt"
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
- Icon: map marker (fa-map-marker-alt)

**Usage:**

Locations are indexed by django-watson and searchable via:
- Global full-text search endpoint
- Filtering search results by section "Location"
- Icon display in search results
