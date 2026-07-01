# Code Style

## Python
- **Black**: 120 char line length
- **isort**: trailing commas
- **flake8**: see `setup.cfg`
- **mypy**: Django/DRF plugins enabled
- **Quotes**: Double quotes (flake8-quotes)

## Frontend
- **ESLint**: @nuxt/eslint (Antfu config)
- **Prettier**: default
- **pnpm**: v10.23.0

## Commits (Conventional)

```
<type>(<scope>): <description>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`
Scopes: App names (`issues`, `spiders`, `users`, `core`)

Examples:
- `feat(issues): add variant covers support`
- `fix(spiders): handle missing image URLs`
