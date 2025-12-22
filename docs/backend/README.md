# Backend (Django)

A brief guide to the server side of the Read Comics project.

## Pages
- [Architecture and directory structure](architecture.md)
- [Tests, type checks, and background workflow](workflow.md)

## Applications
- [Characters](characters/README.md)
- [Concepts](concepts/README.md)
- [Core](core/README.md)
- [Issues](issues/README.md)
- [Locations](locations/README.md)
- [Missing Issues](missing_issues/README.md)
- [Objects](objects/README.md)
- [People](people/README.md)
- [Powers](powers/README.md)
- [Publishers](publishers/README.md)
- [Search](search/README.md)
- [Story Arcs](story_arcs/README.md)
- [Teams](teams/README.md)
- [Utils](utils/README.md)
- [Spiders](spiders/README.md)
- [Users](users/README.md)
- [Volumes](volumes/README.md)

## Keeping app docs accurate
- Run `python scripts/check_backend_docs.py` after adding or removing Django apps to ensure each backend module has a companion README under `docs/backend/<app>/README.md`.
- When you mention a documented app or helper, add a link to the corresponding doc so readers can jump to the full description.
- Tip: before adding text about an existing concept (models, managers, workflows), search the `docs/` tree and drop the relative link (`[Concept](concepts/README.md)` style) instead of rephrasing long explanations.
