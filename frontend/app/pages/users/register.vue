<!-- Docs: [[docs/frontend/pages/users/register.md]] -->
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

const fields: AuthFormField[] = [
  {
    name: 'username',
    type: 'string',
    label: 'Username',
    placeholder: 'Enter your username',
    required: true
  },
  {
    name: 'email',
    type: 'string',
    label: 'Email',
    placeholder: 'Enter your email',
    required: true
  },
  {
    name: 'password',
    label: 'Password',
    type: 'password',
    placeholder: 'Enter your password',
    required: true
  },
  {
    name: 'confirmPassword',
    label: 'Confirm Password',
    type: 'password',
    placeholder: 'Confirm your password',
    required: true
  }
]

const schema = z
  .object({
    username: z.string('Username is required').trim().min(1, 'Username is required'),
    email: z
      .string('Email is required')
      .trim()
      .min(1, 'Email is required')
      .email('Invalid email address'),
    password: z.string('Password is required').min(8, 'Password must be at least 8 characters'),
    confirmPassword: z.string('Email is required').min(1, 'Please confirm your password')
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword']
  })

type Schema = z.output<typeof schema>

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  loading.value = true
  formError.value = null

  const registerError = await userStore.register(
    payload.data.username,
    payload.data.email,
    payload.data.password
  )

  if (registerError) {
    loading.value = false
    const axiosError = registerError as {
      response?: {
        status?: number
        data?: {
          username?: string[]
          email?: string[]
          password1?: string[]
          non_field_errors?: string[]
        }
      }
    }
    if (axiosError?.response?.status === 400) {
      const errors = axiosError.response.data
      formError.value =
        errors?.username?.[0] ||
        errors?.email?.[0] ||
        errors?.password1?.[0] ||
        errors?.non_field_errors?.[0] ||
        'Registration failed'
    } else {
      formError.value = 'Network error. Please try again later.'
    }
    return
  }

  toast.add({
    title: `Welcome, ${userStore.displayName}!`,
    color: 'success'
  })

  const redirectTo = route.query.to ? String(route.query.to) : '/'
  await router.replace(redirectTo)
}

const loginLink = computed(() => ({
  path: '/users/login',
  query: route.query.to ? { to: route.query.to } : undefined
}))
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-4 p-4">
    <UPageCard class="w-full max-w-md">
      <UAuthForm
        :schema="schema"
        :fields="fields"
        :loading="loading"
        title="Create an account"
        icon="i-lucide-user-plus"
        submit-label="Sign up"
        @submit="onSubmit"
      >
        <template #description>
          Already have an account?
          <ULink :to="loginLink" class="text-primary font-medium">Log in</ULink>.
        </template>
        <template #validation>
          <UAlert v-if="formError" color="error" icon="i-lucide-circle-alert" :title="formError" />
        </template>
      </UAuthForm>
    </UPageCard>
  </div>
</template>
