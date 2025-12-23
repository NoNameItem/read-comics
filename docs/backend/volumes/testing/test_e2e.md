# Volumes E2E Tests

End-to-end API tests (`test_e2e.py`) verifying complete workflows for volumes endpoints.

**Mark**: `pytestmark = pytest.mark.django_db` (all tests have database access)

## Test Class: TestVolumesCount

Tests for `/api/volumes/count/` endpoint.

### test_count

**Endpoint**: GET /api/volumes/count/

**Fixtures used**:
- `user` — Test user
- `authenticated_api_client` — HTTP client with JWT token
- `volumes_no_issues` — 2-9 volumes without related issues
- `volumes_with_issues` — 2-9 volumes with 1-2 issues each
- `finished_volumes` — Finished volumes (all issues marked done for user)

**Assertions**:
- Status code: 200
- Response has `count` key
- Count matches: len(volumes_no_issues) + len(volumes_with_issues) + len(finished_volumes)

**Purpose**: Verify count endpoint returns correct total

**Business logic verified**:
- Count includes ALL volumes regardless of issue count
- Count includes finished volumes
- Response format correct

## Test Class: TestVolumesList

Tests for `/api/volumes/` list endpoint (main endpoint).

### test_dont_hide_finished

**Endpoint**: GET /api/volumes/?hide-finished=no

**Fixtures used**:
- `user` — Test user
- `authenticated_api_client` — Client with JWT
- `volumes_with_issues` — Non-finished volumes
- `finished_volumes` — Finished volumes

**Assertions**:
- Status code: 200
- Count = len(volumes_with_issues) + len(finished_volumes)
- All items have expected field set (slug, image, start_year, publisher__*, name, issues_count, finished_count, is_finished)

**Purpose**: Verify ?hide-finished=no query parameter shows ALL volumes

**Business logic verified**:
- Query parameter ?hide-finished=no disables default filtering
- Both finished and non-finished volumes appear
- Response includes all expected fields

**Related**: `HideFinishedQuerySetMixin` (filtering logic)

### test_hide_finished

**Endpoint**: GET /api/volumes/ (default, no query parameter)

**Fixtures used**:
- `user` — Test user
- `authenticated_api_client` — Client with JWT
- `volumes_with_issues` — Non-finished volumes
- `finished_volumes` — Finished volumes

**Assertions**:
- Status code: 200
- Count = len(volumes_with_issues) (finished EXCLUDED)
- All items have expected field set

**Purpose**: Verify default behavior HIDES finished volumes

**Business logic verified**:
- Default behavior (no ?hide-finished parameter) hides completed
- Only non-finished volumes in response
- Count excludes finished

**Related**: `HideFinishedQuerySetMixin` (default behavior)

### test_finished_mark

**Endpoint**: GET /api/volumes/?hide-finished=no

**Fixtures used**:
- `user` — Test user
- `authenticated_api_client` — Client with JWT
- `finished_volume` — Volume with all issues finished by user

**Assertions**:
- Status code: 200
- Response includes finished_volume
- is_finished field = True

**Purpose**: Verify finished volumes marked with is_finished=True

**Business logic verified**:
- Finished volume appears in list
- is_finished field correctly computed as True
- Correct value when all issues finished

**Related**: Serializer computes is_finished via queryset annotation

### test_no_finished_mark

**Endpoint**: GET /api/volumes/

**Fixtures used**:
- `user` — Test user
- `authenticated_api_client` — Client with JWT
- `volume_with_issues` — Volume without all issues finished

**Assertions**:
- Status code: 200
- Volume appears in results
- is_finished field = False

**Purpose**: Verify non-finished volumes marked with is_finished=False

**Business logic verified**:
- Non-finished volume appears in list
- is_finished field correctly computed as False
- Correct value when not all issues finished

### test_no_auth_finished_mark

**Endpoint**: GET /api/volumes/

**Fixtures used**:
- `api_client` — Unauthenticated HTTP client
- `volume_with_issues` — Volume with some finished issues
- `finished_volume` — Volume with all issues finished

**Assertions**:
- Status code: 200
- All items in response have is_finished = None

**Purpose**: Verify unauthenticated users see is_finished=None (no user state)

**Business logic verified**:
- Unauthenticated requests can't have user-specific state
- is_finished not boolean but null
- Preserves privacy (doesn't leak user data)

### test_data

**Endpoint**: GET /api/volumes/

**Fixtures used**:
- `api_client` — Unauthenticated client
- `volume_with_issues` — Volume with related publisher and issues

**Assertions**:
- Status code: 200
- Verify specific fields match volume data (name, year, publisher info, counts)

**Purpose**: Verify serialized response data correctly represents database object

**Data validation**: Checks that serialized output matches source data

## Response Structure

### Expected Fields (VolumesListSerializer)

```
"slug"                  — AutoSlugField
"image"                 — Image URL (from square_medium property)
"publisher__name"       — Publisher name
"publisher__image"      — Publisher image
"publisher__slug"       — Publisher slug
"name"                  — Volume name
"short_description"     — Volume description
"issues_count"          — Count of related issues
"finished_count"        — Count of issues finished by user
"is_finished"           — Boolean (True if all issues finished) or None (unauthenticated)
"start_year"            — Publication year
```

Tests validate this exact field set (via `flatten_dict()` helper).

## Test Patterns

### Fixture Combinations for Filtering

Tests use complementary fixtures to verify filter logic:

```python
def test_hide_finished(
    volumes_with_issues,    # Data that SHOULD appear
    finished_volumes,       # Data that should be EXCLUDED
    authenticated_api_client
):
    response = authenticated_api_client.get("/api/volumes/")
    # Verify: only volumes_with_issues count
    # Verify: no finished_volumes in response
```

### Field Set Validation

Tests ensure response includes ALL expected fields and NO extra fields:

```python
expected_keys = {"slug", "image", "name", ...}
flatten_response_data = flatten_dict(response.data["results"][0])
assert expected_keys == set(flatten_response_data.keys())
```

### Multiple Data Points

Tests use multiple fixtures to ensure logic works with various data:

```python
def test_hide_finished(
    volumes_with_issues,      # Multiple non-finished
    finished_volumes,         # Multiple finished
    authenticated_api_client
):
    # Tests with mix of data
```

## Test Execution

**Run all E2E tests**:
```bash
pytest read_comics/volumes/tests/test_e2e.py
```

**Run specific test class**:
```bash
pytest read_comics/volumes/tests/test_e2e.py::TestVolumesList
```

**Run specific test**:
```bash
pytest read_comics/volumes/tests/test_e2e.py::TestVolumesList::test_hide_finished
```

**With verbose output**:
```bash
pytest -vv read_comics/volumes/tests/test_e2e.py::TestVolumesList::test_hide_finished
```

**With print output**:
```bash
pytest -s read_comics/volumes/tests/test_e2e.py::TestVolumesList::test_hide_finished
```

## Dependencies

### Database Models

- `Volume` — Main model being tested
- `Issue` — Related issues (volume.issues)
- `Publisher` — Related publisher (volume.publisher)
- `User` — Test user for authentication
- `FinishedIssue` — Through model for user progress

### ViewSet & Serializers

- `VolumesViewSet` — Provides list endpoint
- `VolumesListSerializer` — Serializes Volume for list responses
- Mixins: `HideFinishedQuerySetMixin`, `IssuesCountQuerySetMixin`

### Fixtures

- Global: `user`, `api_client`, `authenticated_api_client`
- App-specific: `volumes_no_issues`, `volumes_with_issues`, `finished_volume`, `finished_volumes`

## Failure Scenarios

Tests help catch:

1. **Filtering broken** — Count includes finished when shouldn't
2. **Field missing** — is_finished not in response
3. **Wrong values** — is_finished=False when should be True
4. **Authorization** — Unauthenticated shouldn't see user-specific data
5. **Serialization** — Response data doesn't match database

## Extending Tests

When adding new functionality:

1. **New query parameter** → Add test for parameter + expected behavior
2. **New serializer field** → Add field validation to test_data
3. **New filtering logic** → Add test for inclusion/exclusion with fixtures
4. **New action** → Add test class for new endpoint

Example: Adding search

```python
def test_search_by_name(
    volume_with_issues,
    authenticated_api_client
):
    """Search filters volumes by name"""
    response = authenticated_api_client.get(
        f"/api/volumes/?search={volume_with_issues.name}"
    )
    assert response.status_code == 200
    # Verify search works
    volume_ids = [item["id"] for item in response.data["results"]]
    assert volume_with_issues.id in volume_ids
```
