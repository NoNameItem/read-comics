# Missing Issues API

REST API for accessing missing issue records with count endpoint.

## Documentation

- [`endpoints.md`](endpoints.md) — REST endpoint specifications
- [`viewsets.md`](viewsets.md) — ViewSet configuration and behavior

## Key Features

- **Count Endpoint** — `/count/` for total missing issue count
- **Skip Filtering** — Only returns issues with `skip=False`
- **Entity Links** — MissingIssue records link to characters, teams, locations, and other entities