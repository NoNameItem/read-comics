# ZIP Download Module

## Summary

- **views.py**: Generic view for streaming zip file downloads of related content
- **zip_downloader.py**: Streaming zip creation with parallel file downloading

## Overview

The `zip_download` module provides a generic, reusable system for downloading collections of files as a single zip archive with server-side streaming. It supports two organization strategies: grouped by publisher/volume hierarchy or sequentially ordered, with concurrent downloads managed through gevent pools.

## Key Components

- `BaseZipDownloadView`: Generic HTTP view for zip downloads with configurable file organization
- `ZipDownloader`: Streaming zip file writer extending zipstream.ZipFile
- `Downloader`: Parallel file downloader with automatic retry logic

## Architecture

The module follows a layered approach:
1. **View Layer** (BaseZipDownloadView): Handles HTTP requests, file listing, and response streaming
2. **Download Layer** (ZipDownloader): Manages zip creation and streaming  
3. **I/O Layer** (Downloader): Handles concurrent downloads with retry logic

## Usage Pattern

Views inherit from `BaseZipDownloadView` and define:
- `base_model`: The Django model being browsed (Volume, StoryArc, etc.)
- `sublist_querysets`: An object implementing `HasGetIssuesQuerySetProtocol` to provide issues

The view then handles streaming the zip file with proper HTTP headers and filename encoding.

## References

- [views.md](views.md)
- [zip_downloader.md](zip_downloader.md)
