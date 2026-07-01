# Issues Search Adapters

## Summary

- [`IssueSearchAdapter`](#issuesearchadapter) — Provides full-text search integration for comic issues

## Reference

### `IssueSearchAdapter`

Integrates Issue model with django-watson full-text search system.

**Configuration:**

```python
SECTION = "Issue"
ICON = "fa-book-open"
```

**Inherited Methods (from BaseSearchAdapter):**

The adapter inherits search behavior from `BaseSearchAdapter`:

- `get_title(obj)` — Returns searchable title
- `get_description(obj)` — Returns searchable description
- `get_content(obj)` — Returns full text content for indexing
- `get_meta(obj)` — Returns search result metadata

**Implementation:**

#### `get_title(obj)`
Returns `obj.get_full_name()` — formatted name like "Volume Name (2020) #42 Title".

**Default Behavior:**

Other methods use `BaseSearchAdapter` defaults:
- Description from `short_description` field
- Content from full text fields (html_description, etc.)
- Meta information for search result display

**Usage:**

Issues are indexed by django-watson and searchable via:
- Global full-text search endpoint
- Filtering search results by section "Issue"
- Icon display in search results (book icon)
