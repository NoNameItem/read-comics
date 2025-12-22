# Documentation Style Guide

When adding new classes or functions under `docs/`, follow this checklist so the reference material stays consistent and linked:

1. **Section heading** naming the class or function (e.g., `## ClassName`).
2. **Description bullets** summarizing purpose, context, and relationships to the rest of the app.
3. **Attributes & properties** (if any): list exposed fields with a one-line note on their type/role.
4. **Methods**: describe each method on its own bullet, then add sub-bullets for every parameter.
   - Example:
     - `method(self, arg)` — short summary.
       - `arg`: explanation.
5. Always add a **Reference** section when a file documents multiple helpers so all entries appear together, including top-level functions.
6. At the top of the file (or in the summary section), provide a short listing of every documented class/function with a link (e.g., `[ClassName](#classname)` or `[function_name](#function_name)`) to the specific entry inside the Reference section.
7. **Link hygiene**: before introducing a new class or helper, search the existing documentation for the concept and add relative links wherever it is mentioned elsewhere, ensuring readers can jump between pages.
8. **Document public APIs only**: describe every top-level class or function defined in the file unless its name starts with an underscore (private helper); exclude private modules or functions from the summary and Reference section.
9. If you mention other documented concepts (models, managers, mixins, workflows), link to their pages rather than repeating the same explanation.
10. Whenever you add a new backend documentation page, update the corresponding Python module with a top-of-file `# Docs: [[...]]` comment pointing to the doc path so the code and docs stay explicitly linked across sessions.
11. All documentation content must be written in English; review existing docs written in another language before starting a new page.
12. When documenting DRF endpoints, create `docs/backend/<app>/endpoints.md` capturing the URL, viewset/action, relevant `GET` query parameters, request schema for write operations, response schema, and concrete request/response examples; mention that file in `# Docs: [[...]]` comments at the top of the associated views/viewsets.

Include this guide (linked from `docs/README.md`) so future contributors reuse the format and remember to add the linking step.
