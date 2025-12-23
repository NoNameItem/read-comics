# Global Factories

Shared factory classes used across all backend tests.

## ComicvineSyncModelFactory

**Location**: `read_comics/utils/test_utils/factories.py`

Base factory for all models syncing from ComicVine API.

### Purpose

Provides default field values for ComicVine-synced models:
- Auto-incrementing `comicvine_id` (sequence)
- Fake URLs via `Faker("uri")`
- Status set to `MATCHED`
- Fake timestamps (current year)
- Deduplication via `django_get_or_create` on `comicvine_id`

### Inherited By

All entity factories inherit from this base:
- `VolumeFactory`
- `IssueFactory`
- `CharacterFactory`
- `TeamFactory`
- `PersonFactory`
- `LocationFactory`
- `ConceptFactory`
- `ObjectFactory`
- `PowerFactory`
- `StoryArcFactory`

### Field Defaults

| Field | Type | Value | Purpose |
|-------|------|-------|---------|
| `comicvine_id` | Integer | Auto-sequence (0, 1, 2...) | Unique API identifier |
| `comicvine_url` | URLField | Fake URI | Public ComicVine link |
| `comicvine_status` | CharField | `MATCHED` | Default sync status |
| `comicvine_last_match` | DateTime | Fake (current year) | Last sync timestamp |
| `created_dt` | DateTime | Fake (current year) | Creation timestamp |
| `modified_dt` | DateTime | Fake (current year) | Modification timestamp |

### Usage

#### Basic Creation

```python
from read_comics.volumes.tests.factories import VolumeFactory

# Create volume with all defaults
volume = VolumeFactory()

# Create with overrides
volume = VolumeFactory(
    comicvine_id=12345,
    comicvine_status=ComicvineSyncModel.ComicvineStatus.QUEUED
)
```

#### Deduplication Behavior

The factory uses `django_get_or_create = ["comicvine_id"]`:
- Multiple calls with same `comicvine_id` return same object
- Useful for testing idempotent imports

```python
# First call: creates new object
volume1 = VolumeFactory(comicvine_id=100)

# Second call: returns existing object (same comicvine_id)
volume2 = VolumeFactory(comicvine_id=100)

assert volume1.id == volume2.id  # Same database object
```

#### In Child Factories

App-specific factories extend this base:

```python
class VolumeFactory(ComicvineSyncModelFactory):
    name = Faker("word")
    start_year = factory.LazyAttribute(lambda o: int(Faker("year").generate()))
    publisher = factory.SubFactory("read_comics.publishers.tests.factories.PublisherFactory")

    class Meta:
        model = Volume
        # Inherits: django_get_or_create = ["comicvine_id"]
```

Child factories automatically get all parent defaults plus their own fields.

### Faker Generators

Common Faker generators used in factories:

| Generator | Output | Example |
|-----------|--------|---------|
| `Faker("word")` | Single word | "umbrella" |
| `Faker("name")` | Full name | "John Smith" |
| `Faker("email")` | Email address | "user@example.com" |
| `Faker("paragraph")` | Short paragraph | "Lorem ipsum dolor sit..." |
| `Faker("uri")` | URL | "https://example.com/path" |
| `Faker("year")` | Year string | "2023" |
| `Faker("date_time_this_year")` | DateTime object | datetime(...) |
| `Faker("user_name")` | Username | "john_smith" |

### LazyAttribute Pattern

Dynamically compute field values based on other fields:

```python
start_year_str = Faker("year")  # "2023" (string)
start_year = factory.LazyAttribute(lambda o: int(o.start_year_str))  # 2023 (int)
```

**When to use**:
- Converting field types
- Computing based on other fields
- Generating related values

### SubFactory Pattern

Automatically create related objects:

```python
# When Volume is created, Publisher is also created
volume = VolumeFactory()
assert volume.publisher is not None  # Automatically created

# Pass custom parameters to SubFactory
volume = VolumeFactory(publisher__name="Marvel Comics")
assert volume.publisher.name == "Marvel Comics"
```

**Syntax**: `factory.SubFactory("path.to.Factory", param=value)`

**Nested parameters**: Use double underscore `__` to pass to SubFactory

### Post-Generation Hooks

Run logic after object creation:

```python
class VolumeFactory(ComicvineSyncModelFactory):
    @factory.post_generation
    def add_issues(self: Volume, create, extracted, **kwargs):
        """Create related issues after volume is created"""
        if create and extracted is not None and extracted > 0:
            for i in range(extracted):
                IssueFactory(volume=self)
```

**When to use**:
- M2M relationships (add() after creation)
- Complex setup requiring saved parent object
- Conditional related object creation

**Usage**: `VolumeFactory(add_issues=5)` → Creates 5 related issues

### Batch Creation

Create multiple objects:

```python
# Create list of volumes
volumes = VolumeFactory.create_batch(size=5)

# With parameters
volumes = VolumeFactory.create_batch(size=5, add_issues=2)
```

**Methods**:
- `.create()` — Single object, saved to DB
- `.create_batch(size=N)` — N objects, saved to DB
- `.build()` — Single object, not saved
- `.build_batch(size=N)` — N objects, not saved

### Database Get-or-Create

`django_get_or_create = ["comicvine_id"]` in Meta class:

**Behavior**:
- First creation with `comicvine_id=100` → Insert
- Second creation with `comicvine_id=100` → Return existing (no insert)
- Avoids constraint violations on unique fields

**Use case**: Importing same entities from API multiple times

```python
# Simulating re-import from ComicVine
volume = VolumeFactory(comicvine_id=12345)
volume.delete()

# Re-create with same ID
volume2 = VolumeFactory(comicvine_id=12345)  # New object with same ID

# Without django_get_or_create, would cause IntegrityError if comicvine_id is unique
```

## UserFactory

**Location**: `read_comics/users/tests/factories.py`

Factory for creating test users.

### Purpose

Generate user objects with secure passwords and various role levels.

### Variants

| Class | Role | Sets | Usage |
|-------|------|------|-------|
| `UserFactory` | Regular | username, email, name | Standard user |
| `StaffFactory` | Staff | is_staff=True | Admin/staff testing |
| `SuperuserFactory` | Admin | is_superuser=True | Full admin access |

### Field Defaults

| Field | Type | Value |
|-------|------|-------|
| `username` | CharField | Fake username (Faker) |
| `email` | EmailField | Fake email (Faker) |
| `name` | CharField | Fake full name (Faker) |
| `password` | (post-generation) | 42-char with special chars |

### Password Handling

Passwords are handled via post-generation hook:
- Default: Generates strong 42-character password
- Custom: `UserFactory(password="MyPassword123!")` sets specific password

### Usage

#### Basic User Creation

```python
from read_comics.users.tests.factories import UserFactory, StaffFactory, SuperuserFactory

# Regular user
user = UserFactory()

# Staff user
staff = StaffFactory()

# Superuser
admin = SuperuserFactory()

# Custom credentials
user = UserFactory(
    username="john_doe",
    email="john@example.com",
    name="John Doe",
    password="SecurePassword123!"
)
```

#### In Tests

```python
@pytest.mark.django_db
def test_user_creation():
    user = UserFactory()
    assert user.username is not None
    assert user.is_active
    assert not user.is_staff

    staff = StaffFactory()
    assert staff.is_staff
    assert not staff.is_superuser

    admin = SuperuserFactory()
    assert admin.is_superuser
    assert admin.is_staff
```

#### Django ORM Integration

`django_get_or_create = ["username"]` means:
- Creating same username twice returns same object
- Useful for setUp code that might run multiple times

```python
user1 = UserFactory(username="john")
user2 = UserFactory(username="john")
assert user1.id == user2.id  # Same user
```

## Factory Inheritance and Composition

### Extending Factories

Create specialized factories by inheritance:

```python
class VolumeFactory(ComicvineSyncModelFactory):
    # Inherits: comicvine_id, comicvine_status, created_dt, etc.

    name = Faker("word")
    publisher = factory.SubFactory("read_comics.publishers.tests.factories.PublisherFactory")

    class Meta:
        model = Volume
```

### Multiple Inheritance

Factories can use multiple base classes:

```python
# Hypothetical factory combining multiple patterns
class UserWithManyIssuesFactory(UserFactory):
    # Inherits UserFactory behavior
    # Add custom fields
    is_premium = True
```

## Best Practices for Factories

1. **Use Faker** — Generate realistic fake data
   ```python
   name = Faker("word")  # ✅ Good
   name = "Test"         # ❌ Bad: too generic
   ```

2. **Avoid Overriding Built-ins** — Don't redefine parent fields unnecessarily
   ```python
   # ❌ Bad: unnecessary override
   class VolumeFactory(ComicvineSyncModelFactory):
       comicvine_id = factory.Sequence(lambda n: n + 1000)
   ```

3. **Document Post-Generation** — Comment when logic is non-obvious
   ```python
   @factory.post_generation
   def add_issues(self, create, extracted, **kwargs):
       """Creates specified number of related issues for volume"""
       if create and extracted:
           for i in range(extracted):
               IssueFactory(volume=self)
   ```

4. **Use SubFactory for Common Relationships**
   ```python
   # ✅ Good: automatic creation
   volume = VolumeFactory()  # Publisher auto-created

   # ❌ Bad: manual creation
   publisher = PublisherFactory()
   volume = VolumeFactory(publisher=publisher)
   ```

5. **Batch Creation for Collections**
   ```python
   # ✅ Good: clear intent
   volumes = VolumeFactory.create_batch(size=5)

   # ❌ Bad: manual loop
   volumes = [VolumeFactory() for _ in range(5)]
   ```

## Debugging Factories

### Check Generated Values

```python
from read_comics.volumes.tests.factories import VolumeFactory

# Print actual generated values
volume = VolumeFactory()
print(volume.name)
print(volume.comicvine_id)
print(volume.created_dt)
```

### Build vs. Create

```python
# Build: create object without saving
volume = VolumeFactory.build()
# Useful for checking defaults without DB

# Create: save to database
volume = VolumeFactory()
```

### Override Specific Fields

```python
# Keep defaults, override one field
volume = VolumeFactory(name="Custom Name")
```
