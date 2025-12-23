# Location Factories in `read_comics/locations/tests/factories.py`

## Summary

- [`LocationFactory`](#locationsfactory) - Factory for creating Location instances

## Reference

### LocationFactory

Factory class for generating Location model instances with realistic test data.

**Extends:** [`ComicvineSyncModelFactory`](../../../utils/test_utils_factories.md#comicvinesyncmodelfactory)

**Location:** `read_comics/locations/tests/factories.py`

**Meta Configuration:**
- Model: `Location`
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
- **Behavior:** Creates N Issue instances and associates them with the locations
- **Usage:** `LocationFactory(add_issues=5)`

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
locations = LocationFactory()

# With issues (if applicable)
locations = LocationFactory(add_issues=10)

# Batch creation
locations_list = LocationFactory.create_batch(size=20)
```

#### Dependencies

- `read_comics.locations.models.Location`
- `IssueFactory` - For creating relationships (when applicable)
