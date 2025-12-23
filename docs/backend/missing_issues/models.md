# Missing Issues Models

## Summary

- **`Locks`** — Simple distributed lock mechanism for synchronization
- **`APIQueue`** — Queue for tracking entities needing API synchronization
- **`IgnoredPublisher`** — Tracks publishers excluded from missing issue tracking
- **`IgnoredVolume`** — Tracks volumes excluded from missing issue tracking
- **`IgnoredIssue`** — Tracks individual issues excluded from missing issue tracking
- **`MissingIssue`** — Core model for issues not yet in the system with ComicVine data and related entity links
- **`WatchedItem`** — Generic relation allowing users to watch any comic entity for missing issues

## Reference

### Locks

Simple distributed lock model for task synchronization.

| Field | Type | Purpose |
|-------|------|---------|
| `code` | CharField(100, unique) | Unique lock identifier |
| `dttm` | DateTimeField | Lock timestamp |

**Usage**: Prevents simultaneous execution of critical tasks.

---

### APIQueue

Queue for tracking entities that need API synchronization.

| Field | Type | Purpose |
|-------|------|---------|
| `endpoint` | TextField | ComicVine API endpoint path |
| `comicvine_id` | IntegerField | ComicVine ID of entity |
| `added_in_queue` | DateTimeField | Timestamp when added (auto) |

**Purpose**: Tracks pending API syncs for characters, people, teams, etc.

---

### IgnoredPublisher

Publisher entries excluded from missing issue tracking.

| Field | Type | Purpose |
|-------|------|---------|
| `comicvine_id` | IntegerField(unique) | ComicVine publisher ID |
| `comicvine_url` | URLField | ComicVine publisher URL |
| `name` | TextField | Publisher name |

**Usage**: When a publisher is ignored, all its missing issues are deleted.

---

### IgnoredVolume

Volume entries excluded from missing issue tracking.

| Field | Type | Purpose |
|-------|------|---------|
| `comicvine_id` | IntegerField(unique) | ComicVine volume ID |
| `comicvine_url` | URLField | ComicVine volume URL |
| `name` | TextField | Volume name |
| `start_year` | CharField | Volume start year |
| `publisher_name` | TextField | Associated publisher name |
| `publisher_comicvine_id` | IntegerField | Associated publisher ComicVine ID |

**Usage**: When a volume is ignored, all its missing issues are deleted.

---

### IgnoredIssue

Individual issue entries excluded from missing issue tracking.

| Field | Type | Purpose |
|-------|------|---------|
| `comicvine_id` | IntegerField(unique) | ComicVine issue ID |
| `comicvine_url` | URLField | ComicVine issue URL |
| `name` | TextField | Issue name/title |
| `number` | CharField | Issue number |
| `cover_date` | DateField | Issue cover date |
| `volume_comicvine_id` | IntegerField | Related volume ID |
| `volume_comicvine_url` | URLField | Related volume URL |
| `volume_name` | TextField | Related volume name |
| `volume_start_year` | CharField | Related volume start year |
| `publisher_name` | TextField | Related publisher name |
| `publisher_comicvine_id` | IntegerField | Related publisher ID |

**Usage**: Archives individual issues user chose to ignore.

---

### MissingIssue

Core model representing issues not yet imported into the system.

**Purpose**: Tracks comic issues found in ComicVine that aren't yet in PostgreSQL, with relationships to all related comic entities.

#### Fields - Issue Data

| Field | Type | Purpose |
|-------|------|---------|
| `comicvine_id` | IntegerField(unique) | ComicVine issue ID |
| `comicvine_url` | URLField | ComicVine issue URL |
| `name` | TextField | Issue title/name |
| `number` | CharField | Issue number (e.g., "1", "1.5", "½") |
| `numerical_number` | FloatField | Parsed numeric version (0.5, 1.0, 100.0, etc.) |
| `cover_date` | DateField | Issue cover/publication date |

#### Fields - Volume/Publisher Data

| Field | Type | Purpose |
|-------|------|---------|
| `volume_comicvine_id` | IntegerField | Related Volume ComicVine ID |
| `volume_comicvine_url` | URLField | Related Volume URL |
| `volume_name` | TextField | Related Volume name |
| `volume_start_year` | CharField | Related Volume start year |
| `publisher_name` | TextField | Related Publisher name |
| `publisher_comicvine_id` | IntegerField | Related Publisher ComicVine ID |
| `publisher_comicvine_url` | URLField | Related Publisher URL |

#### Relations to Comic Entities (M2M)

| Field | Type | Purpose |
|-------|------|---------|
| `characters` | M2M | Characters appearing in issue |
| `concepts` | M2M | Concepts featured in issue |
| `locations` | M2M | Locations in issue |
| `objects_in` | M2M | Objects/equipment in issue |
| `people` | M2M | Creators/people involved |
| `story_arcs` | M2M | Story arcs featured |
| `teams` | M2M | Teams appearing in issue |
| `volume` | FK | Parent Volume (nullable) |
| `publisher` | FK | Parent Publisher (nullable) |

#### Skip/Ignore Fields

| Field | Type | Purpose |
|-------|------|---------|
| `skip` | BooleanField | Whether user skipped this issue |
| `skip_date` | DateField | When issue was skipped |

**Skip logic**: If skip expires (`skip_date < today - SKIP_DAYS`), skip is automatically cleared.

#### Methods

| Method | Purpose |
|--------|---------|
| `set_numerical_number()` | Parse `number` field into numeric float (handles "½", "1.5", etc.) |
| `ignore_publisher()` | Create IgnoredPublisher entry and delete all missing issues from publisher |
| `ignore_volume()` | Create IgnoredVolume entry and delete all missing issues from volume |
| `ignore()` | Create IgnoredIssue entry and delete self |
| `__str__()` | Returns formatted string: "Volume Name #Number [Title]" |

#### Properties - DigitalOcean Spaces Paths

Methods return sanitized paths for storing data in Spaces (replaces `:` with `*_*`, `/` with `*@*`):

| Property | Purpose |
|----------|---------|
| `publisher_space_path` | Path: `{publisher_name} [{comicvine_id}]` |
| `volume_space_path` | Path: `{volume_name} [{year}] [{comicvine_id}]` |
| `issue_space_path` | Path: `{volume_name} #{number} [{comicvine_id}]` |

---

### WatchedItem

Generic relation allowing users to watch any comic entity (Character, Volume, Person, etc.) for missing issues.

| Field | Type | Purpose |
|-------|------|---------|
| `user` | FK | User who is watching |
| `content_type` | FK | Django ContentType (which model is watched) |
| `object_id` | BigIntegerField | ID of watched object |
| `content_object` | GenericFK | Reference to actual watched object |

**Constraint**: `unique_together = [["user", "content_type", "object_id"]]` — Each user can watch each entity only once.

**Usage**: When an entity with watchers gets missing issues identified, users are notified.