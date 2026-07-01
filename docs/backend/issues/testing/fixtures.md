# Issue Fixtures in `read_comics/issues/tests/conftest.py`

## Summary

- [`issue_no_issues`](#issue_no_issues) - Single Issue instance without related issues
- [`issue_with_issues`](#issue_with_issues) - Single Issue instance with 1-2 related issues
- [`issues_no_issues`](#issues_no_issues) - List of 2-9 Issue instances without issues
- [`issues_with_issues`](#issues_with_issues) - List of 2-9 Issue instances with issues

## Reference

### issue_no_issues

**Type:** Issue model instance | **Scope:** `function`

**Behavior:** Creates one Issue using IssueFactory without any related issues.

**When to use:** Testing issues detail endpoint with missing relationships, testing list filtering.

### issue_with_issues

**Type:** Issue model instance | **Scope:** `function`

**Behavior:** Creates one Issue using IssueFactory with 1-2 related issues randomly.

**When to use:** Testing issues detail endpoint with full data, testing URL routing, testing ordering operations.

### issues_no_issues

**Type:** List of Issue model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 issues using `IssueFactory.create_batch(size=randrange(2, 10))`. None have related issues.

**When to use:** Testing `show-all=yes` filter, testing count endpoint with filtering.

### issues_with_issues

**Type:** List of Issue model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 issues using `IssueFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))`. Each has 1-2 related issues.

**When to use:** Testing list endpoint default behavior, testing ordering operations, testing pagination.

## Fixture Combinations

**Testing Filtering Behavior:**
```python
def test_filter_consistency(api_client, issues_no_issues, issues_with_issues):
    # Default - only shows issues_with_issues
    # With show-all - shows both
```
