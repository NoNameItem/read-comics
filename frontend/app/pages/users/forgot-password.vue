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
    startCooldown()
  } catch (error: unknown) {
    const axiosError = error as { response?: { status?: number; data?: { detail?: string } } }
    if (axiosError?.response?.status === 429) {
      formError.value =
        axiosError.response.data?.detail || 'Too many requests. Please try again later.'
    } else if (axiosError?.response?.status === 400) {
      // Don't reveal if email exists - show success anyway
      submittedEmail.value = payload.data.email
      emailSent.value = true
      startCooldown()
    } else {
      formError.value = 'Network error. Please try again later.'
    }
  } finally {
    loading.value = false
  }
}

async function onResend() {
  loading.value = true
  formError.value = null

  try {
    await axios.post('/auth/password/reset/', { email: submittedEmail.value })
    startCooldown()
  } catch (error: unknown) {
    const axiosError = error as { response?: { status?: number; data?: { detail?: string } } }
    if (axiosError?.response?.status === 429) {
      formError.value =
        axiosError.response.data?.detail || 'Too many requests. Please try again later.'
    } else if (axiosError?.response?.status === 400) {
      // Email may not exist, but still show success for security
      startCooldown()
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
      <div v-if="emailSent" class="space-y-6">
        <div class="flex flex-col items-center text-center">
          <UIcon name="i-lucide-mail-check" class="size-8 mb-2 text-primary" />
          <h1 class="text-xl font-semibold text-highlighted">Check your email</h1>
          <p class="mt-1 text-base text-muted">
            We sent a password reset link to <strong>{{ submittedEmail }}</strong>
          </p>
        </div>

        <UAlert v-if="formError" color="error" icon="i-lucide-circle-alert" :title="formError" />

        <UButton block :loading="loading" :disabled="resendCooldown > 0" @click="onResend">
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
