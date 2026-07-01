# People Search Adapters

## Summary

- **`PersonSearchAdapter`** — Full-text search integration for creators with people icon

## Reference

### PersonSearchAdapter

Enables full-text search for Person model via django-watson integration.

**Configuration**:
- **Section**: `Person`
- **Icon**: `fa-people-carry` (Font Awesome icon class)

**Search scope**: All `Person` instances indexed by django-watson, searchable by name, aliases, description, and other indexed fields.

**Usage**: Integrated into global search functionality; queries return persons matching search terms with people-specific icon/styling in results.