# StoryArc Factories in `read_comics/story_arcs/tests/factories.py`

## Summary

- [`StoryArcFactory`](#story_arcsfactory) - Factory for creating StoryArc instances

## Reference

### StoryArcFactory

Factory class for generating StoryArc model instances with realistic test data.

**Extends:** [`ComicvineSyncModelFactory`](../../../utils/test_utils_factories.md#comicvinesyncmodelfactory)

**Location:** `read_comics/story_arcs/tests/factories.py`

**Meta Configuration:**
- Model: `StoryArc`
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
- **Behavior:** Creates N Issue instances and associates them with the story_arcs
- **Usage:** `StoryArcFactory(add_issues=5)`

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
story_arcs = StoryArcFactory()

# With issues (if applicable)
story_arcs = StoryArcFactory(add_issues=10)

# Batch creation
story_arcs_list = StoryArcFactory.create_batch(size=20)
```

#### Dependencies

- `read_comics.story_arcs.models.StoryArc`
- `IssueFactory` - For creating relationships (when applicable)
