# MissingIssue Factories in `read_comics/missing_issues/tests/factories.py`

## Summary

- [`MissingIssueFactory`](#missing_issuesfactory) - Factory for creating MissingIssue instances

## Reference

### MissingIssueFactory

Factory class for generating MissingIssue model instances with realistic test data.

**Extends:** [`ComicvineSyncModelFactory`](../../../utils/test_utils_factories.md#comicvinesyncmodelfactory)

**Location:** `read_comics/missing_issues/tests/factories.py`

**Meta Configuration:**
- Model: `MissingIssue`
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
- **Behavior:** Creates N Issue instances and associates them with the missing_issues
- **Usage:** `MissingIssueFactory(add_issues=5)`

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
missing_issues = MissingIssueFactory()

# With issues (if applicable)
missing_issues = MissingIssueFactory(add_issues=10)

# Batch creation
missing_issues_list = MissingIssueFactory.create_batch(size=20)
```

#### Dependencies

- `read_comics.missing_issues.models.MissingIssue`
- `IssueFactory` - For creating relationships (when applicable)
