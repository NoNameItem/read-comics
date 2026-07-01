# Missing Issues Management Commands

## Summary

- **`clearqueue`** — Django management command to clear API synchronization queue (all or specific endpoints)

## Reference

### clearqueue

Clears entries from the `APIQueue` model.

**Usage**:
```bash
# Clear entire queue
python manage.py clearqueue

# Clear specific endpoints
python manage.py clearqueue comicvine_characters comicvine_volumes comicvine_people
```

**Arguments**:
- `endpoints` — One or more MongoDB collection names (required positional arguments)

**Endpoint examples**:
- `comicvine_characters` (from `Character.MONGO_COLLECTION`)
- `comicvine_volumes` (from `Volume.MONGO_COLLECTION`)
- `comicvine_people` (from `Person.MONGO_COLLECTION`)
- `comicvine_teams` (from `Team.MONGO_COLLECTION`)
- And all other ComicVine entity collections

#### Behavior

1. **If no endpoints provided** — Deletes all `APIQueue` records
   - Output: `"Cleared all queues"`

2. **If endpoints provided** — For each endpoint:
   - Deletes `APIQueue` records matching that endpoint name
   - Output: `"Cleared {endpoint} queue"`

#### Implementation

- Uses Django `BaseCommand` class
- Custom argument parser via `add_arguments()`
- Styled output via `self.stdout.write(self.style.SUCCESS(...))`

#### Purpose

Removes entities from the API synchronization queue stored in `APIQueue` model. Typically used when:
- Queue gets stuck or corrupted
- Need to force re-sync of specific ComicVine collections
- Clearing stale sync requests

**Related model**: `APIQueue` stores `endpoint` (collection name) and `comicvine_id` (entity ID) for tracking.

#### Example

```bash
# Clear queue for character and person syncs
python manage.py clearqueue comicvine_characters comicvine_people

# Output:
# Cleared comicvine_characters queue
# Cleared comicvine_people queue

# Clear entire queue
python manage.py clearqueue

# Output:
# Cleared all queues
```