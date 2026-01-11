<!-- Docs: [[docs/frontend/pages/users/login.md]] -->
<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent, AuthFormField } from '@nuxt/ui'

definePageMeta({
  layout: 'blank'
})

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const toast = useToast()

const loading = ref(false)
const formError = ref<string | null>(null)

const registerLink = computed(() => ({
  path: '/users/register',
  query: route.query.to ? { to: route.query.to } : undefined
}))

const fields: AuthFormField[] = [
  {
    name: 'login',
    type: 'string',
    label: 'Login',
    placeholder: 'Enter your login',
    required: true
  },
  {
    name: 'password',
    label: 'Password',
    type: 'password',
    placeholder: 'Enter your password',
    required: true
  }
]

const schema = z.object({
  login: z.string('Login is required').trim().min(1, 'Login is required'),
  password: z.string('Password is required').trim().min(1, 'Password is required')
})

type Schema = z.output<typeof schema>

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  loading.value = true
  formError.value = null

  const loginError = await userStore.login(payload.data.login, payload.data.password)

  if (loginError) {
    loading.value = false
    const axiosError = loginError as {
      response?: { status?: number; data?: { non_field_errors?: string[] } }
    }
    if (axiosError?.response?.status === 400) {
      formError.value = axiosError.response.data?.non_field_errors?.[0] || 'Invalid credentials'
    } else {
      formError.value = 'Network error. Please try again later.'
    }
    return
  }

  toast.add({
    title: `Welcome back, ${userStore.name || userStore.username}!`,
    color: 'success'
  })

  const redirectTo = route.query.to ? String(route.query.to) : '/'
  await router.replace(redirectTo)
}
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-4 p-4">
    <UPageCard class="w-full max-w-md">
      <UAuthForm
        :schema="schema"
        :fields="fields"
        :loading="loading"
        title="Welcome back!"
        icon="i-lucide-lock"
        @submit="onSubmit"
      >
        <template #description>
          Don't have an account?
          <ULink :to="registerLink" class="text-primary font-medium">Sign up</ULink>.
        </template>
        <template #password-hint>
          <ULink to="/users/forgot-password" class="text-primary font-medium" tabindex="-1"
            >Forgot password?</ULink
          >
        </template>
        <template #validation>
          <UAlert v-if="formError" color="error" icon="i-lucide-circle-alert" :title="formError" />
        </template>
      </UAuthForm>
    </UPageCard>
  </div>
</template>
