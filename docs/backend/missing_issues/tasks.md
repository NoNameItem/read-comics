# Missing Issues Tasks

## Summary

- **`BaseMissingIssuesTask`** — Base Celery task syncing missing issues from MongoDB to PostgreSQL with ignore filtering
- **Entity-specific tasks** — 8 task classes for Volume, Publisher, Character, Concept, Location, Object, Person, StoryArc, Team missing issues

## Reference

### BaseMissingIssuesTask

Base Celery task that identifies missing issues for an entity by comparing MongoDB ComicVine data against PostgreSQL.

**Inheritance**: Celery `Task`

**Resilience**:
- Auto-retries on `OperationalError`, `WorkerLostError`, `CursorNotFound`
- Max 10 retries with exponential backoff (up to 60 seconds)

#### Configuration

| Attribute | Value | Purpose |
|-----------|-------|---------|
| `MONGO_COLLECTION` | `comicvine_issues` | MongoDB collection to query |
| `FILTER_PATH` | None (subclass override) | MongoDB path filter (e.g., `character_credits.id`) |
| `MODEL` | None (subclass override) | Django model being processed (Volume, Character, etc.) |
| `LOOKUP` | Aggregation pipeline | Joins issues with volumes, extracts volume data |
| `PROJECT` | Aggregation pipeline | Maps MongoDB fields to MissingIssue fields |

#### Key Methods

| Method | Purpose |
|--------|---------|
| `get_existing_issues(obj)` | Returns ComicVine IDs of issues already in system for entity |
| `get_ignored_issues()` | Returns ComicVine IDs of ignored issues |
| `get_ignored_volumes()` | Returns ComicVine IDs of ignored volumes |
| `get_ignored_publishers()` | Returns ComicVine IDs of ignored publishers |
| `get_match(obj)` | Builds MongoDB aggregation filter matching entity, excluding existing/ignored |
| `get_issues_from_mongo(obj)` | Executes MongoDB aggregation to fetch missing issues for entity |
| `get_or_create_missing_issue(mongo_issue)` | Creates/updates MissingIssue record; deletes if issue was added to system |
| `add_missing_issue(obj, missing_issue)` | Links missing issue to entity |
| `process_mongo_issues(obj, issues)` | Processes list of MongoDB issues, filtering ignored items |
| `get_objects()` | Returns entities with >0 issues or watchers (for full sync) |
| `check_object(obj)` | Validates entity should be processed (has issues or watchers) |
| `run(pk=None)` | Main task entry point — processes single entity or all entities |

#### MongoDB Aggregation Pipeline

1. **Match** — Filter issues by entity (via FILTER_PATH) and exclude existing/ignored
2. **Lookup volumes** — Join with comicvine_volumes collection
3. **Match** — Filter by non-ignored publishers
4. **Lookup publishers** — Join with comicvine_publishers
5. **Project** — Map to MissingIssue field structure

#### Skip Logic

- Issues with `skip=True` are auto-reset after `SKIP_DAYS` (if skip_date is old)
- Allows user to temporarily skip issues that appear multiple times during updates

#### Run Modes

1. **Single entity**: `run(pk=obj.pk)` — Process specific entity
2. **Batch**: `run()` — Process all entities with issues/watchers, spawning individual tasks per entity

---

### VolumeMissingIssuesTask

Missing issues task for Volume model.

```python
class VolumeMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "volume.id"
    MODEL = Volume
```

**Task name**: `read_comics.missing_issues.tasks.volume_missing_issues_task`

**Behavior**: Finds ComicVine issues in target volume not yet in PostgreSQL.

---

### PublisherMissingIssuesTask

Missing issues task for Publisher model. Overrides base methods to handle publisher-wide searches.

```python
class PublisherMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "volume.publisher.id"
    MODEL = Publisher
```

**Special behavior**:
- **get_objects()** — Excludes ignored publishers via subquery
- **check_object()** — Returns False if publisher is in IgnoredPublisher
- **get_match()** — Custom filter that looks up all volumes for publisher in MongoDB first
- **get_issues_from_mongo()** — Skips FILTER_PATH matching; uses pre-fetched volume IDs instead

**Task name**: `read_comics.missing_issues.tasks.publisher_missing_issues_task`

---

### CharacterMissingIssuesTask

Missing issues task for Character model.

```python
class CharacterMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "character_credits.id"
    MODEL = Character
```

**Task name**: `read_comics.missing_issues.tasks.character_missing_issues_task`

---

### ConceptMissingIssuesTask

Missing issues task for Concept model.

```python
class ConceptMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "concept_credits.id"
    MODEL = Concept
```

**Task name**: `read_comics.missing_issues.tasks.concept_missing_issues_task`

---

### LocationMissingIssuesTask

Missing issues task for Location model.

```python
class LocationMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "location_credits.id"
    MODEL = Location
```

**Task name**: `read_comics.missing_issues.tasks.location_missing_issues_task`

---

### ObjectMissingIssuesTask

Missing issues task for Object model.

```python
class ObjectMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "object_credits.id"
    MODEL = Object
```

**Task name**: `read_comics.missing_issues.tasks.object_missing_issues_task`

---

### PersonMissingIssuesTask

Missing issues task for Person (creator/contributor) model.

```python
class PersonMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "person_credits.id"
    MODEL = Person
```

**Task name**: `read_comics.missing_issues.tasks.person_missing_issues_task`

---

### StoryArcMissingIssuesTask

Missing issues task for StoryArc model.

```python
class StoryArcMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "story_arc_credits.id"
    MODEL = StoryArc
```

**Task name**: `read_comics.missing_issues.tasks.story_arc_missing_issues_task`

---

### TeamMissingIssuesTask

Missing issues task for Team model.

```python
class TeamMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "team_credits.id"
    MODEL = Team
```

**Task name**: `read_comics.missing_issues.tasks.team_missing_issues_task`

---

## Task Lifecycle

1. **Entity sync task** (e.g., `PersonComicvineInfoTask`) completes
2. **Triggers** corresponding missing issues task: `PersonMissingIssuesTask.delay(pk=person.pk)`
3. **Missing issues task**:
   - Queries MongoDB for issues with `person_credits.id = person.comicvine_id`
   - Excludes issues already in `Issue` table
   - Excludes issues/volumes/publishers in ignore lists
   - Creates/updates `MissingIssue` records
   - Links via M2M relationship `missing_issue.people.add(person)`

## Integration Points

**Triggered by**: All entity sync tasks via `MISSING_ISSUES_TASK` configuration:
- `CharacterComicvineInfoTask` → `CharacterMissingIssuesTask`
- `PersonComicvineInfoTask` → `PersonMissingIssuesTask`
- `TeamComicvineInfoTask` → `TeamMissingIssuesTask`
- (and all other entity sync tasks)

**Queue**: Entity-specific queue (e.g., `read_comics_characters` for character missing issues)