# Pages

File-based routing pages.

## Documentation

- [index.md](index.md) — Home page
- [users/login.md](users/login.md) — Login page
- [users/register.md](users/register.md) — Registration page

## Overview

Pages map to routes via file structure:
- `pages/index.vue` → `/`
- `pages/users/login.vue` → `/users/login`
- `pages/users/register.vue` → `/users/register`

## Route Table

| Path | Page | Layout | Auth |
|------|------|--------|------|
| `/` | index.vue | default | No |
| `/users/login` | users/login.vue | blank | No |
| `/users/register` | users/register.vue | blank | No |