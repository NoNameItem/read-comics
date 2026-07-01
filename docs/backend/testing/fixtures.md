# Global Fixtures

Pytest fixtures provided by root conftest (`read_comics/conftest.py`).

## Overview

Global fixtures are available to all tests across all apps. They provide:
- API clients with different authentication levels
- Test users with various roles
- Storage and S3 mocking
- Database access markers

## API Clients

HTTP clients for making requests to Django REST Framework endpoints.

### api_client

**Type**: `APIClient` (from `rest_framework.test`)

**Authentication**: None (anonymous user)

**Usage**: Testing unauthenticated endpoints or public data

```python
def test_public_list(api_client):
    response = api_client.get("/api/volumes/")
    # Request has no authorization header
    assert response.status_code in [200, 401]
```

### authenticated_api_client

**Type**: `APIClient` with JWT Bearer token

**Authentication**: Regular user via JWT

**Depends on**: `user` fixture (creates fresh user each test)

**Usage**: Testing user-specific endpoints or authenticated data

```python
def test_authenticated_list(authenticated_api_client, user):
    response = authenticated_api_client.get("/api/volumes/")
    # Request includes: Authorization: Bearer <token>
    assert response.status_code == 200

def test_user_profile(authenticated_api_client, user):
    response = authenticated_api_client.get(f"/api/users/{user.id}/")
    assert response.status_code == 200
```

**How it works**:
1. Takes `user` fixture as parameter
2. Generates JWT tokens via `RefreshToken.for_user(user)`
3. Sets Authorization header on all requests
4. Each test gets fresh user + fresh tokens

### staff_api_client

**Type**: `APIClient` with JWT Bearer token

**Authentication**: Staff user (is_staff=True)

**Depends on**: `staff` fixture (creates fresh staff user each test)

**Usage**: Testing staff-only endpoints or admin actions

```python
def test_staff_access(staff_api_client, staff):
    response = staff_api_client.get("/api/admin/users/")
    assert response.status_code == 200

def test_regular_user_no_staff_access(authenticated_api_client):
    response = authenticated_api_client.get("/api/admin/users/")
    assert response.status_code == 403
```

### superuser_api_client

**Type**: `APIClient` with JWT Bearer token

**Authentication**: Superuser (is_superuser=True and is_staff=True)

**Depends on**: `superuser` fixture (creates fresh superuser each test)

**Usage**: Testing unrestricted endpoints or full admin access

```python
def test_superuser_access(superuser_api_client, superuser):
    response = superuser_api_client.get("/api/admin/system-settings/")
    assert response.status_code == 200
```

## User Fixtures

User objects created via UserFactory and its specializations.

### user

**Type**: User model instance

**Created via**: `UserFactory()`

**Attributes**:
- `username` — Fake username
- `email` — Fake email
- `name` — Fake full name
- `password` — Strong 42-character password
- `is_active` — True
- `is_staff` — False
- `is_superuser` — False

**Scope**: Function-scoped (new user per test)

**Usage**: Standard test user for authenticated tests

```python
def test_user_profile(user):
    assert user.is_active
    assert not user.is_staff

def test_user_with_finished_issues(user):
    # Create issues finished by this user
    issue = IssueFactory()
    issue.finished_users.add(user)
    assert user.finished_issues.count() == 1
```

### staff

**Type**: User model instance with staff privileges

**Created via**: `StaffFactory()`

**Attributes**: Same as `user`, plus:
- `is_staff` — True

**Scope**: Function-scoped

**Usage**: Staff-only feature testing

```python
def test_staff_can_delete_volume(staff_api_client, staff):
    response = staff_api_client.delete("/api/volumes/1/")
    assert response.status_code in [204, 403]  # Depends on permissions
```

### superuser

**Type**: User model instance with superuser privileges

**Created via**: `SuperuserFactory()`

**Attributes**: Same as `user`, plus:
- `is_staff` — True
- `is_superuser` — True

**Scope**: Function-scoped

**Usage**: Admin functionality testing

```python
def test_superuser_can_access_admin(superuser_api_client):
    response = superuser_api_client.get("/api/admin/")
    assert response.status_code == 200
```

## Storage Fixtures

Mock file storage for tests.

### media_storage

**Type**: Pytest fixture (autouse=True)

**What it does**: Redirects Django's `MEDIA_ROOT` to a temporary directory

**Scope**: Function (each test gets fresh tmpdir)

**Autouse**: Yes (runs automatically, no injection needed)

**Benefits**:
- No actual files written to filesystem
- No S3 uploads during tests
- Clean isolation between tests
- No test artifacts left behind

**Implementation detail**: Uses pytest's `tmpdir` fixture

**Why autouse**: File uploads happen in background, don't want real files polluting test environment

## S3 Mocking

### stop_s3_update

**Type**: Pytest fixture (autouse=True)

**What it does**: Mocks `Issue.update_do_metadata()` method (DigitalOcean Spaces metadata update)

**Scope**: Function (each test gets fresh mock)

**Autouse**: Yes (runs automatically)

**Original purpose**: Updates file metadata in S3 when issue details change

**Why mock**: S3 API calls are:
- Slow
- Require credentials
- Create actual files
- Not relevant to most unit tests

**Implementation detail**: Uses `monkeypatch` to override method with no-op

**When you need real S3 behavior**: Disable mock manually:
```python
@pytest.mark.skip(reason="Requires S3 credentials")
def test_s3_metadata_update(monkeypatch):
    # Remove mock
    monkeypatch.undo()
    # Now real update_do_metadata runs
```

## Common Usage Patterns

### Testing Public and Authenticated Versions

```python
def test_public_version(api_client):
    # Unauthenticated request
    response = api_client.get("/api/volumes/")
    # May show: limited data, is_finished=None, no user-specific fields

def test_authenticated_version(authenticated_api_client):
    # Authenticated request
    response = authenticated_api_client.get("/api/volumes/")
    # May show: full data, is_finished=True/False, user-specific fields
```

### Testing Role-Based Access

```python
def test_regular_user_no_delete(authenticated_api_client):
    response = authenticated_api_client.delete("/api/volumes/1/")
    assert response.status_code == 403

def test_staff_delete(staff_api_client):
    response = staff_api_client.delete("/api/volumes/1/")
    assert response.status_code == 204

def test_superuser_always_allowed(superuser_api_client):
    response = superuser_api_client.delete("/api/volumes/1/")
    assert response.status_code == 204
```

### Testing User-Specific Data

```python
def test_finished_volume_only_visible_to_user(
    user,
    authenticated_api_client,
    api_client,
):
    # Create volume and mark finished for specific user
    volume = VolumeFactory(add_issues=1)
    for issue in volume.issues.all():
        issue.finished_users.add(user)

    # Authenticated user sees is_finished=True
    response = authenticated_api_client.get("/api/volumes/")
    assert response.data["results"][0]["is_finished"] is True

    # Unauthenticated user sees is_finished=None
    response = api_client.get("/api/volumes/")
    assert response.data["results"][0]["is_finished"] is None
```

## Fixture Scope

All fixtures are **function-scoped** (default):
- Created fresh for each test function
- Cleaned up after test completes
- No state leakage between tests

**Benefits**:
- Test isolation
- Predictable test data
- No complex setup/teardown

**Trade-off**: Slightly slower (fixture creation overhead)

**Alternative**: Module-scoped fixtures (created once per test module) — Not used in this project for isolation reasons

## Creating New Global Fixtures

To add new global fixtures, edit `read_comics/conftest.py`:

### Template

```python
@pytest.fixture
def my_new_fixture():
    """Description of what this fixture provides"""
    # Setup
    data = something()
    yield data
    # Teardown (optional)
```

### When to Add

- Need data used by multiple apps
- Common authentication/setup patterns
- Shared mocking/patching

### When to Add to App conftest

- Data specific to one app
- Model-specific fixtures (volumes_with_issues)
- App-specific mocking

## Fixture Dependency Chain

```
authenticated_api_client
  └─ user
       └─ (created via UserFactory)

staff_api_client
  └─ staff
       └─ (created via StaffFactory)

superuser_api_client
  └─ superuser
       └─ (created via SuperuserFactory)

media_storage (autouse)
  └─ (uses pytest's tmpdir)

stop_s3_update (autouse)
  └─ (uses monkeypatch)
```

Any test requesting `authenticated_api_client` automatically gets:
1. Fresh user created
2. Fresh API client created
3. JWT token generated and set
4. All autouse fixtures run

## Best Practices

1. **Use appropriate client** — Match authentication level to test
   ```python
   # ✅ Good: Test public data with unauthenticated client
   def test_list_public(api_client):

   # ✅ Good: Test user-specific data with authenticated client
   def test_list_user_data(authenticated_api_client):

   # ❌ Bad: Use authenticated client for public data (over-spec)
   def test_list_public(authenticated_api_client):
   ```

2. **Don't modify fixtures** — Treat as read-only
   ```python
   # ✅ Good: Use as-is
   response = authenticated_api_client.get("/api/volumes/")

   # ❌ Bad: Modify (affects other tests via shared state)
   authenticated_api_client.credentials(...)  # Don't change
   ```

3. **Use user fixture when test depends on user** — Don't create inline
   ```python
   # ✅ Good: Fixture handles creation
   def test_user_profile(user):
       assert user.username is not None

   # ❌ Bad: Manual creation (no cleanup)
   def test_user_profile():
       user = User.objects.create(username="test")
   ```

4. **Autouse fixtures are transparent** — Don't need to think about them
   ```python
   # media_storage and stop_s3_update run automatically
   # No need to inject them unless you want to access/modify
   def test_file_upload():
       # Uses temporary media storage automatically
       file = upload_file(...)
   ```
