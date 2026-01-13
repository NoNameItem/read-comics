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
