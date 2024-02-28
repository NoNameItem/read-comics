<script setup>
import { usePostForm } from "@/composables/usePostForm"
import { requiredValidator } from "@validators"

const isNewPasswordVisible = ref(false)
const isConfirmPasswordVisible = ref(false)

const { errors, formData, formRef, loading, post, status, valid } = usePostForm({
  formInitialValue: {
    new_password1: "",
    new_password2: "",
  },
  url: "/auth/password/change/",
})

const toast = useTitledToast()

watch(status, () => {
  if (status.value === "success") { toast.success("Your password has been changed") }
})
</script>

<template>
  <VCard :loading="loading" title="Change Password">
    <VCardText>
      <VForm ref="formRef" v-model="valid" validate-on="submit" @submit.prevent="post">
        <VRow>
          <VCol cols="12">
            <AppTextField
              v-model="formData.new_password1"
              :append-inner-icon="isNewPasswordVisible ? 'fasl:eye-slash' : 'fasl:eye'"
              :error-messages="errors.new_password1"
              :rules="[requiredValidator]"
              :type="isNewPasswordVisible ? 'text' : 'password'"
              label="New Password"
              max-errors="5"
              @click:append-inner="isNewPasswordVisible = !isNewPasswordVisible"
            />
          </VCol>
          <VCol cols="12">
            <AppTextField
              v-model="formData.new_password2"
              :append-inner-icon="isConfirmPasswordVisible ? 'fasl:eye-slash' : 'fasl:eye'"
              :error-messages="errors.new_password2"
              :rules="[requiredValidator]"
              :type="isConfirmPasswordVisible ? 'text' : 'password'"
              label="Confirm Password"
              max-errors="5"
              @click:append-inner="isConfirmPasswordVisible = !isConfirmPasswordVisible"
            />
          </VCol>

          <VCol cols="12">
            <FormErrors :error="false" :error-messages="errors.non_field_errors" max-errors="5" />
          </VCol>

          <VCol cols="12">
            <VBtn :loading="loading" block type="submit">
              Change Password
            </VBtn>
          </VCol>
        </VRow>
      </VForm>
    </VCardText>
  </VCard>
</template>
