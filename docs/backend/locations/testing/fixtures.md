# Location Fixtures in `read_comics/locations/tests/conftest.py`

## Summary

- [`location_no_issues`](#location_no_issues) - Single Location instance without related issues
- [`location_with_issues`](#location_with_issues) - Single Location instance with 1-2 related issues
- [`locations_no_issues`](#locations_no_issues) - List of 2-9 Location instances without issues
- [`locations_with_issues`](#locations_with_issues) - List of 2-9 Location instances with issues

## Reference

### location_no_issues

**Type:** Location model instance | **Scope:** `function`

**Behavior:** Creates one Location using LocationFactory without any related issues.

**When to use:** Testing locations detail endpoint with missing relationships, testing list filtering.

### location_with_issues

**Type:** Location model instance | **Scope:** `function`

**Behavior:** Creates one Location using LocationFactory with 1-2 related issues randomly.

**When to use:** Testing locations detail endpoint with full data, testing URL routing, testing ordering operations.

### locations_no_issues

**Type:** List of Location model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 locations using `LocationFactory.create_batch(size=randrange(2, 10))`. None have related issues.

**When to use:** Testing `show-all=yes` filter, testing count endpoint with filtering.

### locations_with_issues

**Type:** List of Location model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 locations using `LocationFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))`. Each has 1-2 related issues.

**When to use:** Testing list endpoint default behavior, testing ordering operations, testing pagination.

## Fixture Combinations

**Testing Filtering Behavior:**
```python
def test_filter_consistency(api_client, locations_no_issues, locations_with_issues):
    # Default - only shows locations_with_issues
    # With show-all - shows both
```
