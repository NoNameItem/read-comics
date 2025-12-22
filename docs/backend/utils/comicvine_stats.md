# Comicvine stats helpers in `utils/comicvine_stats.py`

## Summary
- [`get_queued_stats`](#get_queued_stats) — gathers queued `ComicvineStatus` counts across each domain model and returns totals.
- [`get_matched_stats`](#get_matched_stats) — counts matched records (`ComicvineStatus.MATCHED`) per domain model and totals.
- [`get_not_matched_stats`](#get_not_matched_stats) — counts records with `NOT_MATCHED` status for each domain model.
- [`get_was_matched_stats`](#get_was_matched_stats) — counts objects that have ever been matched (non-null `comicvine_last_match`).
- [`get_not_actual_stats`](#get_not_actual_stats) — compares local timestamps with Mongo crawl dates for every domain model to find stale records.
- [`get_not_comicvine_actual_count`](#get_not_comicvine_actual_count) — shared helper counting stale rows for a specific model.

## Reference

### `get_queued_stats`
- Builds a stats dict where each domain (characters, concepts, issues, etc.) calls `.queued().count()` on its manager plus a `total` sum of all values.

### `get_matched_stats`
- Same structure as above but uses `.matched().count()` to report fully synced records.

### `get_not_matched_stats`
- Uses `.not_matched().count()` per domain model to report records that still lack a Comicvine match.

### `get_was_matched_stats`
- Uses `.was_matched().count()` to capture every record that was matched at least once (even if its current status changed to queued/unmatched).

### `get_not_actual_stats`
- Invokes `get_not_comicvine_actual_count` for each domain model (Character, Concept, Issue, Location, Object, Person, Power, Publisher, StoryArc, Team, Volume) and adds a `total` sum.

### `get_not_comicvine_actual_count`
- `model`: Django model class with `comicvine_status`, `comicvine_last_match`, and `COMICVINE_COLLECTION` attributes.
- Loads all non-queued objects, queries Mongo for the same Comicvine IDs, and counts how many either lack a `comicvine_last_match` or are stale compared to Mongo's `crawl_date` (converted to UTC).
