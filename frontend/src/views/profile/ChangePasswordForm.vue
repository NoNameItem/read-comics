<script setup>
import { usePostForm } from "@/composables/usePostForm";
import { requiredValidator } from "@validators";

const isOldPasswordVisible = ref(false);
const isNewPasswordVisible = ref(false);
const isConfirmPasswordVisible = ref(false);

const { formData, valid, formRef, status, loading, errors, post } = usePostForm({
  url: "/auth/password/change/",
  formInitialValue: {
    new_password1: "",
    new_password2: "",
  },
});

const toast = useTitledToast();

watch(status, () => {
  if (status.value === "success") {
    toast.success("Your password has been changed");
  }
});
</script>

<template>
  <VCard title="Change Password" :loading="loading">
    <VCardText>
      <VForm ref="formRef" v-model="valid" validate-on="submit" @submit.prevent="post">
        <VRow>
          <VCol cols="12">
            <AppTextField
              v-model="formData.new_password1"
              label="New Password"
              max-errors="5"
              :type="isNewPasswordVisible ? 'text' : 'password'"
              :rules="[requiredValidator]"
              :error-messages="errors.new_password1"
              :append-inner-icon="isNewPasswordVisible ? 'fasl:eye-slash' : 'fasl:eye'"
              @click:append-inner="isNewPasswordVisible = !isNewPasswordVisible" />
          </VCol>
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
            <FormErrors max-errors="5" :error="false" :error-messages="errors.non_field_errors"></FormErrors>
          </VCol>

          <VCol cols="12">
            <VBtn block type="submit" :loading="loading"> Change Password</VBtn>
          </VCol>
        </VRow>
      </VForm>
    </VCardText>
  </VCard>
</template>
