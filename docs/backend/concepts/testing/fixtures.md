# Concept Fixtures in `read_comics/concepts/tests/conftest.py`

## Summary

- [`concept_no_issues`](#concept_no_issues) - Single Concept instance without related issues
- [`concept_with_issues`](#concept_with_issues) - Single Concept instance with 1-2 related issues
- [`concepts_no_issues`](#concepts_no_issues) - List of 2-9 Concept instances without issues
- [`concepts_with_issues`](#concepts_with_issues) - List of 2-9 Concept instances with issues

## Reference

### concept_no_issues

**Type:** Concept model instance | **Scope:** `function`

**Behavior:** Creates one Concept using ConceptFactory without any related issues.

**When to use:** Testing concept detail endpoint with missing `first_issue`, testing list filtering (concepts without issues excluded by default).

### concept_with_issues

**Type:** Concept model instance | **Scope:** `function`

**Behavior:** Creates one Concept using ConceptFactory with 1-2 related issues randomly. Randomly selects one issue as `first_issue`.

**When to use:** Testing concept detail endpoint with full data, testing URL routing with valid concept slug, testing ordering and filtering operations.

### concepts_no_issues

**Type:** List of Concept model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 concepts using `ConceptFactory.create_batch(size=randrange(2, 10))`. None have related issues.

**When to use:** Testing `show-all=yes` filter on list endpoint, testing count endpoint with `show-all=yes` filter.

### concepts_with_issues

**Type:** List of Concept model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 concepts using `ConceptFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))`. Each concept has 1-2 related issues randomly.

**When to use:** Testing list endpoint default behavior, testing count endpoint default behavior, testing ordering operations (by name, issues_count, volumes_count).

## Fixture Combinations

**Testing Filtering Behavior:**
```python
def test_filter_consistency(api_client, concepts_no_issues, concepts_with_issues):
    # Default - only shows concepts_with_issues
    # With show-all - shows both
```