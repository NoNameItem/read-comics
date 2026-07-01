# People Tasks

## Summary

- **`PersonComicvineInfoTask`** — Syncs person data from MongoDB to PostgreSQL, triggers missing issues processing
- **`PeopleRefreshTask`** — Full refresh of all person data from PostgreSQL
- **Spider tasks** — Fetches person data from ComicVine API and caches in MongoDB (4 variants with incremental/skip-existing strategies)

## Reference

### PersonComicvineInfoTask

ComicVine sync task for Person model. Inherits from `BaseComicvineInfoTask`.

**Configuration**:
- **Model**: `Person` (APP_LABEL: `people`)
- **Missing issues task**: `read_comics.missing_issues.tasks.PersonMissingIssuesTask`
- **Purpose**: Sync person data from MongoDB cache → PostgreSQL, then queue missing issues for processing

**Lifecycle**:
1. Fetches person data from MongoDB collection `comicvine_people`
2. Maps ComicVine fields to Django model via `FIELD_MAPPING`
3. Updates/creates Person records in PostgreSQL
4. Triggers PersonMissingIssuesTask to identify gaps in related issues

**Task name**: `read_comics.people.tasks.person_comicvine_info_task`

### PeopleRefreshTask

Full refresh task for all persons. Inherits from `BaseRefreshTask`.

**Configuration**:
- **Model**: `Person` (APP_LABEL: `people`)
- **Purpose**: Refresh all person data from PostgreSQL database

**Task name**: `read_comics.people.tasks.people_refresh_task`

### Spider Tasks

Scrapy spider tasks fetch person data from ComicVine API and store in MongoDB.

#### people_increment_update

Incremental update, don't skip existing persons.

```python
@shared_task
def people_increment_update() -> None
```

**Behavior**: Fetches new persons since last run, updates existing person records.

#### people_skip_existing_increment_update

Incremental update, skip persons already in MongoDB.

```python
@shared_task
def people_skip_existing_increment_update() -> None
```

**Behavior**: Fetches new persons only, avoids re-fetching existing data.

#### people_skip_existing_update

Full update, skip persons already in MongoDB.

```python
@shared_task
def people_skip_existing_update() -> None
```

**Behavior**: Fetches all persons from ComicVine, but skips those already cached in MongoDB.

#### people_update

Full update, don't skip existing persons.

```python
@shared_task
def people_update() -> None
```

**Behavior**: Fetches all persons from ComicVine API, updates all existing records, adds new persons.

#### Configuration

All spider tasks:
- **Spider class**: `PeopleSpider`
- **Queue**: `read_comics_spiders` (for web scraping tasks)
- **Storage**: MongoDB collection `comicvine_people`
- **Downstream**: Data processed by `PersonComicvineInfoTask` for PostgreSQL sync

**Task names**:
- `read_comics.people.tasks.people_increment_update`
- `read_comics.people.tasks.people_skip_existing_increment_update`
- `read_comics.people.tasks.people_skip_existing_update`
- `read_comics.people.tasks.people_update`