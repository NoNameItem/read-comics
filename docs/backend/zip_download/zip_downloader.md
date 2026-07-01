# ZIP Downloader

## Summary

- **Downloader**: Parallel file downloader with gevent pool and automatic retry logic
- **ZipDownloader**: Streaming zip file writer extending zipstream.ZipFile for server-side streaming

## Reference

### Downloader

Manages parallel downloading of files with automatic retry strategy and temporary file handling.

#### Constructor

| Parameter | Type | Default | Purpose |
|---|---|---|---|
| `links` | `list[tuple[str, str]]` | Required | List of (filename, url) tuples to download |

#### Attributes

| Attribute | Type | Purpose |
|---|---|---|
| `links` | `list[tuple[str, str]]` | List of (filename, url) tuples to download |

#### Methods

| Method | Parameters | Returns | Purpose |
|---|---|---|---|
| `download_file(link)` | `link: tuple[str, str]` | `tuple[str, TemporaryFile]` | Downloads single file from URL with retry strategy, returns (filename, file_object) |
| `__iter__()` | — | Iterator of `tuple[str, TemporaryFile]` | Generator yielding downloaded files using gevent pool |

#### Details

**Parallel Downloading:**

- Uses gevent pool with 5 concurrent workers
- Pool.imap_unordered: Results returned in completion order, not request order
- Maxsize of 5 queued tasks per worker

**Retry Strategy:**

- Total retries: 3
- Status codes triggering retry: 429 (Too Many Requests), 500, 502 (Bad Gateway), 503 (Service Unavailable), 504 (Gateway Timeout)
- Allowed methods for retry: HEAD, GET, OPTIONS
- Uses HTTPAdapter with urllib3.Retry

**Temporary File Storage:**

- Each downloaded file stored in `tempfile.TemporaryFile()`
- File pointer seeked to start (position 0) before returning
- Caller responsible for closing file after use

---

### ZipDownloader

Streaming zip file writer extending zipstream.ZipFile for creating zip archives from remote file URLs with parallel downloading and server-side streaming.

#### Constructor

| Parameter | Type | Default | Purpose |
|---|---|---|---|
| `fileobj` | file-like | `None` | File object to write zip data to (if None, uses BytesIO) |
| `mode` | `str` | `"w"` | Zip file mode (typically "w" for write) |
| `compression` | int | `ZIP_DEFLATED` | Compression method (ZIP_DEFLATED for standard compression) |
| `allowZip64` | `bool` | `False` | Allow zip64 format for large archives |
| `request` | Django Request | `None` | Django request object for session/authentication access |

#### Attributes

| Attribute | Type | Purpose |
|---|---|---|
| `links` | `list[tuple[str, str]]` | Accumulated list of (filename, url) tuples |
| `links_compress_type` | int or None | Compression type for link files |
| `links_buffersize` | int or None | Buffer size for reading downloaded files |
| `request` | Django Request | Request object (for potential future download limiting) |

#### Methods

| Method | Parameters | Returns | Purpose |
|---|---|---|---|
| `write_links(links, compress_type, buffer_size)` | `links: list[tuple[str, str]]`, `compress_type: int or None`, `buffer_size: int or None` | None | Adds links to download queue with optional compression and buffer settings |
| `flush()` | — | Iterator of bytes | Generator yielding zip file chunks and downloaded file content |

#### Details

**Streaming Architecture:**

- Extends `zipstream.ZipFile` which generates zip data on-the-fly without buffering entire archive in memory
- `flush()` method is a generator that yields zip file chunks incrementally
- Combines local zip data (from `paths_to_write`) with remote file downloads

**Download Process:**

1. First writes any local files queued in `paths_to_write` (inherited from zipstream)
2. Then creates Downloader instance with accumulated links
3. Iterates through downloaded files, writing each to zip archive
4. Closes temporary files after writing to zip

**Implementation Notes:**

- Uses private method `_ZipFile__write()` to write individual files to zip (name mangling for Python's private method access)
- Comment-out code (lines 64-74) shows incomplete download rate limiting based on:
  - User authentication status
  - `unlimited_downloads` user flag
  - Django setting `DOWNLOAD_TIMEOUT`
  - Session storage of last download timestamp
- Catches and re-raises exceptions from download process
- Default compression uses ZIP_DEFLATED (standard compression)

**Integration with BaseZipDownloadView:**

```python
z = ZipDownloader(compression=ZIP_DEFLATED, allowZip64=True, request=request)
z.write_links(files)  # files from get_grouped_files() or get_ordered_files()
response = StreamingHttpResponse(z, content_type="application/zip")
```

The ZipDownloader generator is passed directly to StreamingHttpResponse, which iterates through it to stream the zip file to the client.
