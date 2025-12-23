# Testing Guide: Factories, Fixtures, and E2E Tests

Comprehensive guide to the ReadComics testing infrastructure, covering Factory Boy factories, pytest fixtures, URL/DRF routing tests, and end-to-end API tests.

## Table of Contents
- [Test Structure](#test-structure)
- [Factories](#factories)
- [Fixtures](#fixtures)
- [URL/DRF Tests](#urldrf-tests)
- [E2E Tests](#e2e-tests)
- [Running Tests](#running-tests)
- [Best Practices](#best-practices)

---

## Test Structure

Each app module follows a consistent testing structure:

```
<app>/tests/
├── __init__.py              # Test package marker
├── conftest.py              # pytest fixtures (app-specific)
├── factories.py             # Factory Boy model factories
├── test_drf_urls.py         # URL routing & DRF endpoint tests
└── test_e2e.py              # End-to-end API integration tests
```

### Global Setup

**Root conftest** (`read_comics/conftest.py`):
- Provides global API clients (unauthenticated, authenticated, staff, superuser)
- Creates test users via factories
- Sets up temporary media storage (no S3 writes during tests)
- Mocks S3 metadata operations (`update_do_metadata`)

**13 app-level conftests** (`<app>/tests/conftest.py`):
- Define model-specific fixtures using factories
- Build on global fixtures from root conftest
- Support single/batch/related data creation patterns

---

## Factories

Factories programmatically create model instances for testing using Factory Boy. They replace manual object creation with declarative, reusable definitions.

### Factory Hierarchy

**Base**: `ComicvineSyncModelFactory` (`read_comics/utils/test_utils/factories.py`)
- Provides defaults for all ComicVine-synced models
- Generates sequential comicvine_ids
- Sets status to MATCHED
- Generates fake URLs and timestamps
- Uses `django_get_or_create` on comicvine_id (prevents duplicates)

**Concrete**: App-specific factories (e.g., `VolumeFactory`, `IssueFactory`)
- Inherit from base or `DjangoModelFactory`
- Override fields with specific fake data generators
- Add post-generation hooks for related objects

### Key Factory Features

#### 1. **Field Declarations**
- `Faker("word")` — Generate fake data (word, paragraph, email, name, etc.)
- `factory.Sequence(lambda n: n)` — Auto-incrementing values
- `factory.LazyAttribute(lambda o: ...)` — Compute field value dynamically
- `factory.SubFactory(...)` — Create related objects automatically

**Example**: VolumeFactory defines:
- `name = Faker("word")` → Random word as volume name
- `start_year = factory.LazyAttribute(lambda o: int(o.start_year_str))` → Convert year string to int
- `publisher = factory.SubFactory(...)` → Auto-create Publisher when volume is created

#### 2. **Post-Generation Hooks**
Used for creating complex relationships after main object creation.

**Example**: VolumeFactory's `add_issues` hook:
- Takes parameter: `VolumeFactory(add_issues=3)`
- Creates specified number of related Issue objects
- Sets one random issue as `first_issue`
- Saves the volume with updated FK

**When to use**: For M2M relationships, through-model setup, or complex post-creation logic

#### 3. **Factory Methods**
- `.create()` — Create and save single object
- `.create_batch(size=5)` — Create and save multiple objects
- `.build()` — Create object without saving to DB
- `.build_batch()` — Build multiple without saving

#### 4. **Inheritance for Specializations**
Factories inherit from each other to create variations.

**Example**: UserFactory hierarchy:
- `UserFactory` — Base user with generated username/email
- `SuperuserFactory` — Extends UserFactory, sets `is_superuser=True`
- `StaffFactory` — Extends UserFactory, sets `is_staff=True`

### Factory Usage Examples

#### Basic Creation

```python
# Single instance with defaults
volume = VolumeFactory()

# Single instance with custom values
volume = VolumeFactory(name="Amazing Spider-Man", start_year=1963)

# Batch creation
volumes = VolumeFactory.create_batch(size=5)
```

#### Related Objects

```python
# Auto-create related Publisher
volume = VolumeFactory()

# Pass custom Publisher
volume = VolumeFactory(publisher__name="Marvel Comics")

# Create with related Issues
volume = VolumeFactory(add_issues=3)  # Adds 3 related issues
```

#### User Variants

```python
user = UserFactory()              # Regular user
staff = StaffFactory()            # Staff user
admin = SuperuserFactory()        # Admin user
user_with_password = UserFactory(password="MyPassword123!")
```

#### In Test Functions

```python
@pytest.mark.django_db
def test_volume_has_issues():
    volume = VolumeFactory(add_issues=5)
    assert volume.issues.count() == 5
    assert volume.first_issue is not None
```

---

## Fixtures

Fixtures provide test data via pytest's dependency injection. They abstract factory calls and create consistent datasets for related tests.

### Global Fixtures (Root conftest)

#### API Clients

**Purpose**: Provide HTTP clients with different authentication levels

- `api_client()` — Unauthenticated REST client
- `authenticated_api_client(user)` — Client with Bearer token for regular user
- `staff_api_client(staff)` — Client with Bearer token for staff user
- `superuser_api_client(superuser)` — Client with Bearer token for superuser

**Authentication method**: JWT tokens via `RefreshToken.for_user()`

**Usage**:
```python
def test_unauthenticated_list(api_client):
    response = api_client.get("/api/volumes/")
    # May return 401 or 200 depending on permissions

def test_authenticated_list(authenticated_api_client):
    response = authenticated_api_client.get("/api/volumes/")
    # Requests include Authorization: Bearer <token>
```

#### User Fixtures

**Purpose**: Provide pre-created users with different roles

- `user()` — Regular user via UserFactory
- `staff()` — Staff user via StaffFactory
- `superuser()` — Admin user via SuperuserFactory

**Usage**:
```python
def test_user_profile(user):
    assert user.username is not None

def test_superuser_permissions(superuser, superuser_api_client):
    response = superuser_api_client.get("/api/admin/")
    assert response.status_code == 200
```

#### Storage & Mocking Fixtures

- `media_storage()` — Autouse fixture redirecting media to tmpdir (no real file writes)
- `stop_s3_update()` — Autouse fixture disabling S3 metadata updates during tests

**Autouse** means they run for every test automatically (no parameter injection needed).

### Module-Level Fixtures (App conftest)

Each app provides fixtures for its primary model and related variations.

#### Volumes Fixtures (Pattern)

- `volume_no_issues()` — Single volume without related issues
- `volume_with_issues()` — Single volume with 1-2 random issues
- `volumes_no_issues()` — List of 2-9 volumes without issues
- `volumes_with_issues()` — List of 2-9 volumes, each with 1-2 issues
- `finished_volume(user)` — Single volume where all issues marked finished by user
- `finished_volumes(user)` — List of volumes where all issues marked finished by user

**Pattern rationale**:
- Single vs. batch fixtures for different test needs (count vs. list tests)
- With/without related data (to test filtering/hiding behavior)
- User-dependent fixtures (to test user-specific logic like "finished" state)

**Usage**:
```python
def test_count_all_volumes(volumes_with_issues, volumes_no_issues):
    # Both fixtures combined = all test volumes
    expected_count = len(volumes_with_issues) + len(volumes_no_issues)

def test_hide_finished_volumes(volumes_with_issues, finished_volumes):
    # finished_volumes should be hidden from default list endpoint
    expected_count = len(volumes_with_issues)
```

#### Issues Fixtures (Pattern)

- `issue()` — Single issue
- `issues()` — List of 2-9 issues
- `finished_issue(user)` — Single issue marked finished by user
- `finished_issues(user)` — List of 2-9 issues marked finished by user

**Usage**:
```python
def test_issue_serialization(issue):
    assert issue.number is not None

def test_finished_count(user, finished_issues):
    assert user.finished_issues.count() == len(finished_issues)
```

### Fixture Composition

Fixtures can depend on other fixtures (pytest injects them automatically):

```python
@pytest.fixture
def finished_volume(user) -> Volume:  # Depends on user fixture
    volume = VolumeFactory(add_issues=3)
    for issue in volume.issues.all():
        issue.finished_users.add(user)  # Link to specific user
    return volume
```

---

## URL/DRF Tests

URL tests verify bidirectional mapping between URL names and paths in Django REST Framework.

**Location**: `<app>/tests/test_drf_urls.py`

**Purpose**: Catch regressions when routing configuration changes

### Test Pattern

Each endpoint gets two assertions:
1. `reverse()` — URL name → URL path
2. `resolve()` — URL path → URL name

**Example for volumes endpoints**:
- `test_count()` — Verifies `/api/volumes/count/` maps to `api:volume-count`
- `test_list()` — Verifies `/api/volumes/` maps to `api:volume-list`
- `test_started()` — Verifies `/api/volumes/started/` maps to `api:volume-started` (custom action)

### Common Endpoints Tested

Standard RESTful endpoints:
- `/api/<entity>/` — List (GET) and Create (POST)
- `/api/<entity>/<id>/` — Retrieve (GET), Update (PUT/PATCH), Delete
- `/api/<entity>/count/` — Count action (from CountActionMixin)

Custom action endpoints:
- `/api/<entity>/started/` — Started items (from StartedActionMixin)
- `/api/<entity>/finished/` — Finished items (from FinishedQuerySetMixin)

### Benefits

- **Fast**: No database access, purely routing checks
- **Regression detection**: Catches accidental route changes
- **Documentation**: List of all available endpoints
- **Testing order**: Run before E2E tests (endpoints must exist before testing them)

---

## E2E Tests

End-to-end tests verify complete API workflows from HTTP request to response validation.

**Location**: `<app>/tests/test_e2e.py`

**Scope**: HTTP request → Django ViewSet → Database query → Serialization → HTTP response

**Mark**: All tests have `pytestmark = pytest.mark.django_db` (enables database access)

### Test Organization

Tests grouped by endpoint in classes:
- `TestVolumesList` — List endpoint tests
- `TestVolumesCount` — Count endpoint tests
- `TestVolumesStarted` — Started endpoint tests

### Test Scenarios

#### 1. Authentication & Authorization Tests

**Purpose**: Verify access control and authentication requirements

**Test cases**:
- Unauthenticated access (api_client) — May return 401 or filtered data
- Authenticated access (authenticated_api_client) — User-specific data
- Unauthorized actions (staff_api_client vs. superuser_api_client) — Permission checks

**Example scenario**:
- Unauthenticated user gets list with `is_finished=None` for all items
- Authenticated user gets list with `is_finished=True/False` based on their progress

#### 2. Filtering & Query Parameter Tests

**Purpose**: Verify query parameters affect response data correctly

**Test cases**:
- Default behavior — `GET /api/volumes/`
- Hide finished — `GET /api/volumes/?hide-finished=yes`
- Show all — `GET /api/volumes/?hide-finished=no`
- Ordering — `GET /api/volumes/?ordering=name`
- Search — `GET /api/volumes/?search=spider`

**Assertions**:
- Status code 200
- Correct count in response
- Correct items in results
- Correct ordering of results

**Example**: Hide finished volumes test
- Create volumes_with_issues and finished_volumes fixtures
- GET `/api/volumes/` (default behavior)
- Assert response.data["count"] == len(volumes_with_issues) (finished excluded)
- GET `/api/volumes/?hide-finished=no`
- Assert response.data["count"] == len(volumes_with_issues) + len(finished_volumes) (all shown)

#### 3. Response Structure Validation

**Purpose**: Verify serializer output matches API contract

**Test cases**:
- Check all expected fields present in response
- Verify field types (string, int, boolean, object, array)
- Check nested object structure
- Validate computed fields

**Assertions**:
- Response has exactly expected set of keys
- No extra fields leaked from database
- Nested relationships properly serialized
- Count and pagination metadata correct

**Example**: List response validation
- Expected keys: {slug, image, name, publisher__name, issues_count, finished_count, is_finished}
- Check all items have exactly these keys
- Check publisher__name is string
- Check issues_count is integer
- Check is_finished is boolean or None

#### 4. Business Logic Tests

**Purpose**: Verify endpoints correctly implement domain logic

**Test cases**:
- Finished volumes hidden by default but shown with flag
- is_finished computed correctly (all issues finished?)
- issues_count reflects actual related issues
- finished_count reflects user's finished issues
- Pagination limits results correctly

**Example**: Finished volume marking
- Create volume with 3 issues
- Mark all issues as finished for user
- GET list endpoint with authenticated client
- Assert is_finished=True for that volume
- Create another volume (not finished)
- Assert is_finished=False for that volume

### Common Response Assertions

**Status code**:
```python
assert response.status_code == 200
```

**Count/Pagination**:
```python
assert response.data["count"] == expected_total
assert len(response.data["results"]) == expected_page_size
```

**Field validation**:
```python
item = response.data["results"][0]
assert "slug" in item
assert item["is_finished"] in [True, False, None]
assert isinstance(item["issues_count"], int)
```

**Nested data**:
```python
assert response.data["results"][0]["publisher"]["name"] == "Marvel Comics"
```

**Comparison with fixtures**:
```python
volume_ids = [item["id"] for item in response.data["results"]]
assert set(volume_ids) == set(v.id for v in volumes_with_issues)
```

### Response Data Flattening

Helper function `flatten_dict()` converts nested responses to single-level dicts for easier assertion:

**Before**: `{"publisher": {"name": "Marvel", "slug": "marvel"}}`
**After**: `{"publisher__name": "Marvel", "publisher__slug": "marvel"}`

**Usage**: Verify exact set of returned keys
```python
flatten_response = flatten_dict(response.data["results"][0])
expected_keys = {"slug", "name", "publisher__name", "issues_count"}
assert set(flatten_response.keys()) == expected_keys
```

---

## Running Tests

### Basic Commands

**All tests** (from project root):
```bash
docker-compose -f local.yml run --rm backend pytest
```

**Specific test file**:
```bash
docker-compose -f local.yml run --rm backend pytest read_comics/volumes/tests/test_e2e.py
```

**Specific test class**:
```bash
docker-compose -f local.yml run --rm backend pytest read_comics/volumes/tests/test_e2e.py::TestVolumesList
```

**Specific test method**:
```bash
docker-compose -f local.yml run --rm backend pytest read_comics/volumes/tests/test_e2e.py::TestVolumesList::test_hide_finished
```

### Output Options

**Verbose output** (show test names):
```bash
pytest -v
```

**Very verbose** (show test names + assertions):
```bash
pytest -vv
```

**Show print statements**:
```bash
pytest -s
```

**Show local variables on failure**:
```bash
pytest -l
```

**Combined**:
```bash
pytest -vv -s --tb=short
```

### Coverage Analysis

**Generate coverage report**:
```bash
docker-compose -f local.yml run --rm backend coverage run -m pytest
docker-compose -f local.yml run --rm backend coverage html
```

Opens report at `htmlcov/index.html`

### Filter Tests

**Run only URLs tests**:
```bash
pytest -k "test_drf_urls"
```

**Run only E2E tests**:
```bash
pytest -k "test_e2e"
```

**Run except E2E**:
```bash
pytest -k "not test_e2e"
```

---

## Best Practices

### 1. Use Fixtures Instead of Inline Creation

**✅ Good**: Factories + fixtures abstract complexity
```python
def test_volume_count(volumes_with_issues):
    # Fixture handles creation
    assert len(volumes_with_issues) > 0
```

**❌ Bad**: Manual object creation
```python
def test_volume_count():
    volume = Volume.objects.create(name="Test")
    # No related data, fragile, hard to modify
    assert volume is not None
```

**Benefits**:
- Fixtures reused across tests (DRY principle)
- Easy to modify test data setup (change fixture, not every test)
- Fixture names document intent (volumes_with_issues is clear)

### 2. One Test = One Concern

**✅ Good**: Separate tests for different behaviors
```python
def test_list_returns_200(authenticated_api_client, volumes_with_issues):
    response = authenticated_api_client.get("/api/volumes/")
    assert response.status_code == 200

def test_list_hides_finished(authenticated_api_client, volumes_with_issues, finished_volumes):
    response = authenticated_api_client.get("/api/volumes/")
    # Assert only volumes_with_issues count (finished excluded)
    assert response.data["count"] == len(volumes_with_issues)
```

**❌ Bad**: Multiple concerns in one test
```python
def test_volume_list(authenticated_api_client, volumes_with_issues, finished_volumes):
    response = authenticated_api_client.get("/api/volumes/")
    assert response.status_code == 200  # Tests status
    assert response.data["count"] == len(volumes_with_issues)  # Tests filtering
    # Hard to debug which part failed
```

### 3. Name Tests to Describe Behavior

**✅ Good**: Clear test names explain what's tested
- `test_hide_finished_by_default()`
- `test_show_finished_with_flag()`
- `test_unauthenticated_users_see_none_for_finished()`

**❌ Bad**: Generic or unclear names
- `test_list()`
- `test_volumes()`
- `test_api()`

### 4. Use Parametrized Tests for Multiple Scenarios

**✅ Good**: Single parametrized test covers multiple cases
```python
@pytest.mark.parametrize("query,expected_count", [
    ("?hide-finished=yes", 5),
    ("?hide-finished=no", 10),
    ("", 5),  # Default
])
def test_hide_finished_parameter(authenticated_api_client, query, expected_count):
    response = authenticated_api_client.get(f"/api/volumes/{query}")
    assert response.data["count"] == expected_count
```

**❌ Bad**: Separate tests for each case (repetitive)
```python
def test_hide_finished_yes(): ...
def test_hide_finished_no(): ...
def test_hide_finished_default(): ...
```

### 5. Mark Tests Appropriately

**✅ Good**: Mark at class level if all tests need DB
```python
@pytest.mark.django_db
class TestVolumesAPI:
    def test_list(self, authenticated_api_client): ...
    def test_count(self, authenticated_api_client): ...
```

**✅ Good**: Mark individual tests if mixed
```python
def test_url_routing():  # No DB needed
    assert reverse("api:volume-list") == "/api/volumes/"

@pytest.mark.django_db
def test_list_endpoint(authenticated_api_client):  # DB needed
    response = authenticated_api_client.get("/api/volumes/")
    assert response.status_code == 200
```

### 6. Test Realistically

**✅ Good**: Use actual API endpoints and serializers
```python
def test_list(authenticated_api_client, volumes_with_issues):
    response = authenticated_api_client.get("/api/volumes/")
    # Tests full stack: URL → ViewSet → Serializer
    assert response.status_code == 200
```

**❌ Bad**: Test serializers directly (bypass ViewSet)
```python
def test_serializer():
    volume = VolumeFactory()
    serializer = VolumeSerializer(volume)
    # Doesn't test ViewSet, permissions, filtering
    assert serializer.data["name"] == volume.name
```

### 7. Validate Response Structure

Always check that response has expected fields:

```python
# ✅ Good: Verify exact field set
expected_keys = {"slug", "name", "publisher__name", "issues_count"}
actual_keys = set(flatten_dict(response.data["results"][0]).keys())
assert expected_keys == actual_keys  # Catches missing/extra fields

# ❌ Bad: Only check specific field
assert "name" in response.data["results"][0]  # Doesn't catch extra leaks
```

---

## Testing Workflow

### When Adding New Feature

1. **Write URL test** — Define expected endpoint
   ```bash
   pytest read_comics/volumes/tests/test_drf_urls.py::TestVolumesApiUrls::test_new_endpoint
   ```

2. **Write E2E test** — Define expected behavior
   ```bash
   pytest read_comics/volumes/tests/test_e2e.py::TestNewFeature
   ```

3. **Implement feature** (ViewSet, Serializer, Model)

4. **Run tests** — Should pass

5. **Run full suite** — Ensure no regressions
   ```bash
   pytest read_comics/volumes/tests/
   ```

### When Debugging Failed Test

1. **Run with verbose output**:
   ```bash
   pytest -vv -s test_file.py::TestClass::test_method
   ```

2. **Check fixtures** — Are they creating expected data?
   ```bash
   pytest -vv -s --pdb test_file.py::test_method
   # In debugger: print(fixtures)
   ```

3. **Check response** — What's actually returned?
   ```bash
   pytest -vv -s test_file.py::test_method
   # Add print(response.data) in test
   ```

4. **Check database** — What's actually saved?
   ```bash
   pytest -vv -s --pdb test_file.py::test_method
   # In debugger: Model.objects.all()
   ```

---

## Summary

| Component | Purpose | Location | Example |
|-----------|---------|----------|---------|
| **Factories** | Create test objects | `tests/factories.py` | `VolumeFactory(add_issues=3)` |
| **Fixtures** | Provide test data | `tests/conftest.py` | `def test_list(volumes_with_issues):` |
| **URL Tests** | Verify routing | `tests/test_drf_urls.py` | `reverse()` and `resolve()` |
| **E2E Tests** | Test full workflows | `tests/test_e2e.py` | HTTP requests and responses |

All tests are database-marked, use factories for data, validate responses completely, and test realistic scenarios.