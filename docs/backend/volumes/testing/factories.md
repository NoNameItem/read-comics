# Volumes Factories

Factory for creating Volume test objects.

## VolumeFactory

**Location**: `read_comics/volumes/tests/factories.py`

Creates Volume model instances with automatic Publisher creation and optional related Issues.

### Inheritance

Extends: `ComicvineSyncModelFactory` (inherits comicvine_id, status, timestamps)

### Field Parameters

| Field | Type | Generator | Purpose |
|-------|------|-----------|---------|
| `name` | TextField | Faker("word") | Volume/series name |
| `start_year` | IntegerField | int(Faker("year")) | Publication year |
| `publisher` | ForeignKey | SubFactory | Related Publisher (auto-created) |
| `add_issues` | (post-generation) | — | Number of related issues to create |

### Inherited from ComicvineSyncModelFactory

- `comicvine_id` — Auto-sequence (0, 1, 2...)
- `comicvine_status` — MATCHED
- `created_dt`, `modified_dt` — Fake timestamps

### Usage Examples

#### Basic Creation

**Single volume with defaults**:
```python
volume = VolumeFactory()
# Auto-creates Publisher
# Has random name, year
```

**With custom values**:
```python
volume = VolumeFactory(
    name="Amazing Spider-Man",
    start_year=1963
)
```

**With custom Publisher**:
```python
publisher = PublisherFactory(name="Marvel Comics")
volume = VolumeFactory(publisher=publisher)

# Or using SubFactory parameter syntax:
volume = VolumeFactory(publisher__name="Marvel Comics")
```

#### Batch Creation

**Multiple volumes**:
```python
volumes = VolumeFactory.create_batch(size=5)
```

**Multiple with same publisher**:
```python
volumes = VolumeFactory.create_batch(
    size=3,
    publisher__name="DC Comics"
)
# All 3 share same publisher named "DC Comics"
```

#### Related Issues

The `add_issues` post-generation parameter creates related Issue objects:

**Single volume with issues**:
```python
volume = VolumeFactory(add_issues=3)
# Creates 3 IssueFactory objects linked to this volume
# Sets first_issue to one random issue
```

**Batch volumes with issues**:
```python
volumes = VolumeFactory.create_batch(
    size=5,
    add_issues=2
)
# 5 volumes, each with 2 issues
# Each volume's first_issue set to random issue
```

**With specific issue count range** (in fixtures):
```python
# Fixtures use random count for variety
volume = VolumeFactory(add_issues=randrange(1, 3))
# 1-2 issues per volume (random)
```

### Post-Generation Hook: add_issues

**Triggered by**: `VolumeFactory(add_issues=N)`

**What it does**:
1. Creates N Issue objects via IssueFactory
2. Links all issues to the volume (volume FK)
3. Selects one random issue as volume.first_issue
4. Saves the volume with updated first_issue FK

**Use cases**:
- Testing volume endpoints that show issue counts
- Testing volume.first_issue relationship
- Creating realistic volume data with issues

**Example fixture using add_issues**:
```python
@pytest.fixture
def volume_with_issues():
    return VolumeFactory(add_issues=randrange(1, 3))
    # Creates 1-2 issues per call
```

### Testing with Related Data

#### Volume Issue Count

```python
def test_volume_issue_count():
    volume = VolumeFactory(add_issues=5)
    assert volume.issues.count() == 5
    assert volume.first_issue is not None
```

#### Volume First Issue

```python
def test_first_issue_set():
    volume = VolumeFactory(add_issues=3)
    assert volume.first_issue in volume.issues.all()
    # first_issue is one of the created issues
```

#### Testing Collections

```python
def test_many_volumes():
    volumes = VolumeFactory.create_batch(size=10, add_issues=2)
    total_issues = sum(v.issues.count() for v in volumes)
    assert total_issues == 20  # 10 volumes × 2 issues
```

### Database Get-or-Create

Via inherited `django_get_or_create = ["comicvine_id"]`:

**Same comicvine_id returns same object**:
```python
volume1 = VolumeFactory(comicvine_id=100)
volume2 = VolumeFactory(comicvine_id=100)
assert volume1.id == volume2.id  # Same database row
```

**Different comicvine_id creates new objects**:
```python
volume1 = VolumeFactory(comicvine_id=100)
volume2 = VolumeFactory(comicvine_id=101)
assert volume1.id != volume2.id  # Different rows
```

### In Test Scenarios

#### Fixtures with Collections

```python
@pytest.fixture
def volumes_with_issues():
    # Create 2-9 volumes, each with 1-2 issues
    return VolumeFactory.create_batch(
        size=randrange(2, 10),
        add_issues=randrange(1, 3)
    )

def test_list_count(volumes_with_issues, authenticated_api_client):
    expected_count = len(volumes_with_issues)
    response = authenticated_api_client.get("/api/volumes/")
    assert response.data["count"] == expected_count
```

#### Finished Volumes

```python
@pytest.fixture
def finished_volumes(user):
    volumes = VolumeFactory.create_batch(
        size=randrange(2, 10),
        add_issues=randrange(1, 3)
    )
    # Mark all issues as finished for user
    for volume in volumes:
        for issue in volume.issues.all():
            issue.finished_users.add(user)
    return volumes

def test_hide_finished(
    volumes_with_issues,
    finished_volumes,
    authenticated_api_client
):
    response = authenticated_api_client.get("/api/volumes/")
    # Finished volumes hidden by default
    assert response.data["count"] == len(volumes_with_issues)
```

### Common Patterns

#### Isolating Test Data

```python
# ✅ Good: Each test gets fresh volume
def test_a(authenticated_api_client):
    volume = VolumeFactory(add_issues=3)
    # volume.id = random (different each test)

def test_b(authenticated_api_client):
    volume = VolumeFactory(add_issues=3)
    # Different volume than test_a
```

#### Building Complex Scenarios

```python
def test_complex_filtering():
    # Create volumes with different states
    volume_marvel = VolumeFactory(
        publisher__name="Marvel",
        add_issues=5
    )
    volume_dc = VolumeFactory(
        publisher__name="DC",
        add_issues=3
    )

    # Test filtering by publisher
    response = api_client.get("/api/volumes/?publisher=marvel")
    assert response.data["count"] == 1
```

#### Testing Edge Cases

```python
def test_volume_no_issues():
    volume = VolumeFactory()  # add_issues not specified
    assert volume.issues.count() == 0

def test_volume_many_issues():
    volume = VolumeFactory(add_issues=100)
    assert volume.issues.count() == 100
```

### Debugging Factories

**Check generated volume**:
```python
volume = VolumeFactory()
print(f"ID: {volume.id}")
print(f"Name: {volume.name}")
print(f"Year: {volume.start_year}")
print(f"ComicVine ID: {volume.comicvine_id}")
print(f"Publisher: {volume.publisher.name}")
print(f"Issues: {volume.issues.count()}")
```

**Build vs. Create**:
```python
# Build: object not saved to DB
volume_unsaved = VolumeFactory.build()
print(f"Has ID: {volume_unsaved.id}")  # None

# Create: object saved to DB
volume_saved = VolumeFactory()
print(f"Has ID: {volume_saved.id}")  # Integer
```

**Override with inspection**:
```python
volume = VolumeFactory(add_issues=5)
# Check defaults
assert volume.name != ""
assert volume.start_year > 1900
# Check relationships
assert volume.publisher is not None
assert volume.first_issue is not None
assert volume.issues.count() == 5
```
