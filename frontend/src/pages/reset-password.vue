<script setup>
import authV1BottomShape from "@images/svg/auth-v1-bottom-shape.svg?raw";
import authV1TopShape from "@images/svg/auth-v1-top-shape.svg?raw";
import { VNodeRenderer } from "@layouts/components/VNodeRenderer";
import { themeConfig } from "@themeConfig";
import axios from "@axios";
import { emailValidator, requiredValidator } from "@validators";
import { usePostForm } from "@/composables/usePostForm";

const htmlTitle = useTitle();

htmlTitle.value = "Reset Password";

const emailSent = ref(false);

const { formData, valid, formRef, status, loading, errors, post } = usePostForm({
  url: "/auth/password/reset/",
  formInitialValue: { email: "" },
});

async function resetPassword() {
  loading.value = true;

  if (!valid.value) {
    loading.value = false;
    return;
  }

  await axios.post("/auth/password/reset/", { email: email.value });
  loading.value = false;
  emailSent.value = true;
}
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
        </VCardText>

        <VCardText>
          <VForm ref="formRef" v-model="valid" validate-on="submit" @submit.prevent="post">
            <VRow>
              <!-- password -->
              <VContainer v-if="status !== 'success'">
                <VCol cols="12">
                  <AppTextField
                    v-model="formData.email"
                    autofocus
                    label="Email"
                    :error-messages="errors.email"
                    :rules="[emailValidator, requiredValidator]" />
                </VCol>

                <!-- reset password -->
                <VCol cols="12">
                  <VBtn block type="submit" :loading="loading"> Reset password</VBtn>
                </VCol>
              </VContainer>
              <p v-else>
                Password reset link sent to
                <span class="font-weight-bold">{{ formData.email }}.</span>
              </p>

              <!-- back to login -->
              <VCol cols="12">
                <RouterLink class="d-flex align-center justify-center" :to="{ name: 'login' }">
                  <VIcon icon="fasl:chevron-left" />
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
