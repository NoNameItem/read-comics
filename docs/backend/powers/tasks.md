# Powers Tasks

## Summary

- **`PowerComicvineInfoTask`** — Syncs power data from MongoDB to PostgreSQL
- **`PowersRefreshTask`** — Full refresh of all power data from PostgreSQL
- **Spider tasks** — Fetches power data from ComicVine API and caches in MongoDB (4 variants with incremental/skip-existing strategies)

## Reference

### PowerComicvineInfoTask

ComicVine sync task for Power model. Inherits from `BaseComicvineInfoTask`.

**Configuration**:
- **Model**: `Power` (APP_LABEL: `powers`)
- **Purpose**: Sync power data from MongoDB cache → PostgreSQL

**Lifecycle**:
1. Fetches power data from MongoDB collection `comicvine_powers`
2. Maps ComicVine fields to Django model via field name matching
3. Updates/creates Power records in PostgreSQL

**Task name**: `read_comics.powers.tasks.power_comicvine_info_task`

### PowersRefreshTask

Full refresh task for all powers. Inherits from `BaseRefreshTask`.

**Configuration**:
- **Model**: `Power` (APP_LABEL: `powers`)
- **Purpose**: Refresh all power data from PostgreSQL database

**Task name**: `read_comics.powers.tasks.powers_refresh_task`

### Spider Tasks

Scrapy spider tasks fetch power data from ComicVine API and store in MongoDB.

#### powers_increment_update

Incremental update, don't skip existing powers.

```python
@shared_task
def powers_increment_update() -> None
```

**Behavior**: Fetches new powers since last run, updates existing power records.

#### powers_skip_existing_increment_update

Incremental update, skip powers already in MongoDB.

```python
@shared_task
def powers_skip_existing_increment_update() -> None
```

**Behavior**: Fetches new powers only, avoids re-fetching existing data.

#### powers_skip_existing_update

Full update, skip powers already in MongoDB.

```python
@shared_task
def powers_skip_existing_update() -> None
```

**Behavior**: Fetches all powers from ComicVine, but skips those already cached in MongoDB.

#### powers_update

Full update, don't skip existing powers.

```python
@shared_task
def powers_update() -> None
```

**Behavior**: Fetches all powers from ComicVine API, updates all existing records, adds new powers.

#### Configuration

All spider tasks:
- **Spider class**: `PowersSpider`
- **Queue**: `read_comics_spiders` (for web scraping tasks)
- **Storage**: MongoDB collection `comicvine_powers`
- **Downstream**: Data processed by `PowerComicvineInfoTask` for PostgreSQL sync

**Task names**:
- `read_comics.powers.tasks.powers_increment_update`
- `read_comics.powers.tasks.powers_skip_existing_increment_update`
- `read_comics.powers.tasks.powers_skip_existing_update`
- `read_comics.powers.tasks.powers_update`