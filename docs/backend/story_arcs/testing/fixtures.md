# StoryArc Fixtures in `read_comics/story_arcs/tests/conftest.py`

## Summary

- [`storyarc_no_issues`](#storyarc_no_issues) - Single StoryArc instance without related issues
- [`storyarc_with_issues`](#storyarc_with_issues) - Single StoryArc instance with 1-2 related issues
- [`story_arcs_no_issues`](#story_arcs_no_issues) - List of 2-9 StoryArc instances without issues
- [`story_arcs_with_issues`](#story_arcs_with_issues) - List of 2-9 StoryArc instances with issues

## Reference

### storyarc_no_issues

**Type:** StoryArc model instance | **Scope:** `function`

**Behavior:** Creates one StoryArc using StoryArcFactory without any related issues.

**When to use:** Testing story_arcs detail endpoint with missing relationships, testing list filtering.

### storyarc_with_issues

**Type:** StoryArc model instance | **Scope:** `function`

**Behavior:** Creates one StoryArc using StoryArcFactory with 1-2 related issues randomly.

**When to use:** Testing story_arcs detail endpoint with full data, testing URL routing, testing ordering operations.

### story_arcs_no_issues

**Type:** List of StoryArc model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 story_arcs using `StoryArcFactory.create_batch(size=randrange(2, 10))`. None have related issues.

**When to use:** Testing `show-all=yes` filter, testing count endpoint with filtering.

### story_arcs_with_issues

**Type:** List of StoryArc model instances | **Scope:** `function`

**Behavior:** Creates batch of 2-9 story_arcs using `StoryArcFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))`. Each has 1-2 related issues.

**When to use:** Testing list endpoint default behavior, testing ordering operations, testing pagination.

## Fixture Combinations

**Testing Filtering Behavior:**
```python
def test_filter_consistency(api_client, story_arcs_no_issues, story_arcs_with_issues):
    # Default - only shows story_arcs_with_issues
    # With show-all - shows both
```
