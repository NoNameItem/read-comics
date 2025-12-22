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
11. Write all documentation content in English and audit any existing non-English pages before adding new content.
12. For DRF endpoints, create `docs/backend/<app>/endpoints.md` that captures the request/response schema, URL, viewset/action, query/request parameters, and concrete examples; mention that doc in the `# Docs: [[...]]` comment on the corresponding views/viewsets file.

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

## Anchors & linking
- Every summary bullet must point to an existing anchor (e.g., `- [`MyClass`](#myclass)` paired with `### MyClass`).
- Keep links relative (e.g., `../utils/helpers.md#helper`) so navigation works locally.
- Link this guide from `docs/README.md` so future contributors remember the format and the linking requirement.

## Applicability & reminders
- This template governs models, tasks, utilities, views, commands, endpoints, and any other public callable documented under `docs/`.
- Review adjacent docs before adding new entries to reuse consistent structure and terminology.
- Reference this guide whenever you add or update documentation so the format stays stable between sessions.
