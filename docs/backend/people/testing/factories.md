# Person Factories in `read_comics/people/tests/factories.py`

## Summary

- [`PersonFactory`](#peoplefactory) - Factory for creating Person instances

## Reference

### PersonFactory

Factory class for generating Person model instances with realistic test data.

**Extends:** [`ComicvineSyncModelFactory`](../../../utils/test_utils_factories.md#comicvinesyncmodelfactory)

**Location:** `read_comics/people/tests/factories.py`

**Meta Configuration:**
- Model: `Person`
- Excluded fields: Intermediate fields like `aliases_list`

#### Parameters

Factory uses Faker generators for creating realistic test data. Key parameters include:
- `name` - Generated using Faker
- `short_description` - Generated paragraph
- `aliases` - Newline-joined list of aliases
- Additional entity-specific fields

#### Post-Generation Hooks

**`add_issues(create, extracted, **kwargs)`** (if applicable)
- **Trigger:** Pass `add_issues=N` parameter to factory
- **Behavior:** Creates N Issue instances and associates them with the people
- **Usage:** `PersonFactory(add_issues=5)`

#### Inherited Fields

From `ComicvineSyncModelFactory`:
- `comicvine_id` - Unique ComicVine API identifier
- `comicvine_status` - Sync status
- `slug` - URL-safe identifier
- `image` - Image URL
- `description` - Full description

#### Usage Examples

```python
# Basic creation
people = PersonFactory()

# With issues (if applicable)
people = PersonFactory(add_issues=10)

# Batch creation
people_list = PersonFactory.create_batch(size=20)
```

#### Dependencies

- `read_comics.people.models.Person`
- `IssueFactory` - For creating relationships (when applicable)
