# Volumes Search Adapter

## Summary

- `VolumeSearchAdapter` — Full-text search integration for volumes with custom title formatting

## Reference

### VolumeSearchAdapter

Integrates Volume model with full-text search via django-watson.

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `SECTION` | `"Volume"` | Display name in search results UI |
| `ICON` | `"fa-book-spells"` | FontAwesome book with spells icon for search results |

#### Custom Methods

| Method | Signature | Description |
|---|---|---|
| `get_title()` | `(obj: Volume) → str` | Custom title formatting for search results |

#### get_title() Implementation

Returns formatted string combining:
- Volume name
- Start year
- Aliases on separate line

Format: `"Name Year\nAliases"`

Example output:
```
The Amazing Spider-Man 1963
Spider-Man|Amazing Spider-Man|ASM
```

#### Behavior

- Inherits from `BaseSearchAdapter`
- Searches across searchable fields in model
- Returns results grouped under "Volume" section
- Each result shows with book/spells icon
- Custom title includes year and aliases for context

## Details

### Search Integration

Volumes are searchable by:
- Name
- Aliases
- Short description
- HTML description
- Custom title (includes year for better discovery)

### Result Display

When volumes appear in search results:
- Section header: "Volume"
- Icon: Book with spells icon (`fa-book-spells`)
- Result title: Custom formatted with name, year, and aliases
- Result link: Points to volume detail page (slug)

### Title Formatting Benefit

Custom `get_title()` improves search result relevance:
- Shows publication year immediately
- Displays aliases for alternate names
- Multi-line format improves readability
- Helps distinguish between volume versions/reboots

## References

- [../models.md](../models.md) — Volume model (fields included in search)
- [../../search/search_adapters.md](../../search/search_adapters.md) — BaseSearchAdapter reference