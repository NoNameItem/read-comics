# Concepts

Manages abstract concepts, themes, and ideas that appear in comic books. Concepts can be various abstract ideas like "magic", "time travel", "artificial intelligence", etc.

## Documentation

### Core

- [**models.md**](models.md) — Concept model with ComicVine sync, aliases, images, first appearances, watchers

### API

- [**api/endpoints.md**](api/endpoints.md) — List, detail, count, technical-info endpoints
- [**api/serializers.md**](api/serializers.md) — ConceptsListSerializer, ConceptDetailSerializer, ConceptTechnicalInfoSerializer
- [**api/viewsets.md**](api/viewsets.md) — ConceptViewSet configuration, mixins, queryset filtering

### Features

- [**search_adapters.md**](search_adapters.md) — Full-text search integration with django-watson
- [**tasks.md**](tasks.md) — Celery tasks for ComicVine syncing and batch updates

## Key Modules

- `models.py` — Concept model with ComicVine API integration
- `api/serializers.py` — Three serializers for different endpoints
- `api/viewsets.py` — Read-only ViewSet with aggregated counts and filtering
- `search_adapters.py` — django-watson search integration
- `tasks.py` — Celery tasks for syncing and refreshing concept data
- `tests/test_e2e.py` — E2E API tests
