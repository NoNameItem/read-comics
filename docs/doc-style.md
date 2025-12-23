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

1. **ALWAYS follow this doc-style.md guide** — Apply all rules in Sections "Standard structure", "Detailed checklist", "Endpoint documentation", "Content guidelines", and "Anchors & linking" without exception.

2. **Structure requirement:**
   - Use `# Title` → `## Summary` → `## Reference` (or `## <Section>`) → `### Class/Function` → `#### Details`
   - Always include Summary section with one-line bullets
   - Always include Reference section with detailed information

3. **Endpoint documentation ONLY in endpoints.md:**
   - DO NOT describe endpoints in viewsets.md — that's reserved for viewset configuration only
   - Endpoint examples, request/response, URL patterns → endpoints.md ONLY
   - Viewsets.md → configuration, mixins, serializers, queryset only

4. **Always add Docs comments:**
   - Every Python module with documentation must have `# Docs: [[docs/path/to_file.md]]` at the top
   - Update module comment if documentation file path changes

5. **Before starting documentation:**
   - Read this doc-style.md file to ensure compliance
   - Check adjacent docs for terminology consistency
   - Use relative links for cross-references

6. **Do NOT include full function implementations in documentation:**
   - Document method signatures, parameters, return values, and behavior
   - DO NOT paste entire function code
   - Show only small config snippets (1-3 lines) or brief call examples when needed
   - Focus on WHAT a function does, not HOW it's implemented in detail

**This rule applies across all sessions. Do not skip or abbreviate these requirements.**
