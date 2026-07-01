# Characters

Stores character profiles, relationships, images, and search integration.

## Key modules
- [`models.py`](models.md) defines the [`Character`](models.md#character) model with ComicVine synchronization, relationships (friends/enemies, teams), and download support.
- [`tasks.py`](tasks.md) provides Celery tasks for character synchronization ([`CharacterComicvineInfoTask`](tasks.md#charactercomicvineinfotask)), batch refresh ([`CharactersRefreshTask`](tasks.md#charactersrefreshtask)), and spider crawls ([`characters_update`](tasks.md#characters_update), [`characters_increment_update`](tasks.md#characters_increment_update)).
- [`search_adapters.py`](search_adapters.md) provides [`CharacterSearchAdapter`](search_adapters.md#charactersearchadapter) for full-text search indexing and result presentation.
- `api/`:
  - [`serializers.py`](api/serializers.md) defines [`CharactersListSerializer`](api/serializers.md#characterslistserializer), [`CharacterDetailSerializer`](api/serializers.md#characterdetailserializer), and [`CharacterTechnicalInfoSerializer`](api/serializers.md#charactertechnicalinfoserializer) for JSON responses.
  - [`viewsets.py`](api/viewsets.md) provides [`CharacterViewSet`](api/viewsets.md#characterviewset) for `/api/characters/` REST endpoints with filtering, ordering, and aggregation.
  - [`endpoints.md`](api/endpoints.md) documents the REST API routes and response formats.
- `templates/` and `views.py` render character cards and reference lists.

