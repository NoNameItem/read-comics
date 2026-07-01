# MissingIssue Fixtures in `read_comics/missing_issues/tests/conftest.py`

## Summary

- [`missingissue_no_issues`](#missingissue_no_issues) - Single MissingIssue instance without related issues
- [`missingissue_with_issues`](#missingissue_with_issues) - Single MissingIssue instance with 1-2 related issues
- [`missing_issues_no_issues`](#missing_issues_no_issues) - List of 2-9 MissingIssue instances without issues
- [`missing_issues_with_issues`](#missing_issues_with_issues) - List of 2-9 MissingIssue instances with issues

## Reference

### missingissue_no_issues

**Type:** MissingIssue model instance | **Scope:** `function`

**Behavior:** Creates one MissingIssue using MissingIssueFactory without any related issues.

**When to use:** Testing missing_issues detail endpoint with missing relationships, testing list filtering.

### missingissue_with_issues

**Type:** MissingIssue model instance | **Scope:** `function`

**Behavior:** Creates one MissingIssue using MissingIssueFactory with 1-2 related issues randomly.

**When to use:** Testing missing_issues detail endpoint with full data, testing URL routing, testing ordering operations.

### missing_issues_no_issues

**Type:** List of MissingIssue model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 missing_issues using `MissingIssueFactory.create_batch(size=randrange(2, 10))`. None have related issues.

**When to use:** Testing `show-all=yes` filter, testing count endpoint with filtering.

### missing_issues_with_issues

**Type:** List of MissingIssue model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 missing_issues using `MissingIssueFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))`. Each has 1-2 related issues.

**When to use:** Testing list endpoint default behavior, testing ordering operations, testing pagination.

## Fixture Combinations

**Testing Filtering Behavior:**
```python
def test_filter_consistency(api_client, missing_issues_no_issues, missing_issues_with_issues):
    # Default - only shows missing_issues_with_issues
    # With show-all - shows both
```
