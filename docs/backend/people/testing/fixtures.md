# Person Fixtures in `read_comics/people/tests/conftest.py`

## Summary

- [`person_no_issues`](#person_no_issues) - Single Person instance without related issues
- [`person_with_issues`](#person_with_issues) - Single Person instance with 1-2 related issues
- [`people_no_issues`](#people_no_issues) - List of 2-9 Person instances without issues
- [`people_with_issues`](#people_with_issues) - List of 2-9 Person instances with issues

## Reference

### person_no_issues

**Type:** Person model instance | **Scope:** `function`

**Behavior:** Creates one Person using PersonFactory without any related issues.

**When to use:** Testing people detail endpoint with missing relationships, testing list filtering.

### person_with_issues

**Type:** Person model instance | **Scope:** `function`

**Behavior:** Creates one Person using PersonFactory with 1-2 related issues randomly.

**When to use:** Testing people detail endpoint with full data, testing URL routing, testing ordering operations.

### people_no_issues

**Type:** List of Person model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 people using `PersonFactory.create_batch(size=randrange(2, 10))`. None have related issues.

**When to use:** Testing `show-all=yes` filter, testing count endpoint with filtering.

### people_with_issues

**Type:** List of Person model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 people using `PersonFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))`. Each has 1-2 related issues.

**When to use:** Testing list endpoint default behavior, testing ordering operations, testing pagination.

## Fixture Combinations

**Testing Filtering Behavior:**
```python
def test_filter_consistency(api_client, people_no_issues, people_with_issues):
    # Default - only shows people_with_issues
    # With show-all - shows both
```
