# Documentation Guidelines

**CRITICAL: Follow `docs/doc-style.md` for all documentation**

## Structure
`# Title` → `## Summary` → `## Reference` → `### Class` → `#### Details`

## Rules
1. Summary section: one-line bullets with anchor links
2. Endpoints ONLY in `endpoints.md` (not viewsets.md)
3. Python modules need `# Docs: [[docs/path/to_file.md]]` comment
4. Use relative links: `[viewsets.md#class]`, `../models.md#field`
5. English only

## Token Savings Strategy

Read docs instead of source code:
1. `docs/backend/<app>/README.md` → overview
2. `models.md` → schema, relationships
3. `api/serializers.md` → response structures
4. `api/viewsets.md` → API configuration
5. Source code → only for implementation details

Savings: 50-70% tokens vs reading source files directly.

## For New Modules
- Comprehensive enough to replace 80% of source code reading
- Include all field names, types, relationships
- Document signatures and behavior (not implementation)
