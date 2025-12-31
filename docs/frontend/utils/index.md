# Utils in `frontend/app/utils/index.ts`

Random number and array utility functions.

## Summary

- [`randomInt`](#randomint) — generate random integer in range
- [`randomFrom`](#randomfrom) — pick random element from array

## Reference

### randomInt

Generates a random integer between min and max (inclusive).

- **Parameters:**
  - `min`: `number` — minimum value (inclusive)
  - `max`: `number` — maximum value (inclusive)
- **Returns:** `number` — random integer in range [min, max]

**Example:**
```typescript
const roll = randomInt(1, 6) // 1-6
```

### randomFrom

Picks a random element from an array.

- **Type Parameter:** `T` — array element type
- **Parameters:**
  - `array`: `T[]` — source array
- **Returns:** `T` — random element from array

**Example:**
```typescript
const colors = ['red', 'green', 'blue']
const color = randomFrom(colors) // 'red', 'green', or 'blue'
```