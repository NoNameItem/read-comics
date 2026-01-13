# Password Reset Confirm Page Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a page where users can set a new password after clicking the reset link from their email.

**Architecture:** Single Vue page with form/success states. Reads uid/token from query params, submits to dj-rest-auth endpoint. Backend change updates the email link URL.

**Tech Stack:** Nuxt 3, Nuxt UI (UPageCard, UAuthForm), Zod validation, Axios

---

## Task 1: Update Backend URL

**Files:**
- Modify: `read_comics/users/api/serializers.py:45-49`

**Step 1: Update the URL in password_reset_url_generator**

Change line 47 from:
```python
f"{settings.FRONTEND_BASE_URL}/password-reset-confirm"
```

To:
```python
f"{settings.FRONTEND_BASE_URL}/users/password-reset"
```

**Step 2: Run backend tests to verify nothing broke**

Run: `docker compose -f local.yml run --rm django pytest read_comics/users/tests/test_drf_urls.py -v`

Expected: All tests pass

---

## Task 2: Create Password Reset Page

**Files:**
- Create: `frontend/app/pages/users/password-reset.vue`
- Reference: `frontend/app/pages/users/forgot-password.vue` (similar pattern)
- Reference: `frontend/app/pages/users/register.vue` (password validation pattern)

**Step 1: Create the page file**

Create `frontend/app/pages/users/password-reset.vue`:

```vue
<!-- Docs: [[docs/frontend/pages/users/password-reset.md]] -->
<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent, AuthFormField } from '@nuxt/ui'

definePageMeta({
  layout: 'blank'
})

const route = useRoute()
const axios = useAxios()

const loading = ref(false)
const formError = ref<string | null>(null)
const resetComplete = ref(false)
const showRequestNewLink = ref(false)

// Get params from URL
const uid = computed(() => route.query.uid as string | undefined)
const token = computed(() => route.query.token as string | undefined)

// Redirect if missing params
onMounted(() => {
  if (!uid.value || !token.value) {
    navigateTo('/users/forgot-password')
  }
})

const fields: AuthFormField[] = [
  {
    name: 'password',
    type: 'password',
    label: 'New password',
    placeholder: 'Enter new password',
    required: true
  },
  {
    name: 'confirmPassword',
    type: 'password',
    label: 'Confirm password',
    placeholder: 'Confirm new password',
    required: true
  }
]

const schema = z
  .object({
    password: z.string().min(1, 'Password is required'),
    confirmPassword: z.string().min(1, 'Please confirm your password')
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword']
  })

type Schema = z.output<typeof schema>

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  loading.value = true
  formError.value = null
  showRequestNewLink.value = false

  try {
    await axios.post('/auth/password/reset/confirm/', {
      uid: uid.value,
      token: token.value,
      new_password1: payload.data.password,
      new_password2: payload.data.confirmPassword
    })
    resetComplete.value = true
  } catch (error: unknown) {
    const axiosError = error as {
      response?: {
        status?: number
        data?: {
          token?: string[]
          uid?: string[]
          new_password1?: string[]
          new_password2?: string[]
          non_field_errors?: string[]
        }
      }
    }

    if (axiosError?.response?.status === 400) {
      const errors = axiosError.response.data

      // Check for invalid/expired token
      if (errors?.token || errors?.uid) {
        formError.value =
          'This password reset link has expired or is invalid. Please request a new one.'
        showRequestNewLink.value = true
      } else {
        // Password validation errors from backend
        formError.value =
          errors?.new_password1?.[0] ||
          errors?.new_password2?.[0] ||
          errors?.non_field_errors?.[0] ||
          'Password reset failed'
      }
    } else if (axiosError?.response?.status === 429) {
      formError.value =
        (axiosError.response.data as { detail?: string })?.detail ||
        'Too many requests. Please try again later.'
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
      <!-- Success State -->
      <div v-if="resetComplete" class="space-y-6">
        <div class="flex flex-col items-center text-center">
          <UIcon name="i-lucide-check-circle" class="size-8 mb-2 text-primary" />
          <h1 class="text-xl font-semibold text-highlighted">Password changed</h1>
          <p class="mt-1 text-base text-muted">
            Your password has been updated. You can now log in with your new password.
          </p>
        </div>

        <UButton block to="/users/login">Log in</UButton>
      </div>

      <!-- Form State -->
      <UAuthForm
        v-else
        :schema="schema"
        :fields="fields"
        :loading="loading"
        title="Set new password"
        icon="i-lucide-key-round"
        submit-label="Save new password"
        @submit="onSubmit"
      >
        <template #validation>
          <UAlert v-if="formError" color="error" icon="i-lucide-circle-alert" :title="formError">
            <template v-if="showRequestNewLink" #actions>
              <UButton
                to="/users/forgot-password"
                color="error"
                variant="outline"
                size="xs"
                label="Request new link"
              />
            </template>
          </UAlert>
        </template>
      </UAuthForm>
    </UPageCard>
  </div>
</template>
```

**Step 2: Verify the dev server runs without errors**

Run: `cd frontend && pnpm dev`

Open: `http://localhost:3000/users/password-reset` (should redirect to forgot-password)
Open: `http://localhost:3000/users/password-reset?uid=test&token=test` (should show form)

---

## Task 3: Manual Testing

**Step 1: Test the full flow**

1. Start backend: `docker compose -f local.yml up`
2. Start frontend: `cd frontend && pnpm dev`
3. Go to `http://localhost:3000/users/forgot-password`
4. Enter a valid email and submit
5. Check MailHog at `http://localhost:8025` for the reset email
6. Click the link in the email - should open `/users/password-reset?uid=...&token=...`
7. Enter new password and confirm
8. Should see success state
9. Click "Log in" and verify login works with new password

**Step 2: Test error cases**

1. Go to `/users/password-reset` without params → should redirect to forgot-password
2. Go to `/users/password-reset?uid=invalid&token=invalid` → submit form → should show "link expired" error
3. Enter mismatched passwords → should show "Passwords do not match" error

---

## Task 4: Lint and Type Check

**Step 1: Run lint**

Run: `cd frontend && pnpm lint:fix`

Expected: No errors (warnings OK)

**Step 2: Run type check**

Run: `cd frontend && pnpm typecheck`

Expected: No errors

---

## Summary

| Task | Description |
|------|-------------|
| 1 | Update backend URL in serializers.py |
| 2 | Create password-reset.vue page |
| 3 | Manual testing of full flow |
| 4 | Lint and type check |
