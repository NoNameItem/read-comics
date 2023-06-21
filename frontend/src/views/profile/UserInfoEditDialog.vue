<script setup>
import { useUserStore } from "@/stores/user";
import { useQuery, useQueryClient } from "@tanstack/vue-query";
import { queries } from "@/queries";
import { usePostForm } from "@/composables/usePostForm";

const props = defineProps({
  isDialogVisible: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(["submit", "update:isDialogVisible"]);

const GENDERS = [
  { value: "F", label: "Female" },
  { value: "M", label: "Male" },
  { value: "U", label: "Unicorn" },
  { value: "O", label: "Other" },
];

const { data: profileData } = useQuery(queries.profile.profileData);

const user = useUserStore();

const getUserData = () => ({
  name: user.name,
  gender: user.gender,
  birth_date: user.birthDate,
  bio: profileData.value?.bio,
});

const {
  formData: userData,
  valid,
  formRef,
  status,
  loading,
  errors,
  responseData,
  post,
  reset,
} = usePostForm({
  url: "/profile/",
  formInitialValue: getUserData(),
  httpMethod: "patch",
});

const queryClient = useQueryClient();

watch(status, () => {
  if (status.value === "success") {
    user.setUser(responseData.value);
    queryClient.invalidateQueries({ queryKey: ["profile"] });
    status.value = null;
    emit("update:isDialogVisible", false);
  }
});

watch(profileData, () => {
  userData.value = getUserData();
});

const onFormReset = () => {
  emit("update:isDialogVisible", false);
  userData.value = getUserData();
  reset();
};

const dialogModelValueUpdate = (val) => {
  emit("update:isDialogVisible", val);
};
</script>

<template>
  <VDialog
    id="userInfoDialog"
    :width="$vuetify.display.smAndDown ? 'auto' : 677"
    :model-value="props.isDialogVisible"
    @update:model-value="dialogModelValueUpdate">
    <!-- Dialog close btn -->
    <DialogCloseBtn @click="dialogModelValueUpdate(false)" />

    <VCard class="pa-sm-8 pa-5" :loading="loading">
      <VCardItem class="text-center">
        <VCardTitle class="text-h5 mb-3"> Edit User Information</VCardTitle>
      </VCardItem>

      <VCardText>
        <!-- 👉 Form -->
        <VForm ref="formRef" v-model="valid" class="mt-6" validate-on="submit" @submit.prevent="post">
          <VRow>
            <!-- 👉 First Name -->
            <VCol cols="12">
              <AppTextField v-model="userData.name" label="Name" :error-messages="errors.name" />
            </VCol>

            <!-- 👉 Gender -->
            <VCol cols="6">
              <AppSelect
                v-model="userData.gender"
                label="Gender"
                :items="GENDERS"
                item-title="label"
                item-value="value" />
            </VCol>

            <!-- 👉 Birth Date -->
            <VCol cols="6">
              <AppTextField
                v-model="userData.birth_date"
                label="Birth Date"
                type="date"
                :error-messages="errors.birth_date"></AppTextField>
            </VCol>

            <!-- 👉 Bi0 -->
            <VCol cols="12">
              <AppTextarea
                v-model="userData.bio"
                label="Tell us about yourself"
                type="date"
                :error-messages="errors.bio"></AppTextarea>
            </VCol>

            <VCol cols-12>
              <FormErrors :error="false" :error-messages="errors.non_field_errors"></FormErrors>
            </VCol>

            <!-- 👉 Submit and Cancel -->
            <VCol cols="12" class="d-flex flex-wrap justify-center gap-4">
              <VBtn type="submit" :loading="loading"> Submit</VBtn>

              <VBtn color="secondary" variant="tonal" :loading="loading" @click="onFormReset"> Cancel</VBtn>
            </VCol>
          </VRow>
        </VForm>
      </VCardText>
    </VCard>
  </VDialog>
</template>
