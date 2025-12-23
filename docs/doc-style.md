# Documentation Style Guide

This single reference merges every existing checklist so all contributors document backend classes, tasks, helpers, views, commands, and API surfaces in a consistent format.

## Scope
- Applies to every module, class, task, function, helper, or view description living anywhere under `docs/`.
- Treat each file as reference material rather than prose; keep statements factual, objective, and tied directly to implementation details.

## Standard structure
1. Start with `# <Topic> in `path/to/module.py`` where `<Topic>` names the primary class/task/function documented and `path/to/module.py` is the relative import path.
2. Add `## Summary` with one-sentence bullet per major entity (model, task, view, helper, endpoint, etc.) linking to anchors (e.g., `[#classname]`).
3. Follow with `## Reference` or `## <Section>` and use `###` headings for each class/callable plus `####` subheadings such as "Class attributes", "Fields", "Behavior", "Usage", "Parameters", "Returns", "Routing", etc.
4. Conclude with operational sections where applicable (`Task routing`, `Configuration`, `Common usage patterns`, `Endpoint catalog`) so readers can easily find runtime guidance.

## Detailed checklist
1. Include a dedicated heading for every documented class or function (e.g., `## ClassName`).
2. Provide summary bullets describing purpose, context, and relationships to other system parts.
3. List all attributes and properties with a concise one-line note on their type/role when the entity exposes fields.
4. Describe every method as an individual bullet; include sub-bullets for each parameter and explain return values or side effects inline (see example below).
   - Example:
     - `method(self, arg)` — short summary.
       - `arg`: explanation.
5. When a file documents multiple helpers, include a `## Reference` section so each entry appears together.
6. At the top of the file (or inside the summary section), enumerate every documented class or function with links to the detailed entries (e.g., `[ClassName](#classname)`).
7. Before introducing a concept, search the existing docs and insert relative links to other explanations so readers can jump elsewhere.
8. Document every top-level class or function defined in the module. Private helpers (names starting with `_`) belong in the detailed descriptions but are excluded from the summary listing.
9. When referencing other documented concepts (models, mixins, commands, workflows), use relative links rather than repeating explanations.
10. Add a `# Docs: [[docs/path/to_page.md]]` comment at the top of the associated Python module so code and documentation remain explicitly linked across sessions.
    - **Multiple docs rule**: If a Python file has multiple documentation files, use **separate comments for each link**, one per line:
      ```python
      # Docs: [[docs/backend/app/models.md]]
      # Docs: [[docs/backend/app/tasks.md]]
      # Docs: [[docs/backend/app/search_adapters.md]]
      ```
    - Do NOT combine multiple links in a single comment: `# Docs: [[...]], [[...]]` ❌
11. Write all documentation content in English and audit any existing non-English pages before adding new content.
12. For DRF endpoints, create `docs/backend/<app>/endpoints.md` that captures the request/response schema, URL, viewset/action, query/request parameters, and concrete examples; mention that doc in the `# Docs: [[...]]` comment on the corresponding views/viewsets file.

## Django Model Documentation

When documenting Django models in `models.md` files:

1. **Field separation is MANDATORY** — Models must explicitly separate inherited fields from custom fields:
   - Create a section **"Inherited Fields from [ParentClass]"** listing all fields inherited from parent classes (e.g., `AbstractUser`, `ComicvineSyncModel`, etc.)
   - Create a section **"Custom Fields (defined in [ModelName] model)"** listing only fields defined directly in the documented model
   - If a model extends multiple base classes with fields, create separate subsections for each parent class
   - Use a table format with `Field Name | Type | Null | Blank | Default | Purpose` columns for clarity

2. **Parent class acknowledgement:**
   - Always mention the parent class at the top of the model section (e.g., `Extends: AbstractUser`, `Extends: ComicvineSyncModel`)
   - Document special behaviors inherited from parent (e.g., auto_now, auto_now_add, signal handlers)

3. **Example structure:**
   ```markdown
   ### ModelName

   Extends: [`ParentClassName`](../path/to/parent.md#parentclassname)

   **Inherited Fields from ParentClassName:**
   | Field | Type | Purpose |
   |---|---|---|
   | field1 | ... | ... |

   **Custom Fields (defined in ModelName model):**
   | Field | Type | Purpose |
   |---|---|---|
   | field2 | ... | ... |

   **Methods:**
   - method_name(...)
   ```

## Endpoint documentation

When documenting DRF REST endpoints in `docs/backend/<app>/endpoints.md`, follow this structure for each endpoint section:

1. **Brief description** (1-2 sentences) — what the endpoint does and its primary use case.
2. **ViewSet** — the viewset class powering the endpoint (e.g., [`CharacterViewSet`](viewsets.md#characterviewset)).
3. **Action** — the specific action method or mixin providing the endpoint (e.g., `list`, `retrieve`, `count` from `CountActionMixin`).
4. **Serializer** — the serializer class used for rendering responses (e.g., [`CharactersListSerializer`](serializers.md#characterslistserializer)), or `None` if plain JSON.
5. **Parameters & query params** — list allowed query parameters, path variables, and their effects.
6. **Response example** — JSON response with realistic sample data.

Link viewset, serializer, and model documentation using relative paths (e.g., `[viewsets.md#classname]`, `[serializers.md#classname]`, `[models.md#classname]`).

## Testing Documentation

When documenting tests, factories, and fixtures in `docs/backend/testing/` (global) and `docs/<app>/testing/` (app-specific), follow this structure:

### Organization

1. **Global testing documentation** (`/docs/backend/testing/`):
   - `README.md` — Overview of testing architecture, test types, running tests, common patterns
   - `factories.md` — Global factories (e.g., `ComicvineSyncModelFactory`, `UserFactory`) with parameters and usage
   - `fixtures.md` — Global fixtures (e.g., `api_client`, `authenticated_api_client`, `user`) with scope and dependencies

2. **App-specific testing documentation** (`/docs/<app>/testing/`):
   - `README.md` — Links to app-specific factory, fixture, and test documentation
   - `factories.md` — App factories (e.g., `VolumeFactory`, `IssueFactory`) with parameters, post-generation hooks, and usage
   - `fixtures.md` — App fixtures (e.g., `volume_with_issues`, `finished_volumes`) with scope, dependencies, and usage patterns
   - `test_<module>.md` — Documentation for each test file (e.g., `test_drf_urls.md` for `test_drf_urls.py`, `test_e2e.md` for `test_e2e.py`)

3. **File-to-documentation mapping:**
   - Each test file has a corresponding documentation file with the same name but `.md` extension
   - `tests/test_drf_urls.py` → `testing/test_drf_urls.md`
   - `tests/test_e2e.py` → `testing/test_e2e.md`
   - `tests/factories.py` → `testing/factories.md`
   - `tests/conftest.py` fixtures → `testing/fixtures.md`

### Factory Documentation

When documenting factory classes:

1. **Header**: Name the factory class and location (e.g., `## VolumeFactory in read_comics/volumes/tests/factories.py`)
2. **Inheritance**: Note the parent factory class and what it provides (e.g., `Extends: ComicvineSyncModelFactory`)
3. **Parameters table**: List all parameters with columns: `Field | Type | Generator | Purpose`
   - Include post-generation hooks (e.g., `add_issues`)
   - Document Faker generators used (e.g., `Faker("word")`)
   - Note LazyAttribute usage for dynamic values
4. **Batch creation**: Document `create_batch()` usage and parameter passing
5. **Post-generation hooks**: Explain what each hook does and which parameters trigger it
6. **Usage examples**: Concise examples showing common factory patterns (not full code, just parameter calls)
   - Example: `volume = VolumeFactory(name="Amazing Spider-Man", start_year=1963, add_issues=5)`
7. **Database behavior**: Document `django_get_or_create` deduplication if applicable
8. **No source code**: Do NOT include factory method implementation code

### Fixture Documentation

When documenting fixture functions:

1. **Header**: Name the fixture with function signature (e.g., `## volume_with_issues()`)
2. **Type/Returns**: What object type is returned (e.g., "Volume model instance" or "List of Volume instances")
3. **Scope**: Pytest scope if non-default (e.g., `function`, `session`)
4. **Dependencies**: List fixtures or other fixtures this depends on (e.g., `user` fixture)
5. **Parameters table**: For fixtures with parameters, list columns: `Parameter | Type | Purpose`
6. **Behavior**: What data it creates or modifies (2-3 sentences)
7. **When to use**: Describe common test scenarios where this fixture is appropriate
8. **Usage examples**: Concise examples showing how to use the fixture in tests
   - Include fixture combinations for complex scenarios
   - Example: `def test_hide_finished(volumes_with_issues, finished_volumes, authenticated_api_client):`
9. **No source code**: Do NOT include fixture implementation or setup code

### Test Documentation

When documenting test files and test classes:

1. **File header**: Name and location (e.g., `# Volumes E2E Tests in read_comics/volumes/tests/test_e2e.py`)
2. **Summary**: One-sentence description of test scope (e.g., "End-to-end API tests verifying complete workflows")
3. **Marks/decorators**: Note pytest marks used globally (e.g., `pytestmark = pytest.mark.django_db`)
4. **Test classes**: Document each test class with purpose
5. **Test methods**: For each test method, document:
   - **Endpoint**: HTTP method and URL being tested (e.g., `GET /api/volumes/`)
   - **Fixtures used**: List all fixtures injected into the test
   - **Assertions**: List what the test verifies (not how, just what)
   - **Purpose**: One-sentence statement of what behavior is being tested
   - **Business logic verified**: Bullet list of application behaviors confirmed
   - **Related components**: Link to ViewSet, Serializer, Mixin, or Model being tested (e.g., `[viewsets.md#volumesviewset]`)
6. **Test execution**: Include commands to run the test file and specific tests
7. **No source code**: Do NOT include test implementation code, assertions code, or HTTP request details
   - Exception: Query parameter format (e.g., `?hide-finished=no`) can be shown inline

### Common Testing Documentation Patterns

1. **Response structure**: For API tests, document expected response fields in a table:
   ```markdown
   | Field | Type | Purpose |
   |---|---|---|
   | count | Integer | Total count of items |
   | results | Array | List of serialized objects |
   ```

2. **Fixture combinations**: Show how to use multiple fixtures together:
   ```markdown
   def test_hide_finished(volumes_with_issues, finished_volumes, authenticated_api_client):
       # volumes_with_issues: Data that SHOULD appear
       # finished_volumes: Data that should be EXCLUDED
   ```

3. **Test patterns**: Document reusable patterns (e.g., filtering tests, authorization tests, data validation tests)

4. **Edge cases**: Document test scenarios for boundary conditions and special cases

## Content guidelines
- Use concise bullet lists; avoid speculation and keep prose factual.
- Prefer inline code formatting (`code`) for identifiers, types, routes, and settings, and link to related docs with relative hyperlinks.
- When documenting invocation, show imports and calls inside fenced ` ```python` blocks with realistic parameters.
- Under each subheading note explicit behavior details such as retry policies, database interactions, routing, and side effects.
- **Do NOT include full function/method implementations** — Document purpose, parameters, return values, side effects, and behavior instead. Show config snippets or small call examples only when essential for understanding.

## Anchors & linking
- Every summary bullet must point to an existing anchor (e.g., `- [`MyClass`](#myclass)` paired with `### MyClass`).
- Keep links relative (e.g., `../utils/helpers.md#helper`) so navigation works locally.
- Link this guide from `docs/README.md` so future contributors remember the format and the linking requirement.

## Applicability & reminders
- This template governs models, tasks, utilities, views, commands, endpoints, and any other public callable documented under `docs/`.
- Review adjacent docs before adding new entries to reuse consistent structure and terminology.
- Reference this guide whenever you add or update documentation so the format stays stable between sessions.

## For Claude Code / AI Assistant

**CRITICAL INSTRUCTION (for every documentation session):**

Whenever writing or updating documentation under `docs/backend/`:

1. **ALWAYS follow this doc-style.md guide** — Apply all rules in Sections "Standard structure", "Detailed checklist", "Endpoint documentation", "Testing Documentation", "Content guidelines", and "Anchors & linking" without exception.

2. **Structure requirement:**
   - Use `# Title` → `## Summary` → `## Reference` (or `## <Section>`) → `### Class/Function` → `#### Details`
   - Always include Summary section with one-line bullets
   - Always include Reference section with detailed information

3. **Endpoint documentation ONLY in endpoints.md:**
   - DO NOT describe endpoints in viewsets.md — that's reserved for viewset configuration only
   - Endpoint examples, request/response, URL patterns → endpoints.md ONLY
   - Viewsets.md → configuration, mixins, serializers, queryset only

4. **Testing documentation structure:**
   - Global testing docs in `/docs/backend/testing/` (README.md, factories.md, fixtures.md)
   - App-specific testing docs in `/docs/<app>/testing/` (README.md, factories.md, fixtures.md)
   - Each test file gets corresponding documentation: `test_drf_urls.py` → `test_drf_urls.md`, `test_e2e.py` → `test_e2e.md`
   - Document parameters, behavior, and usage examples — NO source code implementations
   - Include tables for parameters/fields and separate sections for each test class/method

5. **Always add Docs comments:**
   - Every Python module with documentation must have `# Docs: [[docs/path/to_file.md]]` at the top
   - Update module comment if documentation file path changes
   - For test files with multiple docs, use separate comments: `# Docs: [[...]]` then `# Docs: [[...]]` (one per line)

6. **Before starting documentation:**
   - Read this doc-style.md file to ensure compliance
   - Check adjacent docs for terminology consistency
   - Use relative links for cross-references

7. **Do NOT include full function implementations in documentation:**
   - Document method signatures, parameters, return values, and behavior
   - DO NOT paste entire function code
   - Show only small config snippets (1-3 lines) or brief call examples when needed
   - Focus on WHAT a function does, not HOW it's implemented in detail
   - For tests: show fixtures used and what's verified, NOT assertion code

**This rule applies across all sessions. Do not skip or abbreviate these requirements.**
