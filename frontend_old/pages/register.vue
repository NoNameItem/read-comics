<script setup>
import authV1BottomShape from "@images/svg/auth-v1-bottom-shape.svg?raw"
import authV1TopShape from "@images/svg/auth-v1-top-shape.svg?raw"
import { VNodeRenderer } from "@layouts/components/VNodeRenderer"
import { themeConfig } from "@themeConfig"
import { requiredValidator } from "@validators"

definePageMeta({ layout: "blank" })

useHead({ title: "Register" })

const route = useRoute()

const registerForm = ref(null)

const form = reactive({
  email:      "",
  formErrors: null,
  loading:    false,
  password:   "",
  username:   "",
  valid:      false,
})

const backendErrors = ref({
  email:            [],
  non_field_errors: [],
  password1:        [],
  username:         [],
})

const isPasswordVisible = ref(false)

const userStore = useUserStore()

async function register() {
  form.loading = true
  backendErrors.value = {
    email:            [],
    non_field_errors: [],
    password1:        [],
    username:         [],
  }
  form.valid = (await registerForm.value.validate()).valid
  if (!form.valid) {
    form.loading = false

    return
  }

  const toast = useTitledToast()
  const registerError = await userStore.register(form.username, form.email, form.password)

  userStore.$persist()

  if (registerError) {
    if (registerError?.response?.status === 400) { backendErrors.value = registerError.response.data }
    else { toast.error("We experencing network troubles", "Please, try again later", { timeout: false }) }
  }
  else {
    toast.success(`${userStore.username}, nice to meet you!`, "Hope you will like us...")
    await navigateTo({ name: "verify-email", query: { to: route.query.to } })
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

      <!-- 👉 Auth card -->
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

          <VCardTitle class="font-weight-bold text-h5 text-capitalize py-1">
            {{ themeConfig.app.title }}
          </VCardTitle>
        </VCardItem>

        <VCardText class="pt-2">
          <h5 class="text-h5 mb-1">
            Adventure starts here 🚀
          </h5>
        </VCardText>

        <VCardText>
          <VForm
            ref="registerForm"
            v-model="form.valid"
            @submit.prevent="register"
          >
            <VRow>
              <!-- Username -->
              <VCol cols="12">
                <AppTextField
                  v-model="form.username"
                  :error-messages="backendErrors.username"
                  :rules="[requiredValidator]"
                  autofocus
                  label="Username"
                />
              </VCol>
              <!-- email -->
              <VCol cols="12">
                <AppTextField
                  v-model="form.email"
                  :error-messages="backendErrors.email"
                  :rules="[requiredValidator]"
                  label="Email"
                  type="email"
                />
              </VCol>

              <!-- password -->
              <VCol cols="12">
                <AppTextField
                  v-model="form.password"
                  :append-inner-icon="isPasswordVisible ? 'fasl:eye-slash' : 'fasl:eye'"
                  :error-messages="backendErrors.password1"
                  :rules="[requiredValidator]"
                  :type="isPasswordVisible ? 'text' : 'password'"
                  label="Password"
                  @click:append-inner="isPasswordVisible = !isPasswordVisible"
                />
              </VCol>

              <FormErrors
                :error="false"
                :error-messages="backendErrors.non_field_errors"
              />

              <VCol
                class="pt-1 pb-1"
                cols="12"
              >
                <VBtn
                  :loading="form.loading"
                  block
                  type="submit"
                >
                  Sign up
                  <VIcon
                    end
                    icon="fasl:arrow-right-to-bracket"
                  />
                </VBtn>
              </VCol>

              <!-- login instead -->
              <VCol
                class="text-center text-base"
                cols="12"
              >
                <span>Already have an account?</span>
                <NuxtLink
                  :to="{ name: 'login', query: { to: route.query.to } }"
                  class="text-primary ms-2"
                >
                  Sign in instead
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
