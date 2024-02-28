<script setup>
import authV1BottomShape from "@images/svg/auth-v1-bottom-shape.svg?raw"
import authV1TopShape from "@images/svg/auth-v1-top-shape.svg?raw"
import { VNodeRenderer } from "@layouts/components/VNodeRenderer"
import { themeConfig } from "@themeConfig"
import { emailValidator, requiredValidator } from "@validators"

definePageMeta({ layout: "blank" })

useHead({ title: "Reset Password" })

const { errors, formData, formRef, loading, post, status, valid } = usePostForm({
  formInitialValue: { email: "" },
  url:              "/auth/password/reset/",
})
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
        :loading="loading"
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

        <VCardText class="pt-2">
          <h5 class="text-h5 mb-1">
            Reset Password 🔒
          </h5>
        </VCardText>

        <VCardText>
          <VForm
            ref="formRef"
            v-model="valid"
            validate-on="submit"
            @submit.prevent="post"
          >
            <VRow>
              <!-- password -->
              <VContainer v-if="status !== 'success'">
                <VCol cols="12">
                  <AppTextField
                    v-model="formData.email"
                    :error-messages="errors.email"
                    :rules="[emailValidator, requiredValidator]"
                    autofocus
                    label="Email"
                  />
                </VCol>

                <!-- reset password -->
                <VCol cols="12">
                  <VBtn
                    :loading="loading"
                    block
                    type="submit"
                  >
                    Reset password
                  </VBtn>
                </VCol>
              </VContainer>
              <p v-else>
                Password reset link sent to
                <span class="font-weight-bold">{{ formData.email }}.</span>
              </p>

              <!-- back to login -->
              <VCol cols="12">
                <NuxtLink
                  :to="{ name: 'login' }"
                  class="d-flex align-center justify-center"
                >
                  <VIcon icon="fasl:chevron-left" />
                  <span>Back to login</span>
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
