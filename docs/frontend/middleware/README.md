# Middleware

Nuxt route middleware.

## Documentation

- [auth.global.md](auth.global.md) — Authentication guard middleware

## Overview

Middleware runs before route navigation. Global middleware (`.global.ts` suffix) runs on every route.

| Middleware | Type | Description |
|------------|------|-------------|
| `auth.global` | Global | Protects routes requiring authentication |