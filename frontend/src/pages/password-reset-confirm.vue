<script setup>
import authV1BottomShape from "@images/svg/auth-v1-bottom-shape.svg?raw";
import authV1TopShape from "@images/svg/auth-v1-top-shape.svg?raw";
import { VNodeRenderer } from "@layouts/components/VNodeRenderer";
import { themeConfig } from "@themeConfig";
import { requiredValidator } from "@validators";

const route = useRoute();

const isPasswordVisible = ref(false);
const isConfirmPasswordVisible = ref(false);

function processErrors(errors) {
  if (errors.uid || errors.token) {
    const non_field_errors = errors.non_field_errors ?? [];

    non_field_errors.push("Your password reset link seems to be wrong or expired.");
    errors.non_field_errors = non_field_errors;
  }
  return errors;
}

const { formData, valid, formRef, status, loading, errors, responseData, responseStatus, post } = usePostForm({
  url: "/auth/password/reset/confirm/",
  formInitialValue: { uid: route.query.uid, token: route.query.token, new_password1: "", new_password2: "" },
  customProcessErrors: processErrors,
});
</script>

<template>
  <div class="auth-wrapper d-flex align-center justify-center pa-4">
    <div class="position-relative my-sm-16">
      <!-- 👉 Top shape -->
      <VNodeRenderer
        :nodes="h('div', { innerHTML: authV1TopShape })"
        class="text-primary auth-v1-top-shape d-none d-sm-block" />

      <!-- 👉 Bottom shape -->
      <VNodeRenderer
        :nodes="h('div', { innerHTML: authV1BottomShape })"
        class="text-primary auth-v1-bottom-shape d-none d-sm-block" />

      <!-- 👉 Auth Card -->
      <VCard class="auth-card pa-4" max-width="448" :loading="loading">
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
          <h5 class="text-h5 mb-1">Reset Password 🔒</h5>
          <p class="mb-0">
            for <span class="font-weight-bold">{{ route.query.email }}</span>
          </p>
        </VCardText>

        <VCardText>
          <VForm ref="formRef" v-model="valid" validate-on="submit" @submit.prevent="post">
            <VRow>
              <VContainer v-if="status !== 'success'">
                <!-- password -->
                <VCol cols="12">
                  <AppTextField
                    v-model="formData.new_password1"
                    autofocus
                    label="New Password"
                    max-errors="5"
                    :type="isPasswordVisible ? 'text' : 'password'"
                    :rules="[requiredValidator]"
                    :error-messages="errors.new_password1"
                    :append-inner-icon="isPasswordVisible ? 'fasl:eye-slash' : 'fasl:eye'"
                    @click:append-inner="isPasswordVisible = !isPasswordVisible" />
                </VCol>

                <!-- Confirm Password -->
                <VCol cols="12">
                  <AppTextField
                    v-model="formData.new_password2"
                    label="Confirm Password"
                    max-errors="5"
                    :type="isConfirmPasswordVisible ? 'text' : 'password'"
                    :rules="[requiredValidator]"
                    :error-messages="errors.new_password2"
                    :append-inner-icon="isConfirmPasswordVisible ? 'fasl:eye-slash' : 'fasl:eye'"
                    @click:append-inner="isConfirmPasswordVisible = !isConfirmPasswordVisible" />
                </VCol>

                <VCol cols="12">
                  <FormErrors :error="false" :error-messages="errors.non_field_errors"></FormErrors>
                </VCol>

                <!-- reset password -->
                <VCol cols="12">
                  <VBtn block type="submit" :loading="loading"> Set New Password</VBtn>
                </VCol>
              </VContainer>
              <p v-else>You password successfully changed. Now you can login with new password.</p>

              <!-- back to login -->
              <VCol cols="12">
                <RouterLink class="d-flex align-center justify-center" :to="{ name: 'login' }">
                  <VIcon icon="fasl:chevron-left" class="flip-in-rtl" />
                  <span>Back to login</span>
                </RouterLink>
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

<route lang="json">
{ "meta": { "layout": "blank" } }
</route>
