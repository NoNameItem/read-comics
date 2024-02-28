<script setup>
import { requiredValidator } from "@validators"

const user = useUserStore()

const { errors, formData, formRef, loading, post, responseData, status, valid } = usePostForm({
  formInitialValue: { email: user.email },
  httpMethod:       "put",
  url:              "/profile/change-email/",
})

const toast = useTitledToast()

watch(status, () => {
  if (status.value === "success") {
    toast.success("Your email has been changed.", "Please check your inbox and verify email")
    user.email = responseData.value.email
    user.email_verified = responseData.value.verified
  }
})
</script>

<template>
  <VCard
    :loading="loading"
    title="Change Email"
  >
    <VCardText>
      {{ status }}
      <p>
        Your email is the only way to reset your password. Please be sure, that email is correct and verified and that
        you have access to this email
      </p>
      <VForm
        ref="formRef"
        v-model="valid"
        validate-on="submit"
        @submit.prevent="post"
      >
        <VRow>
          <VCol cols="12">
            <AppTextField
              v-model="formData.email"
              :error-messages="errors.email"
              :rules="[requiredValidator]"
              label="Email"
              max-errors="5"
              type="email"
            />
          </VCol>

          <VCol cols="12">
            <FormErrors
              :error="false"
              :error-messages="errors.non_field_errors"
              max-errors="5"
            />
          </VCol>

          <VCol cols="12">
            <VBtn
              :loading="loading"
              block
              type="submit"
            >
              Change Email
            </VBtn>
          </VCol>
        </VRow>
      </VForm>
    </VCardText>
  </VCard>
</template>
