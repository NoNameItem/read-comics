# Teams Search Adapter

## Summary

- `TeamSearchAdapter` — Full-text search integration for teams

## Reference

### TeamSearchAdapter

Integrates Team model with full-text search via django-watson.

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `SECTION` | `"Team"` | Display name in search results UI |
| `ICON` | `"fa-users"` | FontAwesome users icon for search result display |

#### Behavior

- Inherits from `BaseSearchAdapter`
- Searches across searchable fields defined in model
- Returns results grouped under "Team" section
- Each result shows with users icon

## Details

### Search Integration

Teams are searchable by:
- Name
- Aliases
- Short description
- HTML description

Search queries like "avengers" or "x-men" will find relevant teams.

### Result Display

When teams appear in search results:
- Section header: "Team"
- Icon: Users/team icon (`fa-users`)
- Result title: Team name
- Result link: Points to team list filtered/detail page (slug)

## References

- [../models.md](../models.md) — Team model (fields included in search)
- [../../search/search_adapters.md](../../search/search_adapters.md) — BaseSearchAdapter reference