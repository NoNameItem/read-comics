# User Fixtures in `read_comics/users/tests/conftest.py`

## Summary

- [`user_no_issues`](#user_no_issues) - Single User instance without related issues
- [`user_with_issues`](#user_with_issues) - Single User instance with 1-2 related issues
- [`users_no_issues`](#users_no_issues) - List of 2-9 User instances without issues
- [`users_with_issues`](#users_with_issues) - List of 2-9 User instances with issues

## Reference

### user_no_issues

**Type:** User model instance | **Scope:** `function`

**Behavior:** Creates one User using UserFactory without any related issues.

**When to use:** Testing users detail endpoint with missing relationships, testing list filtering.

### user_with_issues

**Type:** User model instance | **Scope:** `function`

**Behavior:** Creates one User using UserFactory with 1-2 related issues randomly.

**When to use:** Testing users detail endpoint with full data, testing URL routing, testing ordering operations.

### users_no_issues

**Type:** List of User model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 users using `UserFactory.create_batch(size=randrange(2, 10))`. None have related issues.

**When to use:** Testing `show-all=yes` filter, testing count endpoint with filtering.

### users_with_issues

**Type:** List of User model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 users using `UserFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))`. Each has 1-2 related issues.

**When to use:** Testing list endpoint default behavior, testing ordering operations, testing pagination.

## Fixture Combinations

**Testing Filtering Behavior:**
```python
def test_filter_consistency(api_client, users_no_issues, users_with_issues):
    # Default - only shows users_with_issues
    # With show-all - shows both
```
