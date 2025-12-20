<script setup lang="ts">
import authV1BottomShape from "@images/svg/auth-v1-bottom-shape.svg?raw"
import authV1TopShape from "@images/svg/auth-v1-top-shape.svg?raw"
import { VNodeRenderer } from "@layouts/components/VNodeRenderer"
import { themeConfig } from "@themeConfig"
import { requiredValidator } from "@validators"

definePageMeta({ layout: "blank" })

useHead({ title: "Log In" })

const form = reactive({
  formErrors: null,
  loading:    false,
  password:   "",
  username:   "",
  valid:      false,
})

const isPasswordVisible = ref(false)
const loginForm = ref(null)

const userStore = useUserStore()
const route = useRoute()
const router = useRouter()

async function login() {
  form.loading = true
  form.formErrors = null

  const { valid } = await loginForm.value.validate()
  if (!valid) {
    form.loading = false

    return
  }

  const toast = useTitledToast()
  const loginError = await userStore.login(form.username, form.password)

  userStore.$persist()

  if (loginError) {
    if (loginError?.response?.status === 400) {
      toast.error("Bad credentials", "")
      form.formErrors = loginError.response.data.non_field_errors
    }
    else {
      toast.error("We experencing network troubles", "Please, try again later", { timeout: false })
    }
  }
  else {
    toast.success(`${userStore.name || userStore.username}, welcome back!`, "We missed you...")
    await router.replace(route.query.to ? String(route.query.to) : "/")
  }
  form.loading = false
}
</script>

<template>
  <div class="auth-wrapper d-flex align-center justify-center pa-4">
    <div class="position-relative my-sm-16">
      <!-- 👉 Top shape -->
      <VNodeRenderer
        :nodes="h('div', { innerHTML: authV1TopShape })"
        class="text-primary auth-v1-top-shape d-none d-sm-block"
      />

      <!-- 👉 Bottom shape -->
      <VNodeRenderer
        :nodes="h('div', { innerHTML: authV1BottomShape })"
        class="text-primary auth-v1-bottom-shape d-none d-sm-block"
      />

      <!-- 👉 Auth Card -->
      <VCard
        class="auth-card pa-4"
        max-width="448"
      >
        <VCardItem class="justify-center">
          <template #prepend>
            <div class="d-flex">
              <VNodeRenderer :nodes="themeConfig.app.logo" />
            </div>
          </template>

          <VCardTitle class="font-weight-bold text-capitalize text-h5 py-1">
            {{ themeConfig.app.title }}
          </VCardTitle>
        </VCardItem>

        <VCardText class="pt-1">
          <h5 class="text-h5 mb-1">
            Welcome to <span class="text-capitalize">{{ themeConfig.app.title }}</span>! 👋🏻
          </h5>
          <p class="mb-0">
            Please sign-in to your account and start the adventure
          </p>
        </VCardText>

        <VCardText>
          <VForm
            ref="loginForm"
            v-model="form.valid"
            @submit.prevent="login"
          >
            <VRow>
              <!-- username -->
              <VCol cols="12">
                <AppTextField
                  v-model="form.username"
                  :rules="[requiredValidator]"
                  autofocus
                  label="Username"
                />
              </VCol>

              <!-- password -->
              <VCol cols="12">
                <AppTextField
                  v-model="form.password"
                  :append-inner-icon="isPasswordVisible ? 'fasl:eye-slash' : 'fasl:eye'"
                  :rules="[requiredValidator]"
                  :type="isPasswordVisible ? 'text' : 'password'"
                  label="Password"
                  @click:append-inner="isPasswordVisible = !isPasswordVisible"
                />
              </VCol>

              <FormErrors
                :error="false"
                :error-messages="form.formErrors"
              />

              <VCol
                class="pt-1 pb-1"
                cols-12
              >
                <NuxtLink
                  :to="{ name: 'reset-password' }"
                  class="text-primary ms-2 mb-1"
                >
                  Forgot Password?
                </NuxtLink>
              </VCol>

              <VCol
                class="pt-1 pb-1"
                cols="12"
              >
                <VBtn
                  :loading="form.loading"
                  block
                  color="primary"
                  type="submit"
                >
                  Login
                  <VIcon
                    end
                    icon="fasl:arrow-right-to-bracket"
                  />
                </VBtn>
              </VCol>

              <!-- create account -->
              <VCol
                class="text-center text-base"
                cols="12"
              >
                <span>New on our platform?</span>
                <NuxtLink
                  :to="{ name: 'register', query: route.query }"
                  class="text-primary ms-2"
                >
                  Create an account
                </NuxtLink>
              </VCol>
            </VRow>
          </VForm>
        </VCardText>
      </VCard>
    </div>
  </div>
</template>

<style lang="scss">
@use "@core/scss/template/pages/page-auth.scss";
</style>
