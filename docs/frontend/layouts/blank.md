# Blank Layout in `frontend/app/layouts/blank.vue`

Minimal layout for authentication pages.

## Summary

- [Structure](#structure) — layout organization
- [Usage](#usage) — when to use

## Reference

### Structure

```
UPageSection
└── <slot /> (page content)
```

Simple wrapper using `UPageSection` without navigation or sidebar.

## Usage

Set in page meta for auth pages:

```typescript
definePageMeta({
  layout: 'blank'
})
```

### Pages Using This Layout

- [`/users/login`](../pages/users/login.md)
- [`/users/register`](../pages/users/register.md)

## Related

- [`default` layout](default.md) — main layout with sidebar