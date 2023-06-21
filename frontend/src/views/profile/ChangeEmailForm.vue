<script setup>
import { usePostForm } from "@/composables/usePostForm";
import { requiredValidator } from "@validators";
import { useUserStore } from "@/stores/user";

const user = useUserStore();

const { formData, valid, formRef, status, loading, errors, responseData, post } = usePostForm({
  url: "/profile/change-email/",
  formInitialValue: {
    email: user.email,
  },
  httpMethod: "put",
});

const toast = useTitledToast();

watch(status, () => {
  if (status.value === "success") {
    toast.success("Your email has been changed.", "Please check your inbox and verify email");
    user.email = responseData.value.email;
    user.email_verified = responseData.value.verified;
  }
});
</script>

<template>
  <VCard title="Change Email" :loading="loading">
    <VCardText>
      <p>
        Your email is the only way to reset your password. Please be sure, that email is correct and verified ad that
        you have access to this email
      </p>
      <VForm ref="formRef" v-model="valid" validate-on="submit" @submit.prevent="post">
        <VRow>
          <VCol cols="12">
            <AppTextField
              v-model="formData.email"
              label="Email"
              max-errors="5"
              type="email"
              :rules="[requiredValidator]"
              :error-messages="errors.email" />
          </VCol>

          <VCol cols="12">
            <FormErrors max-errors="5" :error="false" :error-messages="errors.non_field_errors"></FormErrors>
          </VCol>

          <VCol cols="12">
            <VBtn block type="submit" :loading="loading"> Change Email</VBtn>
          </VCol>
        </VRow>
      </VForm>
    </VCardText>
  </VCard>
</template>
