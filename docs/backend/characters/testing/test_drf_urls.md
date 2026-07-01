# Character URL Tests in `read_comics/characters/tests/test_drf_urls.py`

## Summary

URL routing tests verifying correct URL patterns and reverse resolution for all Character API endpoints.

## Test Class

### TestCharactersApiUrls

Static test class containing four URL routing tests for character endpoints.

**Purpose:** Verify bidirectional URL routing (reverse and resolve) for all character API endpoints

**Location:** `read_comics/characters/tests/test_drf_urls.py`

## Test Methods

### test_list

**Endpoint:** `GET /api/characters/`

**Fixtures used:** None

**Purpose:** Verify list endpoint URL routing

**Verifies:**
- `reverse("api:character-list")` returns `/api/characters/`
- `resolve("/api/characters/")` returns view name `api:character-list`

**Business logic verified:**
- URL pattern correctly registered in API router
- Reverse lookup matches expected URL format
- URL resolver correctly identifies view name

### test_detail

**Endpoint:** `GET /api/characters/{slug}/`

**Fixtures used:** `character_with_issues`

**Purpose:** Verify detail endpoint URL routing with dynamic slug parameter

**Verifies:**
- `reverse("api:character-detail", kwargs={"slug": slug})` returns `/api/characters/{slug}/`
- `resolve("/api/characters/{slug}/")` returns view name `api:character-detail`

**Business logic verified:**
- Detail URL pattern accepts slug parameter
- Slug-based routing works correctly
- URL pattern registered with correct view name

**Database access:** Requires database for creating character fixture

### test_technical_info

**Endpoint:** `GET /api/characters/{slug}/technical-info/`

**Fixtures used:** `character_with_issues`

**Purpose:** Verify technical info custom action URL routing

**Verifies:**
- `reverse("api:character-technical-info", kwargs={"slug": slug})` returns `/api/characters/{slug}/technical-info/`
- `resolve("/api/characters/{slug}/technical-info/")` returns view name `api:character-technical-info`

**Business logic verified:**
- Custom action URL pattern registered correctly
- Technical info action accessible via URL routing
- Slug parameter correctly passed to custom action

**Database access:** Requires database for creating character fixture

### test_count

**Endpoint:** `GET /api/characters/count/`

**Fixtures used:** None

**Purpose:** Verify count custom action URL routing

**Verifies:**
- `reverse("api:character-count")` returns `/api/characters/count/`
- `resolve("/api/characters/count/")` returns view name `api:character-count`

**Business logic verified:**
- Count action URL pattern registered as list route
- Custom action accessible without slug parameter
- URL routing distinguishes between list and count endpoints

## URL Pattern Structure

All character endpoints follow REST conventions:

| Endpoint | URL Pattern | View Name | HTTP Method |
|---|---|---|---|
| List | `/api/characters/` | `api:character-list` | GET |
| Detail | `/api/characters/{slug}/` | `api:character-detail` | GET |
| Count | `/api/characters/count/` | `api:character-count` | GET |
| Technical Info | `/api/characters/{slug}/technical-info/` | `api:character-technical-info` | GET |

## Running Tests

From repository root:

```bash
# Run all URL tests
docker-compose -f local.yml run --rm backend pytest read_comics/characters/tests/test_drf_urls.py

# Run specific test
docker-compose -f local.yml run --rm backend pytest read_comics/characters/tests/test_drf_urls.py::TestCharactersApiUrls::test_detail
```

## Related Components

- **ViewSet:** [`CharacterViewSet`](../api/viewsets.md#characterviewset)
- **Router:** `config/api_router.py` (DRF router registration)
- **Endpoints:** [Character API Endpoints](../api/endpoints.md)