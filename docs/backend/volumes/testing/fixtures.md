# Volumes Fixtures

Pytest fixtures for volumes testing (`read_comics/volumes/tests/conftest.py`).

## Overview

Provides 6 fixtures for testing volumes API with different data scenarios:
- Single volumes vs. batches
- With or without related issues
- With or without user completion

## Single Volume Fixtures

### volume_no_issues

**Type**: Volume model instance

**Returns**: Single `Volume` with no related issues

**When to use**:
- Testing volume endpoints with minimal data
- Testing volume count without filtering by issues
- Testing volume basic fields

**Usage**:
```python
def test_volume_fields(volume_no_issues):
    assert volume_no_issues.name is not None
    assert volume_no_issues.start_year is not None
    assert volume_no_issues.publisher is not None
    assert volume_no_issues.issues.count() == 0
```

### volume_with_issues

**Type**: Volume model instance

**Returns**: Single `Volume` with 1-2 random related issues

**Variant handling**: Uses `randrange(1, 3)` for issue count variety

**When to use**:
- Testing volume list/count endpoints with realistic data
- Testing issue counting logic
- Testing first_issue resolution
- Testing volume detail response fields (issues_count, etc.)

**Usage**:
```python
def test_volume_with_issues(volume_with_issues):
    assert 1 <= volume_with_issues.issues.count() <= 2
    assert volume_with_issues.first_issue is not None

def test_list_includes_issue_count(
    api_client,
    volume_with_issues
):
    response = api_client.get("/api/volumes/")
    item = response.data["results"][0]
    assert item["issues_count"] >= 1
```

## Batch Volume Fixtures

### volumes_no_issues

**Type**: List of Volume instances

**Returns**: 2-9 volumes without related issues

**Variant handling**: Uses `randrange(2, 10)` for size variety

**When to use**:
- Testing list endpoint pagination
- Testing volume count
- Testing filtering with multiple items
- Testing ordering with multiple items

**Usage**:
```python
def test_volumes_count(volumes_no_issues, authenticated_api_client):
    response = authenticated_api_client.get("/api/volumes/count/")
    assert response.data["count"] >= 2

def test_list_pagination(volumes_no_issues, api_client):
    response = api_client.get("/api/volumes/?limit=3")
    assert len(response.data["results"]) <= 3
```

### volumes_with_issues

**Type**: List of Volume instances

**Returns**: 2-9 volumes, each with 1-2 random related issues

**Variant handling**: Both count and issue count use `randrange()` for variety

**When to use**:
- Testing realistic list endpoints
- Testing issue counting across multiple volumes
- Testing filtering behavior (show/hide finished)
- Testing ordering with varied data

**Usage**:
```python
def test_list_issues_counts(volumes_with_issues, api_client):
    response = api_client.get("/api/volumes/")
    # All volumes should have at least 1 issue
    for item in response.data["results"]:
        assert item["issues_count"] >= 1

def test_volumes_ordered_by_year(volumes_with_issues, api_client):
    response = api_client.get("/api/volumes/?ordering=start_year")
    # First volume's year <= last volume's year
    results = response.data["results"]
    if len(results) > 1:
        first_year = results[0]["start_year"]
        last_year = results[-1]["start_year"]
        assert first_year <= last_year
```

## Finished Volume Fixtures

### finished_volume

**Type**: Volume model instance

**Parameter**: `user` fixture (required)

**Returns**: Single `Volume` with 1-2 issues, all marked as finished by `user`

**Setup steps**:
1. Creates volume with random issues (1-2)
2. Marks each issue as finished for specified user
3. Returns volume

**When to use**:
- Testing finished/completed state
- Testing user progress tracking
- Testing "is_finished" field computation
- Testing hide-finished filtering
- Testing user-specific visibility

**Usage**:
```python
def test_finished_volume_marked(
    user,
    finished_volume,
    authenticated_api_client
):
    response = authenticated_api_client.get("/api/volumes/?hide-finished=no")
    # Should include finished volume
    volume_ids = [item["id"] for item in response.data["results"]]
    assert finished_volume.id in volume_ids

def test_finished_volume_hidden_by_default(
    user,
    finished_volume,
    authenticated_api_client
):
    response = authenticated_api_client.get("/api/volumes/")
    # Finished volume hidden by default
    volume_ids = [item["id"] for item in response.data["results"]]
    assert finished_volume.id not in volume_ids

def test_is_finished_field(
    user,
    finished_volume,
    authenticated_api_client
):
    response = authenticated_api_client.get("/api/volumes/?hide-finished=no")
    for item in response.data["results"]:
        if item["id"] == finished_volume.id:
            assert item["is_finished"] is True
```

### finished_volumes

**Type**: List of Volume instances

**Parameter**: `user` fixture (required)

**Returns**: 2-9 volumes, each with 1-2 issues, all marked finished by `user`

**Setup steps** (for each volume):
1. Create volume with random issues (1-2)
2. Mark all issues as finished for user
3. Add to list

**When to use**:
- Testing hide-finished filtering with multiple finished volumes
- Testing user progress count
- Testing finished state across multiple volumes
- Testing filtering combinations

**Usage**:
```python
def test_hide_finished_default(
    volumes_with_issues,
    finished_volumes,
    authenticated_api_client
):
    """Default behavior hides finished volumes"""
    response = authenticated_api_client.get("/api/volumes/")

    # Only non-finished volumes shown
    assert response.data["count"] == len(volumes_with_issues)

    # Finished volumes not in response
    finished_ids = {v.id for v in finished_volumes}
    response_ids = {item["id"] for item in response.data["results"]}
    assert finished_ids.isdisjoint(response_ids)  # No overlap

def test_show_finished_flag(
    volumes_with_issues,
    finished_volumes,
    authenticated_api_client
):
    """With flag, finished volumes are shown"""
    response = authenticated_api_client.get("/api/volumes/?hide-finished=no")

    # Both types shown
    expected_count = len(volumes_with_issues) + len(finished_volumes)
    assert response.data["count"] == expected_count

def test_finished_count_correct(
    finished_volumes,
    authenticated_api_client
):
    """Each finished volume shows correct finished_count"""
    response = authenticated_api_client.get("/api/volumes/?hide-finished=no")

    for item in response.data["results"]:
        # finished_count == issues_count (all finished)
        assert item["finished_count"] == item["issues_count"]
```

## Fixture Composition Patterns

### Combining Fixtures

```python
def test_list_shows_mix(
    volumes_no_issues,           # 2-9 volumes, no issues
    volumes_with_issues,         # 2-9 volumes, 1-2 issues each
    authenticated_api_client
):
    """List shows both types"""
    response = authenticated_api_client.get("/api/volumes/")

    expected_count = len(volumes_no_issues) + len(volumes_with_issues)
    assert response.data["count"] == expected_count

    # Check that results include both types
    response_ids = {item["id"] for item in response.data["results"]}

    no_issue_ids = {v.id for v in volumes_no_issues}
    with_issue_ids = {v.id for v in volumes_with_issues}

    assert response_ids & no_issue_ids  # Some no-issue volumes
    assert response_ids & with_issue_ids  # Some with-issue volumes
```

### Filtering Finished from Mixed

```python
def test_filter_finished_from_mix(
    volumes_with_issues,         # Non-finished
    finished_volumes,            # Finished
    authenticated_api_client
):
    """Hide-finished=yes filters correctly"""
    response = authenticated_api_client.get("/api/volumes/")

    # Only non-finished
    assert response.data["count"] == len(volumes_with_issues)

    response_ids = {item["id"] for item in response.data["results"]}
    finished_ids = {v.id for v in finished_volumes}

    # No finished volumes
    assert not (response_ids & finished_ids)
```

### User-Specific Visibility

```python
def test_different_users_different_finished(
    user,
    user2,  # Second user fixture
    volume_with_issues,
    authenticated_api_client,
):
    """Finished state is user-specific"""
    # Mark finished for user (not user2)
    for issue in volume_with_issues.issues.all():
        issue.finished_users.add(user)

    # User sees finished
    response = authenticated_api_client.get("/api/volumes/?hide-finished=no")
    volume_ids = [item["id"] for item in response.data["results"]]
    assert volume_with_issues.id in volume_ids

    # User2 sees not finished
    # (would need separate client for user2)
```

## Fixture Dependency Chain

```
finished_volume
  └─ user (from global conftest)
       └─ UserFactory

volumes_with_issues
  └─ VolumeFactory.create_batch(add_issues=...)
```

All fixtures use fresh data (function scope), no state between tests.

## Edge Cases and Variants

### Zero Issues

```python
def test_volume_no_issues():
    volume = VolumeFactory()  # No add_issues parameter
    assert volume.issues.count() == 0
```

### Many Issues

```python
def test_volume_many_issues():
    volume = VolumeFactory(add_issues=100)
    assert volume.issues.count() == 100
```

### Random Counts Help Catch Assumptions

```python
# ✅ Good: Test works with any count 1-2
def test_volume_with_issues(volume_with_issues):
    assert volume_with_issues.issues.count() >= 1

# ❌ Bad: Assumes exactly 2
def test_volume_with_issues(volume_with_issues):
    assert volume_with_issues.issues.count() == 2  # May fail!
```

The random counts (via `randrange()`) help catch brittle assumptions in tests.

## Testing Fixture Logic

If you need to verify fixtures work correctly:

```python
def test_fixture_setup(volume_with_issues):
    """Verify fixture creates expected data"""
    assert 1 <= volume_with_issues.issues.count() <= 2
    assert volume_with_issues.first_issue is not None
    assert volume_with_issues.first_issue in volume_with_issues.issues.all()

def test_finished_fixture_setup(user, finished_volume):
    """Verify finished fixture marks issues correctly"""
    assert finished_volume.issues.count() > 0
    for issue in finished_volume.issues.all():
        assert user in issue.finished_users.all()
```
