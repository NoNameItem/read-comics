# Missing Issues DigitalOcean Spaces Integration

## Summary

- **`get_level(prefix="")`** — Lists and filters objects in DigitalOcean Spaces bucket at given path level

## Reference

### get_level(prefix="")

Lists objects and directories in DigitalOcean Spaces bucket at specified prefix depth.

**Parameters**:
- `prefix` (str, default `""`) — S3 prefix/path to list (e.g., `"Publisher Name [123]/Volume Name [2020]/"`

**Returns**: List of dicts with structure:
```python
{
    "name": str,              # Object name without prefix
    "full_name": str,         # Full S3 key path
    "size": int,              # Size in bytes (0 for directories)
}
```

#### Behavior

1. **Connects to DigitalOcean Spaces** via boto3 S3 resource (uses settings: `DO_SPACE_DATA_*`)
2. **Lists with delimiter** (`/`) to get one level of hierarchy
3. **Paginates** through results using `NextMarker`
4. **Filters** out:
   - Hidden files (starting with `.`)
   - AWS metadata (starting with `@ea`)
5. **Sorts** results alphabetically by name
6. **Returns** combined directory and file listings

#### S3 Configuration

Uses settings for connection:
- `DO_SPACE_DATA_REGION` — AWS region
- `DO_SPACE_DATA_ENDPOINT_URL` — DigitalOcean Spaces endpoint
- `DO_SPACE_DATA_KEY` — AWS access key
- `DO_SPACE_DATA_SECRET` — AWS secret key
- `DO_SPACE_DATA_BUCKET` — Bucket name

#### Usage Context

**Purpose**: Navigate DigitalOcean Spaces directory structure for missing issue assets.

**Path structure**:
```
/{publisher_name}_{id}/
  /{volume_name}_{year}_{id}/
    /{issue_name}_{id}/
      [image files, metadata, etc.]
```

Paths use sanitization (`:` → `*_*`, `/` → `*@*`) per `MissingIssue` space path properties.

#### Implementation Details

- **Regex filter**: `ONE_LEVEL_REGEX = r"^[^\/]+\/?$"` — Matches single-level paths (unused in current implementation but available)
- **Marker-based pagination** — Handles large buckets efficiently
- **Deduplication** — Uses `processed` set to prevent duplicate entries during pagination
- **Size handling** — Directories (CommonPrefixes) have size 0; files have actual byte size