# Team Fixtures in `read_comics/teams/tests/conftest.py`

## Summary

- [`team_no_issues`](#team_no_issues) - Single Team instance without related issues
- [`team_with_issues`](#team_with_issues) - Single Team instance with 1-2 related issues
- [`teams_no_issues`](#teams_no_issues) - List of 2-9 Team instances without issues
- [`teams_with_issues`](#teams_with_issues) - List of 2-9 Team instances with issues

## Reference

### team_no_issues

**Type:** Team model instance | **Scope:** `function`

**Behavior:** Creates one Team using TeamFactory without any related issues.

**When to use:** Testing teams detail endpoint with missing relationships, testing list filtering.

### team_with_issues

**Type:** Team model instance | **Scope:** `function`

**Behavior:** Creates one Team using TeamFactory with 1-2 related issues randomly.

**When to use:** Testing teams detail endpoint with full data, testing URL routing, testing ordering operations.

### teams_no_issues

**Type:** List of Team model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 teams using `TeamFactory.create_batch(size=randrange(2, 10))`. None have related issues.

**When to use:** Testing `show-all=yes` filter, testing count endpoint with filtering.

### teams_with_issues

**Type:** List of Team model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 teams using `TeamFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))`. Each has 1-2 related issues.

**When to use:** Testing list endpoint default behavior, testing ordering operations, testing pagination.

## Fixture Combinations

**Testing Filtering Behavior:**
```python
def test_filter_consistency(api_client, teams_no_issues, teams_with_issues):
    # Default - only shows teams_with_issues
    # With show-all - shows both
```
