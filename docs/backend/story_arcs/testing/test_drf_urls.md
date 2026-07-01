# StoryArc URL Tests in `read_comics/story_arcs/tests/test_drf_urls.py`

## Summary

URL routing tests verifying correct URL patterns and reverse resolution for all StoryArc API endpoints.

## Test Class

### TestStoryArcsApiUrls

Static test class containing four URL routing tests for story_arcs endpoints.

## Test Methods

### test_list
**Endpoint:** `GET /api/story_arcs/` | **Fixtures:** None

Verifies `reverse("api:storyarc-list")` returns `/api/story_arcs/` and `resolve` returns view name `api:storyarc-list`.

### test_detail
**Endpoint:** `GET /api/story_arcs/{slug}/` | **Fixtures:** `storyarc_with_issues`

Verifies detail URL pattern accepts slug parameter and correctly resolves to `api:storyarc-detail`.

### test_technical_info
**Endpoint:** `GET /api/story_arcs/{slug}/technical-info/` | **Fixtures:** `storyarc_with_issues`

Verifies custom action URL pattern registered correctly with slug parameter.

### test_count
**Endpoint:** `GET /api/story_arcs/count/` | **Fixtures:** None

Verifies count action URL pattern registered as list route with view name `api:storyarc-count`.

## URL Pattern Structure

| Endpoint | URL Pattern | View Name | HTTP Method |
|---|---|---|---|
| List | `/api/story_arcs/` | `api:storyarc-list` | GET |
| Detail | `/api/story_arcs/{slug}/` | `api:storyarc-detail` | GET |
| Count | `/api/story_arcs/count/` | `api:storyarc-count` | GET |
| Technical Info | `/api/story_arcs/{slug}/technical-info/` | `api:storyarc-technical-info` | GET |

## Running Tests

```bash
docker-compose -f local.yml run --rm backend pytest read_comics/story_arcs/tests/test_drf_urls.py
```

## Related Components

- **ViewSet:** [`StoryArcViewSet`](../api/viewsets.md#storyarcviewset)
- **Endpoints:** [StoryArc API Endpoints](../api/endpoints.md)
