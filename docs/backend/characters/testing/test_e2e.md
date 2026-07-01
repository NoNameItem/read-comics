# Character E2E Tests in `read_comics/characters/tests/test_e2e.py`

## Summary

End-to-end API tests verifying complete workflows for Character endpoints including list, detail, count, and technical-info actions with various filters, ordering, pagination, and authorization scenarios.

**Pytest marks:** `pytestmark = pytest.mark.django_db` (all tests require database)

## Test Classes

- [`TestCharactersCount`](#testcharacterscount) - Count endpoint tests (2 methods)
- [`TestCharactersList`](#testcharacterslist) - List endpoint tests (13 methods)
- [`TestCharacterDetail`](#testcharacterdetail) - Detail endpoint tests (3 methods)
- [`TestCharacterTechnicalInfo`](#testcharactertechnicalinfo) - Technical info authorization tests (5 methods)
- [`TestCharactersParametrized`](#testcharactersparametrized) - Parametrized ordering tests (1 method, 6 variations)
- [`TestCharactersEdgeCases`](#testcharactersedgecases) - Edge case and boundary tests (7 methods)
- [`TestCharactersConsistency`](#testcharactersconsistency) - Cross-endpoint consistency tests (6 methods)
- [`TestCharactersHTTPMethods`](#testcharactershttpmethods) - HTTP method validation tests (9 methods)
- [`TestCharactersCrossEndpoint`](#testcharacterscrossendpoint) - Integration tests (5 methods)

## Reference

### TestCharactersCount

Tests for count endpoint behavior with filtering.

#### test_no_show_all

**Endpoint:** `GET /api/characters/count/`

**Fixtures used:** `api_client`, `characters_no_issues`, `characters_with_issues`

**Purpose:** Verify default count excludes characters without issues

**Business logic verified:**
- Count endpoint returns only characters with issues by default
- Returns status 200
- Response includes `count` field matching length of `characters_with_issues`
- Characters without issues are filtered out

#### test_show_all

**Endpoint:** `GET /api/characters/count/?show-all=yes`

**Fixtures used:** `api_client`, `characters_no_issues`, `characters_with_issues`

**Purpose:** Verify show-all filter includes all characters

**Business logic verified:**
- Count endpoint with `show-all=yes` includes all characters
- Returns status 200
- Response includes `count` field matching total of both fixtures
- No filtering applied when show-all enabled

### TestCharactersList

Tests for list endpoint with pagination, filtering, ordering, and data validation.

**Expected response fields:**

| Field | Type | Purpose |
|---|---|---|
| `slug` | String | Character URL slug |
| `image` | String | Character image URL |
| `publisher__name` | String | Publisher name (nested) |
| `publisher__image` | String | Publisher image URL (nested) |
| `publisher__slug` | String | Publisher URL slug (nested) |
| `name` | String | Character display name |
| `short_description` | Text | Brief character description |
| `issues_count` | Integer | Count of related issues |
| `volumes_count` | Integer | Count of distinct volumes |

#### test_no_show_all

**Endpoint:** `GET /api/characters/`

**Fixtures used:** `api_client`, `characters_no_issues`, `characters_with_issues`

**Purpose:** Verify default list excludes characters without issues

**Business logic verified:**
- List returns only characters with issues by default
- Response count matches `characters_with_issues` length
- All response items contain expected fields (9 fields)
- Flattened response structure matches expected keys

#### test_show_all

**Endpoint:** `GET /api/characters/?show-all=yes`

**Fixtures used:** `api_client`, `characters_no_issues`, `characters_with_issues`

**Purpose:** Verify show-all filter includes all characters

**Business logic verified:**
- List with `show-all=yes` includes all characters
- Response count matches total of both fixtures
- All response items contain expected fields
- Filtering disabled when show-all enabled

#### test_data

**Endpoint:** `GET /api/characters/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify response data accuracy against database

**Business logic verified:**
- Response fields match database values
- Publisher nested data correct (name, slug)
- Issues count calculated correctly
- Volumes count aggregated correctly (distinct volumes from issues)
- Null handling for optional publisher field

#### test_default_ordering_by_name

**Endpoint:** `GET /api/characters/`

**Fixtures used:** `api_client`, `characters_with_issues`

**Purpose:** Verify default ordering is by name ascending

**Business logic verified:**
- Default ordering applied when no `ordering` parameter provided
- Names returned in alphabetical order
- Ordering stable across requests

#### test_ordering_by_name_ascending

**Endpoint:** `GET /api/characters/?ordering=name`

**Fixtures used:** `api_client`, `characters_with_issues`

**Purpose:** Verify explicit name ascending ordering

**Business logic verified:**
- `ordering=name` sorts by name A-Z
- Ordering matches Python's sorted() behavior

#### test_ordering_by_name_descending

**Endpoint:** `GET /api/characters/?ordering=-name`

**Fixtures used:** `api_client`, `characters_with_issues`

**Purpose:** Verify name descending ordering

**Business logic verified:**
- `ordering=-name` sorts by name Z-A
- Reverse ordering applied correctly

#### test_ordering_by_issues_count_ascending

**Endpoint:** `GET /api/characters/?ordering=issues_count`

**Fixtures used:** `api_client`, `characters_with_issues`

**Purpose:** Verify ordering by issues count ascending

**Business logic verified:**
- `ordering=issues_count` sorts by issue count low to high
- Annotated field ordering works correctly

#### test_ordering_by_issues_count_descending

**Endpoint:** `GET /api/characters/?ordering=-issues_count`

**Fixtures used:** `api_client`, `characters_with_issues`

**Purpose:** Verify ordering by issues count descending

**Business logic verified:**
- `ordering=-issues_count` sorts by issue count high to low
- Reverse annotated ordering works

#### test_ordering_by_volumes_count_ascending

**Endpoint:** `GET /api/characters/?ordering=volumes_count`

**Fixtures used:** `api_client`, `characters_with_issues`

**Purpose:** Verify ordering by volumes count ascending

**Business logic verified:**
- `ordering=volumes_count` sorts by distinct volume count low to high
- Aggregated field ordering works correctly

#### test_invalid_ordering_field

**Endpoint:** `GET /api/characters/?ordering=invalid_field`

**Fixtures used:** `api_client`, `characters_with_issues`

**Purpose:** Verify graceful handling of invalid ordering field

**Business logic verified:**
- Invalid ordering parameter ignored
- Falls back to default ordering (name)
- Returns 200 status instead of error

#### test_pagination_invalid_page

**Endpoint:** `GET /api/characters/?page=999`

**Fixtures used:** `api_client`, `characters_with_issues`

**Purpose:** Verify pagination error handling for out-of-range page

**Business logic verified:**
- Out-of-range page returns 404
- Pagination validates page number

#### test_ordering_by_volumes_count_descending (in TestCharacterTechnicalInfo)

**Note:** This test appears duplicated in TestCharacterTechnicalInfo class but belongs in TestCharactersList

### TestCharacterDetail

Tests for detail endpoint with various character states.

**Expected response fields:**

| Field | Type | Purpose |
|---|---|---|
| `slug` | String | Character URL slug |
| `name` | String | Character display name |
| `real_name` | String | Character's real name |
| `publisher` | Object | Nested publisher data (name, slug) |
| `aliases` | List | List of character aliases |
| `birth` | Date | Character birth date (ISO format) |
| `gender` | String | Gender display value |
| `powers` | List | List of power names |
| `first_issue_name` | String | First appearance issue name |
| `first_issue_slug` | String | First appearance issue slug |
| `comicvine_url` | String | ComicVine API URL |
| `short_description` | Text | Brief description |
| `description` | Text | Full description |
| `download_size` | String | Total download size (formatted) |
| `download_link` | String | Download link URL |

#### test_with_first_issue

**Endpoint:** `GET /api/characters/{slug}/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify detail response with complete character data

**Business logic verified:**
- All detail fields present and accurate
- Publisher nested data correct
- Aliases converted from newline-separated to list
- Birth date formatted as ISO date
- Gender enum converted to display value
- Powers list contains power names
- First issue data populated (name and slug)
- ComicVine URL generated correctly
- Download size formatted with humanized units
- Download link includes test server domain

#### test_no_first_issue

**Endpoint:** `GET /api/characters/{slug}/`

**Fixtures used:** `api_client`, `character_no_issues`

**Purpose:** Verify detail response for character without issues

**Business logic verified:**
- First issue name falls back to `first_issue_name` field
- First issue slug is None when no related issue
- Download size shows "0 bytes" when no issues
- Other fields still populated correctly

#### test_not_found

**Endpoint:** `GET /api/characters/does-not-exist/`

**Fixtures used:** `api_client`

**Purpose:** Verify 404 response for non-existent slug

**Business logic verified:**
- Non-existent slug returns 404 status
- No error raised, proper HTTP response

### TestCharacterTechnicalInfo

Tests for technical-info custom action with authorization.

**Expected response fields (authenticated staff/superuser only):**

| Field | Type | Purpose |
|---|---|---|
| `id` | Integer | Database primary key |
| `comicvine_id` | Integer | ComicVine API ID |
| `comicvine_status` | String | Sync status display value |
| `comicvine_last_match` | DateTime | Last sync timestamp (ISO format) |
| `created_dt` | DateTime | Creation timestamp (ISO format) |
| `modified_dt` | DateTime | Last modification timestamp (ISO format) |

#### test_no_auth

**Endpoint:** `GET /api/characters/{slug}/technical-info/`

**Fixtures used:** `api_client`, `character_no_issues`

**Purpose:** Verify unauthenticated access denied

**Business logic verified:**
- Unauthenticated requests return 401
- Authentication required for technical info

#### test_regular_user

**Endpoint:** `GET /api/characters/{slug}/technical-info/`

**Fixtures used:** `authenticated_api_client`, `character_no_issues`

**Purpose:** Verify regular user access denied

**Business logic verified:**
- Authenticated non-staff users return 403
- Staff permission required for technical info

#### test_staff

**Endpoint:** `GET /api/characters/{slug}/technical-info/`

**Fixtures used:** `staff_api_client`, `character_no_issues`

**Purpose:** Verify staff access granted

**Business logic verified:**
- Staff users can access technical info
- Returns 200 status

#### test_superuser

**Endpoint:** `GET /api/characters/{slug}/technical-info/`

**Fixtures used:** `superuser_api_client`, `character_no_issues`

**Purpose:** Verify superuser access and response data

**Business logic verified:**
- Superuser can access technical info
- All technical fields present (id, comicvine_id, comicvine_status, timestamps)
- ComicVine status converted to display value
- Timestamps localized and formatted as ISO strings
- Requires Python 3.12+ (test skipped on older versions)

### TestCharactersParametrized

Parametrized tests to reduce code duplication for ordering operations.

#### test_ordering_parametrized

**Endpoint:** `GET /api/characters/?ordering={field}`

**Fixtures used:** `api_client`, `characters_with_issues`

**Purpose:** Test all ordering fields in both directions using parametrization

**Parameters tested:**

| Parameter | Direction | Field Type |
|---|---|---|
| `name` | Ascending | String field |
| `-name` | Descending | String field |
| `issues_count` | Ascending | Annotated count |
| `-issues_count` | Descending | Annotated count |
| `volumes_count` | Ascending | Aggregated count |
| `-volumes_count` | Descending | Aggregated count |

**Business logic verified:**
- All ordering fields work in both directions
- Values sorted correctly based on field type
- Parametrization reduces test duplication

### TestCharactersEdgeCases

Edge case and boundary condition tests for robust API behavior.

#### test_pagination_boundary_first_page

**Endpoint:** `GET /api/characters/?page=1`

**Fixtures used:** `api_client`, `characters_with_issues`

**Purpose:** Verify first page returns valid results

**Business logic verified:**
- Page 1 accessible and valid
- Response includes results key

#### test_pagination_boundary_zero_page

**Endpoint:** `GET /api/characters/?page=0`

**Fixtures used:** `api_client`

**Purpose:** Verify page 0 rejected

**Business logic verified:**
- Page 0 returns 404
- Pagination starts at 1

#### test_pagination_boundary_negative_page

**Endpoint:** `GET /api/characters/?page=-1`

**Fixtures used:** `api_client`

**Purpose:** Verify negative page rejected

**Business logic verified:**
- Negative page returns 404
- Pagination validates positive integers

#### test_list_with_large_page_size

**Endpoint:** `GET /api/characters/?page_size=10000`

**Fixtures used:** `api_client`, `characters_with_issues`

**Purpose:** Verify large page_size handled gracefully

**Business logic verified:**
- Large page_size returns all results
- No server error or timeout
- Count matches fixture length

#### test_list_with_zero_page_size

**Endpoint:** `GET /api/characters/?page_size=0`

**Fixtures used:** `api_client`

**Purpose:** Verify zero page_size handled

**Business logic verified:**
- Zero page_size returns 200, 400, or 404
- Server handles edge case without error

#### test_response_structure_includes_all_pagination_fields

**Endpoint:** `GET /api/characters/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify pagination response structure

**Business logic verified:**
- Response includes count, next, previous, results fields
- Pagination metadata always present

#### test_list_response_structure_validation

**Endpoint:** `GET /api/characters/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify response data types

**Business logic verified:**
- count is integer
- results is list
- results items are dictionaries

### TestCharactersConsistency

Tests verifying data consistency across different endpoints.

#### test_list_detail_field_consistency

**Endpoint:** `GET /api/characters/` and `GET /api/characters/{slug}/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify list fields subset of detail fields

**Business logic verified:**
- All fields in list response exist in detail response
- Detail endpoint is superset of list endpoint
- No orphaned fields in list serializer

#### test_list_detail_value_consistency

**Endpoint:** `GET /api/characters/` and `GET /api/characters/{slug}/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify shared field values match between list and detail

**Business logic verified:**
- Slug, name, short_description match between endpoints
- Same serialization logic for common fields

#### test_count_vs_list_count_consistency

**Endpoint:** `GET /api/characters/` and `GET /api/characters/count/`

**Fixtures used:** `api_client`, `characters_with_issues`, `characters_no_issues`

**Purpose:** Verify count endpoint matches list count

**Business logic verified:**
- Count endpoint returns same count as list endpoint
- Filtering applied consistently

#### test_count_vs_list_with_show_all_consistency

**Endpoint:** `GET /api/characters/?show-all=yes` and `GET /api/characters/count/?show-all=yes`

**Fixtures used:** `api_client`, `characters_with_issues`, `characters_no_issues`

**Purpose:** Verify show-all filter consistency

**Business logic verified:**
- Show-all filter applied identically to both endpoints
- Count matches list count with filter

#### test_detail_response_has_all_expected_fields

**Endpoint:** `GET /api/characters/{slug}/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify detail response completeness

**Business logic verified:**
- Detail response includes minimum expected fields
- Core fields always present (slug, name, real_name, birth, gender, descriptions, download info)

### TestCharactersHTTPMethods

Tests verifying read-only endpoint restrictions.

#### test_list_endpoint_rejects_post

**Endpoint:** `POST /api/characters/`

**Fixtures used:** `api_client`

**Purpose:** Verify POST not allowed on list

**Business logic verified:**
- POST returns 405, 403, or 400
- List endpoint read-only

#### test_list_endpoint_rejects_put

**Endpoint:** `PUT /api/characters/`

**Fixtures used:** `api_client`

**Purpose:** Verify PUT not allowed on list

**Business logic verified:**
- PUT returns 405, 403, or 400
- List endpoint read-only

#### test_list_endpoint_rejects_patch

**Endpoint:** `PATCH /api/characters/`

**Fixtures used:** `api_client`

**Purpose:** Verify PATCH not allowed on list

**Business logic verified:**
- PATCH returns 405, 403, or 400
- List endpoint read-only

#### test_list_endpoint_rejects_delete

**Endpoint:** `DELETE /api/characters/`

**Fixtures used:** `api_client`

**Purpose:** Verify DELETE not allowed on list

**Business logic verified:**
- DELETE returns 405, 403, or 400
- List endpoint read-only

#### test_detail_endpoint_rejects_post

**Endpoint:** `POST /api/characters/{slug}/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify POST not allowed on detail

**Business logic verified:**
- POST returns 405, 403, or 400
- Detail endpoint read-only

#### test_detail_endpoint_rejects_put

**Endpoint:** `PUT /api/characters/{slug}/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify PUT not allowed on detail

**Business logic verified:**
- PUT returns 405, 403, or 400
- Detail endpoint read-only

#### test_detail_endpoint_rejects_patch

**Endpoint:** `PATCH /api/characters/{slug}/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify PATCH not allowed on detail

**Business logic verified:**
- PATCH returns 405, 403, or 400
- Detail endpoint read-only

#### test_detail_endpoint_rejects_delete

**Endpoint:** `DELETE /api/characters/{slug}/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify DELETE not allowed on detail

**Business logic verified:**
- DELETE returns 405, 403, or 400
- Detail endpoint read-only

#### test_count_endpoint_rejects_post

**Endpoint:** `POST /api/characters/count/`

**Fixtures used:** `api_client`

**Purpose:** Verify POST not allowed on count

**Business logic verified:**
- POST returns 405, 403, or 400
- Count endpoint read-only

#### test_response_content_type_is_json

**Endpoint:** `GET /api/characters/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify JSON content type

**Business logic verified:**
- Response Content-Type header includes application/json
- API returns JSON format

### TestCharactersCrossEndpoint

Integration tests across multiple endpoints for workflow validation.

#### test_list_returns_correct_total_count

**Endpoint:** `GET /api/characters/`

**Fixtures used:** `api_client`, `characters_with_issues`, `characters_no_issues`

**Purpose:** Verify list count matches filter criteria

**Business logic verified:**
- Default list shows only characters with issues
- Count field accurate

#### test_detail_slug_lookup_matches_list_slug

**Endpoint:** `GET /api/characters/` and `GET /api/characters/{slug}/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify slug from list works in detail

**Business logic verified:**
- Slug from list response can be used for detail lookup
- Slug consistency across endpoints

#### test_filtering_consistency_across_endpoints

**Endpoint:** `GET /api/characters/` and `GET /api/characters/count/`

**Fixtures used:** `api_client`, `characters_with_issues`, `characters_no_issues`

**Purpose:** Verify filtering behavior consistent across list and count

**Business logic verified:**
- Default filter applied identically
- Show-all filter applied identically
- List and count use same queryset logic

#### test_pagination_structure_consistent

**Endpoint:** `GET /api/characters/`

**Fixtures used:** `api_client`, `character_with_issues`

**Purpose:** Verify pagination structure always present

**Business logic verified:**
- Count field always present and not null
- Next/previous fields present (nullable)
- Results field is list

## Running Tests

From repository root:

```bash
# Run all E2E tests
docker-compose -f local.yml run --rm backend pytest read_comics/characters/tests/test_e2e.py

# Run specific test class
docker-compose -f local.yml run --rm backend pytest read_comics/characters/tests/test_e2e.py::TestCharactersList

# Run specific test method
docker-compose -f local.yml run --rm backend pytest read_comics/characters/tests/test_e2e.py::TestCharactersList::test_ordering_by_name_ascending

# Run with verbose output
docker-compose -f local.yml run --rm backend pytest read_comics/characters/tests/test_e2e.py -v
```

## Related Components

- **ViewSet:** [`CharacterViewSet`](../api/viewsets.md#characterviewset)
- **Serializers:** [`CharactersListSerializer`](../api/serializers.md#characterslistserializer), [`CharacterDetailSerializer`](../api/serializers.md#characterdetailserializer)
- **Model:** [`Character`](../models.md#character)
- **Endpoints:** [Character API Endpoints](../api/endpoints.md)
- **Fixtures:** [Character Fixtures](fixtures.md)