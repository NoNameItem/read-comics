# Publisher Fixtures in `read_comics/publishers/tests/conftest.py`

## Summary

- [`publisher_no_issues`](#publisher_no_issues) - Single Publisher instance without related issues
- [`publisher_with_issues`](#publisher_with_issues) - Single Publisher instance with 1-2 related issues
- [`publishers_no_issues`](#publishers_no_issues) - List of 2-9 Publisher instances without issues
- [`publishers_with_issues`](#publishers_with_issues) - List of 2-9 Publisher instances with issues

## Reference

### publisher_no_issues

**Type:** Publisher model instance | **Scope:** `function`

**Behavior:** Creates one Publisher using PublisherFactory without any related issues.

**When to use:** Testing publishers detail endpoint with missing relationships, testing list filtering.

### publisher_with_issues

**Type:** Publisher model instance | **Scope:** `function`

**Behavior:** Creates one Publisher using PublisherFactory with 1-2 related issues randomly.

**When to use:** Testing publishers detail endpoint with full data, testing URL routing, testing ordering operations.

### publishers_no_issues

**Type:** List of Publisher model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 publishers using `PublisherFactory.create_batch(size=randrange(2, 10))`. None have related issues.

**When to use:** Testing `show-all=yes` filter, testing count endpoint with filtering.

### publishers_with_issues

**Type:** List of Publisher model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 publishers using `PublisherFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))`. Each has 1-2 related issues.

**When to use:** Testing list endpoint default behavior, testing ordering operations, testing pagination.

## Fixture Combinations

**Testing Filtering Behavior:**
```python
def test_filter_consistency(api_client, publishers_no_issues, publishers_with_issues):
    # Default - only shows publishers_with_issues
    # With show-all - shows both
```
