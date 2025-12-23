# Story Arcs Search Adapter

## Summary

- `StoryArcSearchAdapter` — Full-text search integration for story arcs

## Reference

### StoryArcSearchAdapter

Integrates StoryArc model with full-text search via django-watson.

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `SECTION` | `"Story Arc"` | Display name in search results UI |
| `ICON` | `"fa-books"` | FontAwesome icon for search result display |

#### Behavior

- Inherits from `BaseSearchAdapter`
- Searches across searchable fields defined in model
- Returns results grouped under "Story Arc" section
- Each result shows with books icon

## Details

### Search Integration

Story arcs are searchable by:
- Name
- Aliases
- Short description
- HTML description

Search queries like "dark phoenix" or "saga" will find relevant story arcs.

### Result Display

When story arcs appear in search results:
- Section header: "Story Arc"
- Icon: Books/library icon (`fa-books`)
- Result title: Story arc name
- Result link: Points to story arc detail page (slug)

## References

- [../models.md](../models.md) — StoryArc model (fields included in search)
- [../../search/search_adapters.md](../../search/search_adapters.md) — BaseSearchAdapter reference