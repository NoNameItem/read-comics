# People Testing Documentation

## Overview

This directory contains comprehensive testing documentation for the People app. The People app tests cover factories for creating test data, fixtures for test setup, URL routing tests, and end-to-end API integration tests.

## Documentation Files

- **[factories.md](factories.md)** - Person factory documentation with parameters and post-generation hooks
- **[fixtures.md](fixtures.md)** - Person fixture documentation with scope and dependencies
- **[test_drf_urls.md](test_drf_urls.md)** - URL routing tests for people API endpoints
- **[test_e2e.md](test_e2e.md)** - End-to-end API tests covering list, detail, count, and technical-info endpoints

## Testing Scope

The People app testing suite provides:

1. **PersonFactory** - Factory class for generating Person instances with configurable relationships
2. **Fixtures** - Fixtures for creating people with and without issues in both single and batch modes
3. **URL Tests** - Tests verifying URL routing and reverse resolution for all people endpoints
4. **E2E Tests** - End-to-end tests covering complete API workflows

## Running Tests

From repository root:

```bash
# Run all people tests
docker-compose -f local.yml run --rm backend pytest read_comics/people/tests/

# Run specific test file
docker-compose -f local.yml run --rm backend pytest read_comics/people/tests/test_e2e.py

# Run with coverage
docker-compose -f local.yml run --rm backend coverage run -m pytest read_comics/people/tests/
docker-compose -f local.yml run --rm backend coverage html
```

## Test Structure

**URL Tests** (`test_drf_urls.py`):
- List endpoint routing
- Detail endpoint routing
- Technical info endpoint routing
- Count endpoint routing

**E2E Tests** (`test_e2e.py`):
- Count endpoint behavior with filtering
- List endpoint with pagination, filtering, and ordering
- Detail endpoint with various people states
- Technical info endpoint with authentication and authorization
- Parametrized ordering tests
- Edge case and boundary condition tests
- Consistency tests across endpoints
- HTTP method validation for read-only endpoints

## Related Documentation

- [Person Models](../models.md#people)
- [Person API Viewsets](../api/viewsets.md#peopleviewset)
- [Person API Serializers](../api/serializers.md)
- [Person Endpoints](../api/endpoints.md)
