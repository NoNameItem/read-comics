# Concept Factories in `read_comics/concepts/tests/factories.py`

## Summary

- [`ConceptFactory`](#conceptfactory) - Factory for creating Concept instances with configurable issues

## Reference

### ConceptFactory

Factory class for generating Concept model instances with realistic test data.

**Extends:** [`ComicvineSyncModelFactory`](../../../utils/test_utils_factories.md#comicvinesyncmodelfactory)

**Location:** `read_comics/concepts/tests/factories.py`

**Meta Configuration:**
- Model: `Concept`
- Excluded fields: `aliases_list`, `start_year_str` (intermediate fields)

#### Parameters

| Field | Type | Generator | Purpose |
|---|---|---|---|
| `name` | String | `Faker("word")` | Concept name |
| `short_description` | Text | `Faker("paragraph")` | Brief concept description |
| `start_year_str` | String | `Faker("year")` | Year as string (intermediate, excluded from DB) |
| `start_year` | Integer | `LazyAttribute` | Converts `start_year_str` to integer |
| `aliases_list` | List | `Faker("words", nb=6)` | List of alias words (intermediate, excluded from DB) |
| `aliases` | Text | `LazyAttribute` | Newline-joined string from `aliases_list` |

#### Post-Generation Hooks

**`add_issues(create, extracted, **kwargs)`**
- **Trigger:** Pass `add_issues=N` parameter to factory
- **Behavior:**
  - Creates N Issue instances using IssueFactory
  - Associates all created issues with the concept via `issues` M2M relationship
  - Randomly selects one issue to set as `first_issue`
  - Saves concept instance with updated first_issue
- **Usage:** `ConceptFactory(add_issues=5)` creates concept with 5 related issues

#### Inherited Fields

From `ComicvineSyncModelFactory`:
- `comicvine_id` - Unique ComicVine API identifier
- `comicvine_status` - Sync status
- `slug` - URL-safe identifier
- `image` - Concept image URL
- `description` - Full concept description

#### Usage Examples

**Basic concept creation:**
```python
concept = ConceptFactory()
# Creates concept with random data, no issues
```

**Concept with specific issues count:**
```python
concept = ConceptFactory(add_issues=10)
# Creates concept with 10 related issues
```

**Batch creation:**
```python
concepts = ConceptFactory.create_batch(size=20, add_issues=5)
# Creates 20 concepts, each with 5 issues
```

#### Dependencies

- `IssueFactory` - For creating issue relationships (when `add_issues` used)
- `read_comics.concepts.models.Concept`