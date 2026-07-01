# Object Fixtures in `read_comics/objects/tests/conftest.py`

## Summary

- [`object_no_issues`](#object_no_issues) - Single Object instance without related issues
- [`object_with_issues`](#object_with_issues) - Single Object instance with 1-2 related issues
- [`objects_no_issues`](#objects_no_issues) - List of 2-9 Object instances without issues
- [`objects_with_issues`](#objects_with_issues) - List of 2-9 Object instances with issues

## Reference

### object_no_issues

**Type:** Object model instance | **Scope:** `function`

**Behavior:** Creates one Object using ObjectFactory without any related issues.

**When to use:** Testing objects detail endpoint with missing relationships, testing list filtering.

### object_with_issues

**Type:** Object model instance | **Scope:** `function`

**Behavior:** Creates one Object using ObjectFactory with 1-2 related issues randomly.

**When to use:** Testing objects detail endpoint with full data, testing URL routing, testing ordering operations.

### objects_no_issues

**Type:** List of Object model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 objects using `ObjectFactory.create_batch(size=randrange(2, 10))`. None have related issues.

**When to use:** Testing `show-all=yes` filter, testing count endpoint with filtering.

### objects_with_issues

**Type:** List of Object model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 objects using `ObjectFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))`. Each has 1-2 related issues.

**When to use:** Testing list endpoint default behavior, testing ordering operations, testing pagination.

## Fixture Combinations

**Testing Filtering Behavior:**
```python
def test_filter_consistency(api_client, objects_no_issues, objects_with_issues):
    # Default - only shows objects_with_issues
    # With show-all - shows both
```
