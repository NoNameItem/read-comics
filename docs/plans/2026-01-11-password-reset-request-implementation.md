# Password Reset Request Page Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a password reset request page that allows users to request a password reset email.

**Architecture:** Vue SFC with two states (form → success) managed by a reactive boolean. Uses existing `UAuthForm` for initial state, custom template for success state with resend countdown timer.

**Tech Stack:** Vue 3, Nuxt UI (UPageCard, UAuthForm, UButton, UAlert, UIcon), Zod validation, Axios

---

## Task 1: Create forgot-password.vue page with form state

**Files:**
- Create: `frontend/app/pages/users/forgot-password.vue`

**Step 1: Create the page file with form state only**

```vue
<!-- Docs: [[docs/frontend/pages/users/forgot-password.md]] -->
<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent, AuthFormField } from '@nuxt/ui'

definePageMeta({
  layout: 'blank'
})

const axios = useAxios()

const loading = ref(false)
const formError = ref<string | null>(null)
const emailSent = ref(false)
const submittedEmail = ref('')

const fields: AuthFormField[] = [
  {
    name: 'email',
    type: 'email',
    label: 'Email',
    placeholder: 'Enter your email',
    required: true
  }
]

const schema = z.object({
  email: z.string().trim().min(1, 'Email is required').email('Invalid email address')
})

type Schema = z.output<typeof schema>

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  loading.value = true
  formError.value = null

  try {
    await axios.post('/auth/password/reset/', { email: payload.data.email })
    submittedEmail.value = payload.data.email
    emailSent.value = true
  } catch (error: unknown) {
    const axiosError = error as { response?: { status?: number; data?: { detail?: string } } }
    if (axiosError?.response?.status === 429) {
      formError.value = axiosError.response.data?.detail || 'Too many requests. Please try again later.'
    } else if (axiosError?.response?.status === 400) {
      // Don't reveal if email exists - show success anyway
      submittedEmail.value = payload.data.email
      emailSent.value = true
    } else {
      formError.value = 'Network error. Please try again later.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-4 p-4">
    <UPageCard class="w-full max-w-md">
      <UAuthForm
        :schema="schema"
        :fields="fields"
        :loading="loading"
        title="Forgot your password?"
        icon="i-lucide-key-round"
        submit-label="Send reset link"
        @submit="onSubmit"
      >
        <template #description>
          Remember your password?
          <ULink to="/users/login" class="text-primary font-medium">Log in</ULink>.
        </template>
        <template #validation>
          <UAlert v-if="formError" color="error" icon="i-lucide-circle-alert" :title="formError" />
        </template>
      </UAuthForm>
    </UPageCard>
  </div>
</template>
```

**Step 2: Verify the page renders**

Run: `cd frontend && pnpm dev`
Navigate to: `http://localhost:3000/users/forgot-password`
Expected: Form with email field, "Send reset link" button, and "Log in" link visible

**Step 3: Commit**

```bash
git add frontend/app/pages/users/forgot-password.vue
git commit -m "feat(frontend): add password reset request page with form state

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 2: Add success state with resend countdown

**Files:**
- Modify: `frontend/app/pages/users/forgot-password.vue`

**Step 1: Add resend countdown logic**

Add after the `submittedEmail` ref:

```typescript
const resendCooldown = ref(0)
let cooldownInterval: ReturnType<typeof setInterval> | null = null

function startCooldown() {
  resendCooldown.value = 60
  if (cooldownInterval) clearInterval(cooldownInterval)
  cooldownInterval = setInterval(() => {
    resendCooldown.value--
    if (resendCooldown.value <= 0 && cooldownInterval) {
      clearInterval(cooldownInterval)
      cooldownInterval = null
    }
  }, 1000)
}

onUnmounted(() => {
  if (cooldownInterval) clearInterval(cooldownInterval)
})
```

**Step 2: Update onSubmit to start cooldown on success**

Add `startCooldown()` after setting `emailSent.value = true` (in both success branches):

```typescript
submittedEmail.value = payload.data.email
emailSent.value = true
startCooldown()
```

**Step 3: Add resend function**

Add after `onSubmit`:

```typescript
async function onResend() {
  loading.value = true
  formError.value = null

  try {
    await axios.post('/auth/password/reset/', { email: submittedEmail.value })
    startCooldown()
  } catch (error: unknown) {
    const axiosError = error as { response?: { status?: number; data?: { detail?: string } } }
    if (axiosError?.response?.status === 429) {
      formError.value = axiosError.response.data?.detail || 'Too many requests. Please try again later.'
    } else {
      formError.value = 'Network error. Please try again later.'
    }
  } finally {
    loading.value = false
  }
}
```

**Step 4: Add success state template**

Replace the entire `<template>` section:

```vue
<template>
  <div class="flex flex-col items-center justify-center gap-4 p-4">
    <UPageCard class="w-full max-w-md">
      <!-- Success State -->
      <div v-if="emailSent" class="space-y-6">
        <div class="flex flex-col items-center text-center">
          <UIcon name="i-lucide-mail-check" class="size-8 mb-2 text-primary" />
          <h1 class="text-xl font-semibold text-highlighted">Check your email</h1>
          <p class="mt-1 text-base text-muted">
            We sent a password reset link to <strong>{{ submittedEmail }}</strong>
          </p>
        </div>

        <UAlert v-if="formError" color="error" icon="i-lucide-circle-alert" :title="formError" />

        <UButton
          block
          :loading="loading"
          :disabled="resendCooldown > 0"
          @click="onResend"
        >
          <template v-if="resendCooldown > 0">Resend in {{ resendCooldown }}s</template>
          <template v-else>Resend email</template>
        </UButton>

        <p class="text-sm text-center text-muted">
          <ULink to="/users/login" class="text-primary font-medium">Back to login</ULink>
        </p>
      </div>

      <!-- Form State -->
      <UAuthForm
        v-else
        :schema="schema"
        :fields="fields"
        :loading="loading"
        title="Forgot your password?"
        icon="i-lucide-key-round"
        submit-label="Send reset link"
        @submit="onSubmit"
      >
        <template #description>
          Remember your password?
          <ULink to="/users/login" class="text-primary font-medium">Log in</ULink>.
        </template>
        <template #validation>
          <UAlert v-if="formError" color="error" icon="i-lucide-circle-alert" :title="formError" />
        </template>
      </UAuthForm>
    </UPageCard>
  </div>
</template>
```

**Step 5: Verify both states work**

1. Navigate to: `http://localhost:3000/users/forgot-password`
2. Enter any email and submit
3. Expected: Success state appears with countdown timer
4. Wait for timer or verify button is disabled during cooldown

**Step 6: Commit**

```bash
git add frontend/app/pages/users/forgot-password.vue
git commit -m "feat(frontend): add success state with resend countdown to forgot-password

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 3: Update login page link

**Files:**
- Modify: `frontend/app/pages/users/login.vue:92`

**Step 1: Update the forgot password link**

Change line 92 from:

```vue
<ULink to="#" class="text-primary font-medium" tabindex="-1">Forgot password?</ULink>
```

To:

```vue
<ULink to="/users/forgot-password" class="text-primary font-medium" tabindex="-1">Forgot password?</ULink>
```

**Step 2: Verify the link works**

1. Navigate to: `http://localhost:3000/users/login`
2. Click "Forgot password?" link
3. Expected: Navigates to `/users/forgot-password`

**Step 3: Commit**

```bash
git add frontend/app/pages/users/login.vue
git commit -m "feat(frontend): link forgot password from login page

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 4: Run linting and type checking

**Files:** None (verification only)

**Step 1: Run ESLint**

```bash
cd frontend && pnpm lint
```

Expected: No errors

**Step 2: Run TypeScript check**

```bash
cd frontend && pnpm typecheck
```

Expected: No errors

**Step 3: Fix any issues found**

If errors found, fix them and re-run checks.

**Step 4: Commit fixes if any**

```bash
git add -A
git commit -m "fix(frontend): lint and type fixes for forgot-password page

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 5: Create documentation

**Files:**
- Create: `docs/frontend/pages/users/forgot-password.md`

**Step 1: Create documentation file**

```markdown
# Forgot Password Page in `frontend/app/pages/users/forgot-password.vue`

Password reset request page.

## Summary

- [Route](#route) — path and configuration
- [States](#states) — form and success states
- [Behavior](#behavior) — submit and resend handling

## Reference

### Route

| Property | Value |
|----------|-------|
| Path | `/users/forgot-password` |
| Layout | `blank` |
| Auth Required | No |

## States

### Form State

Initial state with email input form.

#### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | `email` | Yes | User email address |

#### Validation Schema (Zod)

```typescript
z.object({
  email: z.string().trim().min(1, 'Email is required').email('Invalid email address')
})
```

### Success State

Displayed after successful form submission. Shows confirmation message and resend button.

#### Elements

| Element | Description |
|---------|-------------|
| Icon | `i-lucide-mail-check` |
| Title | "Check your email" |
| Message | "We sent a password reset link to **{email}**" |
| Resend button | Disabled for 60s after send, shows countdown |
| Back link | Returns to `/users/login` |

## Behavior

### Submit Flow

1. Set `loading = true`, clear `formError`
2. POST to `/api/auth/password/reset/` with `{ email }`
3. On success or 400 (security: don't reveal if email exists):
   - Store email, switch to success state
   - Start 60-second resend cooldown
4. On 429: show rate limit error
5. On other errors: show "Network error. Please try again later."

### Resend Flow

1. Set `loading = true`, clear `formError`
2. POST to `/api/auth/password/reset/` with stored email
3. On success: restart 60-second cooldown
4. On error: show appropriate error message

### Error Handling

| Status | Display |
|--------|---------|
| 400 | Show success (security) |
| 429 | Server message or "Too many requests. Please try again later." |
| Other | "Network error. Please try again later." |

## UI Components

- `UPageCard` — card container
- `UAuthForm` — form state
- `UButton` — resend button
- `UAlert` — error display
- `UIcon` — success state icon
- `ULink` — navigation links

## Dependencies

- `useAxios` — API calls
- `onUnmounted` — cleanup cooldown interval

## Related

- [Login page](login.md) — links to this page
- [Password reset confirm](forgot-password-confirm.md) — next step in flow (future)
```

**Step 2: Commit**

```bash
git add docs/frontend/pages/users/forgot-password.md
git commit -m "docs(frontend): add forgot-password page documentation

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Create page with form state | `forgot-password.vue` (create) |
| 2 | Add success state with resend | `forgot-password.vue` (modify) |
| 3 | Update login page link | `login.vue` (modify) |
| 4 | Lint and type check | verification |
| 5 | Create documentation | `forgot-password.md` (create) |
