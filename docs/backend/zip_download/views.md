# ZIP Download Views

## Summary

- **BaseZipDownloadView**: Generic streaming HTTP view for zip file downloads with configurable file organization strategies

## Reference

### BaseZipDownloadView

Generic Django View for streaming zip downloads of related model content (typically issues).

#### Type Parameters

| Type Parameter | Bound To | Purpose |
|---|---|---|
| `ModelT` | `Model` | The Django model type for the base object being downloaded |

#### Configuration Attributes

| Attribute | Type | Default | Purpose |
|---|---|---|---|
| `sublist_querysets` | `HasGetIssuesQuerySetProtocol` | Required | Object providing `get_issues_queryset()` method |
| `base_model` | `type[ModelT]` | Required | Django model class to look up by slug |
| `base_slug_kwarg` | `str` | `"slug"` | URL kwarg name for the base object slug |

#### Protocols

**HasGetIssuesQuerySetProtocol**

```
def get_issues_queryset(obj: Model, user: User | None = None) -> QuerySet[Issue]
```

Interface that `sublist_querysets` must implement to provide related issues for a given object.

#### Methods

| Method | Parameters | Returns | Purpose |
|---|---|---|---|
| `escape_file_name(filename)` | `filename: str` | `str` | Static method sanitizing filenames by replacing `/`, `:`, `\t`, `\n` with spaces/dashes |
| `get_issues_queryset()` | — | `QuerySet[Issue]` | Gets issues from sublist_querysets or returns empty queryset if object not loaded |
| `get_base_object()` | — | `ModelT` | Retrieves base model object by slug from URL kwargs, raises 404 if not found |
| `get_grouped_filename(issue)` | `issue: Issue` | `str` | Generates hierarchical filename: `publisher/volume (year)/volume #number [name][space_key_suffix]` |
| `get_grouped_files()` | — | `list[tuple[str, str]]` | Returns list of (filename, download_link) tuples with grouped publisher/volume organization |
| `get_ordered_files()` | — | `list[tuple[str, str]]` | Returns list of (filename, download_link) tuples ordered by cover_date with zero-padded numeric prefixes |
| `get_zip_name()` | — | `str` | Generates zip archive filename from base object's string representation |
| `get(request, *args, **kwargs)` | `request: Request` | `StreamingHttpResponse` | HTTP GET handler handling file organization strategy and streaming zip response |

#### Details

**File Organization Strategies:**

1. **Grouped (default)**: Files organized by publisher/volume hierarchy
   - Path structure: `PublisherName/VolumeName (year)/VolumeName #IssueNumber [IssueName][space_key_suffix]`
   - Triggered by `?names=` query parameter (any value other than "ordered")
   - Preserves logical comic book organization

2. **Ordered**: Files ordered chronologically with numeric prefixes
   - Path structure: `001 - VolumeName #IssueNumber IssueName[space_key_suffix]`
   - Triggered by `?names=ordered` query parameter
   - Zero-padded prefix length calculated from total issue count
   - Ordering: `cover_date` → `volume__name` → `volume__start_year` → `numerical_number` → `number`

**Filename Sanitization:**

- Replaces forward slashes with " - "
- Replaces colons with " - "
- Replaces tabs with single space
- Replaces newlines with single space
- Appends last 4 characters of issue space_key (s3 location identifier)

**HTTP Response:**

- Content-Type: `application/zip`
- Streaming response with proper attachment header
- Filename set to `{zip_name}.zip`
