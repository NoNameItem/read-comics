# Character Factories in `read_comics/characters/tests/factories.py`

## Summary

- [`CharacterFactory`](#characterfactory) - Factory for creating Character instances with configurable issues and powers

## Reference

### CharacterFactory

Factory class for generating Character model instances with realistic test data.

**Extends:** [`ComicvineSyncModelFactory`](../../../utils/test_utils_factories.md#comicvinesyncmodelfactory)

**Location:** `read_comics/characters/tests/factories.py`

**Meta Configuration:**
- Model: `Character`
- Excluded fields: `aliases_list` (intermediate field for generating aliases)

#### Parameters

| Field | Type | Generator | Purpose |
|---|---|---|---|
| `name` | String | `Faker("name")` | Character display name (randomly generated person name) |
| `real_name` | String | `Faker("name")` | Character's real/civilian name |
| `short_description` | Text | `Faker("paragraph")` | Brief character description |
| `gender` | Integer | `FuzzyChoice(Character.Gender.choices)` | Gender choice from Character.Gender enum |
| `birth` | Date | `Faker("date_this_century")` | Birth date within current century |
| `publisher` | ForeignKey | `SubFactory(PublisherFactory)` | Related publisher instance |
| `first_issue_name` | String | `Faker("word")` | Name of character's first appearance |
| `aliases_list` | List | `Faker("words", nb=6)` | Intermediate list of alias words (excluded from database) |
| `aliases` | Text | `LazyAttribute` | Newline-joined string from `aliases_list` |

#### Post-Generation Hooks

**`add_issues(create, extracted, **kwargs)`**
- **Trigger:** Pass `add_issues=N` parameter to factory
- **Behavior:**
  - Creates N Issue instances using IssueFactory
  - Associates all created issues with the character via `issues` M2M relationship
  - Randomly selects one issue to set as `first_issue`
  - Saves character instance with updated first_issue
- **Usage:** `CharacterFactory(add_issues=5)` creates character with 5 related issues

**`add_powers(create, extracted, **kwargs)`**
- **Trigger:** Automatically runs on every created instance
- **Behavior:**
  - Creates 1-3 Power instances using PowerFactory (random count)
  - Associates powers with character via `powers` M2M relationship
- **Usage:** Automatic - every character gets random powers

#### Inherited Fields

From `ComicvineSyncModelFactory`:
- `comicvine_id` - Unique ComicVine API identifier
- `comicvine_status` - Sync status (matched, pending, etc.)
- `slug` - URL-safe identifier
- `image` - Character image URL
- `description` - Full character description

#### Usage Examples

**Basic character creation:**
```python
character = CharacterFactory()
# Creates character with random data, publisher, and 1-3 powers
```

**Character with specific issues count:**
```python
character = CharacterFactory(add_issues=10)
# Creates character with 10 related issues, one set as first_issue
```

**Character with custom data:**
```python
character = CharacterFactory(
    name="Spider-Man",
    real_name="Peter Parker",
    gender=Character.Gender.MALE,
    add_issues=50
)
```

**Batch creation:**
```python
characters = CharacterFactory.create_batch(size=20, add_issues=5)
# Creates 20 characters, each with 5 issues
```

**Character without issues:**
```python
character = CharacterFactory(add_issues=0)
# Explicitly prevents issue creation (use character_no_issues fixture instead)
```

#### Database Behavior

- Creates new Character instance on every call (no deduplication)
- Automatically creates related Publisher via SubFactory
- Automatically creates related Powers (1-3 random count)
- Optionally creates related Issues via `add_issues` parameter

#### Dependencies

**Factory Dependencies:**
- `PublisherFactory` - For creating publisher relationship
- `PowerFactory` - For creating power relationships
- `IssueFactory` - For creating issue relationships (when `add_issues` used)

**Model Import:**
- `read_comics.characters.models.Character`

#### Common Patterns

**Creating characters with varying issue counts:**
```python
from random import randrange

characters = [
    CharacterFactory(add_issues=randrange(1, 10))
    for _ in range(5)
]
```

**Creating character without auto-generated powers:**
Not directly supported - powers always generated. To avoid, manually clear after creation:
```python
character = CharacterFactory()
character.powers.clear()
```