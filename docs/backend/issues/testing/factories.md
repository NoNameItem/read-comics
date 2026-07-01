# Issue Factories in `read_comics/issues/tests/factories.py`

## Summary

- [`IssueFactory`](#issuesfactory) - Factory for creating Issue instances

## Reference

### IssueFactory

Factory class for generating Issue model instances with realistic test data.

**Extends:** [`ComicvineSyncModelFactory`](../../../utils/test_utils_factories.md#comicvinesyncmodelfactory)

**Location:** `read_comics/issues/tests/factories.py`

**Meta Configuration:**
- Model: `Issue`
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
- **Behavior:** Creates N Issue instances and associates them with the issues
- **Usage:** `IssueFactory(add_issues=5)`

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
issues = IssueFactory()

# With issues (if applicable)
issues = IssueFactory(add_issues=10)

# Batch creation
issues_list = IssueFactory.create_batch(size=20)
```

#### Dependencies

- `read_comics.issues.models.Issue`
- `IssueFactory` - For creating relationships (when applicable)
