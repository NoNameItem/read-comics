# Concepts Testing Documentation

## Overview

This directory contains comprehensive testing documentation for the Concepts app. The Concepts app tests cover factories for creating test data, fixtures for test setup, URL routing tests, and end-to-end API integration tests.

## Documentation Files

- **[factories.md](factories.md)** - Concept factory documentation with parameters and post-generation hooks
- **[fixtures.md](fixtures.md)** - Concept fixture documentation with scope and dependencies
- **[test_drf_urls.md](test_drf_urls.md)** - URL routing tests for concept API endpoints
- **[test_e2e.md](test_e2e.md)** - End-to-end API tests covering list, detail, count, and technical-info endpoints

## Testing Scope

The Concepts app testing suite provides:

1. **ConceptFactory** - Factory class for generating Concept instances with configurable relationships
2. **Fixtures** - Four fixtures for creating concepts with and without issues in both single and batch modes
3. **URL Tests** - Four tests verifying URL routing and reverse resolution for all concept endpoints
4. **E2E Tests** - Six test classes with 35+ test methods covering complete API workflows

## Running Tests

From repository root:

```bash
# Run all concept tests
docker-compose -f local.yml run --rm backend pytest read_comics/concepts/tests/

# Run specific test file
docker-compose -f local.yml run --rm backend pytest read_comics/concepts/tests/test_e2e.py

# Run with coverage
docker-compose -f local.yml run --rm backend coverage run -m pytest read_comics/concepts/tests/
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
- Detail endpoint with various concept states
- Technical info endpoint with authentication and authorization
- Parametrized ordering tests for code reduction
- Edge case and boundary condition tests
- Consistency tests across endpoints
- HTTP method validation for read-only endpoints

## Related Documentation

- [Concept Models](../models.md#concept)
- [Concept API Viewsets](../api/viewsets.md#conceptviewset)
- [Concept API Serializers](../api/serializers.md)
- [Concept Endpoints](../api/endpoints.md)