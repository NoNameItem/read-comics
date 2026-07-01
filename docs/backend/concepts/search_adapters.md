# Concept Search Adapter

## Summary

- [`ConceptSearchAdapter`](#conceptsearchadapter) — Full-text search integration for concepts

## Reference

### `ConceptSearchAdapter`

**Base Class:** `BaseSearchAdapter`

**Configuration:**

| Property | Value | Purpose |
|----------|-------|---------|
| `SECTION` | `"Concept"` | Display name in search results UI |
| `ICON` | `"fa-brain"` | FontAwesome icon for UI (brain icon) |

**Inherited Methods:**

All search functionality is inherited from `BaseSearchAdapter`:

- `get_title(obj: Concept) → str` — Returns concept name
- `get_description(obj: Concept) → str` — Returns short_description field
- `get_content(obj: Concept) → str` — Returns full searchable text (name, aliases, description)
- `get_meta(obj: Concept) → dict` — Returns metadata dictionary with slug, comicvine_id, etc.

**Usage:**

Automatically registered with django-watson search index. Concepts are indexed by name, aliases, descriptions, and searchable via the full-text search functionality.

**Example Metadata:**

```python
{
    "slug": "magic",
    "comicvine_id": 75632,
    "image_url": "https://...",
    "start_year": 1962
}
```