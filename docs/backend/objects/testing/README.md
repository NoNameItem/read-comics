# Objects Testing Documentation

## Overview

This directory contains comprehensive testing documentation for the Objects app. The Objects app tests cover factories for creating test data, fixtures for test setup, URL routing tests, and end-to-end API integration tests.

## Documentation Files

- **[factories.md](factories.md)** - Object factory documentation with parameters and post-generation hooks
- **[fixtures.md](fixtures.md)** - Object fixture documentation with scope and dependencies
- **[test_drf_urls.md](test_drf_urls.md)** - URL routing tests for objects API endpoints
- **[test_e2e.md](test_e2e.md)** - End-to-end API tests covering list, detail, count, and technical-info endpoints

## Testing Scope

The Objects app testing suite provides:

1. **ObjectFactory** - Factory class for generating Object instances with configurable relationships
2. **Fixtures** - Fixtures for creating objects with and without issues in both single and batch modes
3. **URL Tests** - Tests verifying URL routing and reverse resolution for all objects endpoints
4. **E2E Tests** - End-to-end tests covering complete API workflows

## Running Tests

From repository root:

```bash
# Run all objects tests
docker-compose -f local.yml run --rm backend pytest read_comics/objects/tests/

# Run specific test file
docker-compose -f local.yml run --rm backend pytest read_comics/objects/tests/test_e2e.py

# Run with coverage
docker-compose -f local.yml run --rm backend coverage run -m pytest read_comics/objects/tests/
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
- Detail endpoint with various objects states
- Technical info endpoint with authentication and authorization
- Parametrized ordering tests
- Edge case and boundary condition tests
- Consistency tests across endpoints
- HTTP method validation for read-only endpoints

## Related Documentation

- [Object Models](../models.md#objects)
- [Object API Viewsets](../api/viewsets.md#objectsviewset)
- [Object API Serializers](../api/serializers.md)
- [Object Endpoints](../api/endpoints.md)
