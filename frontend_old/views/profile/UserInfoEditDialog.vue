<script setup>
import { usePostForm } from "@/composables/usePostForm"
import { useUserStore } from "@/stores/user"
import { useQuery, useQueryClient } from "@tanstack/vue-query"

const props = defineProps({
  isDialogVisible: {
    required: true,
    type:     Boolean,
  },
})

const emit = defineEmits(["submit", "update:isDialogVisible"])

const { queries } = useQueryKeys()

const GENDERS = [
  { label: "Female", value: "F" },
  { label: "Male", value: "M" },
  { label: "Unicorn", value: "U" },
  { label: "Other", value: "O" },
]

const { data: profileData } = useQuery(queries.profile.profileData)

const user = useUserStore()

const getUserData = () => ({
  bio:        profileData.value?.bio,
  birth_date: user.birthDate,
  gender:     user.gender,
  name:       user.name,
})

const {
  errors,
  formData: userData,
  formRef,
  loading,
  post,
  reset,
  responseData,
  status,
  valid,
} = usePostForm({
  formInitialValue: getUserData(),
  httpMethod:       "patch",
  url:              "/profile/",
})

const queryClient = useQueryClient()

watch(status, () => {
  if (status.value === "success") {
    user.setUser(responseData.value)
    queryClient.invalidateQueries({ queryKey: ["profile"] })
    status.value = null
    emit("update:isDialogVisible", false)
  }
})

watch(profileData, () => {
  userData.value = getUserData()
})

const onFormReset = () => {
  emit("update:isDialogVisible", false)
  userData.value = getUserData()
  reset()
}

const dialogModelValueUpdate = (val) => {
  emit("update:isDialogVisible", val)
}
</script>

<template>
  <VDialog
    id="userInfoDialog"
    :model-value="props.isDialogVisible"
    :width="$vuetify.display.smAndDown ? 'auto' : 677"
    @update:model-value="dialogModelValueUpdate"
  >
    <!-- Dialog close btn -->
    <DialogCloseBtn @click="dialogModelValueUpdate(false)" />

    <VCard :loading="loading" class="pa-sm-8 pa-5">
      <VCardItem class="text-center">
        <VCardTitle class="text-h5 mb-3">
          Edit User Information
        </VCardTitle>
      </VCardItem>

      <VCardText>
        <!-- 👉 Form -->
        <VForm ref="formRef" v-model="valid" class="mt-6" validate-on="submit" @submit.prevent="post">
          <VRow>
            <!-- 👉 First Name -->
            <VCol cols="12">
              <AppTextField v-model="userData.name" :error-messages="errors.name" label="Name" />
            </VCol>

            <!-- 👉 Gender -->
            <VCol cols="6">
              <AppSelect
                v-model="userData.gender"
                :items="GENDERS"
                item-title="label"
                item-value="value"
                label="Gender"
              />
            </VCol>

            <!-- 👉 Birth Date -->
            <VCol cols="6">
              <AppTextField
                v-model="userData.birth_date"
                :error-messages="errors.birth_date"
                label="Birth Date"
                type="date"
              />
            </VCol>

            <!-- 👉 Bi0 -->
            <VCol cols="12">
              <AppTextarea
                v-model="userData.bio"
                :error-messages="errors.bio"
                label="Tell us about yourself"
                type="date"
              />
            </VCol>

            <VCol cols-12>
              <FormErrors :error="false" :error-messages="errors.non_field_errors" />
            </VCol>

            <!-- 👉 Submit and Cancel -->
            <VCol class="d-flex flex-wrap justify-center gap-4" cols="12">
              <VBtn :loading="loading" type="submit">
                Submit
              </VBtn>

              <VBtn :loading="loading" color="secondary" variant="tonal" @click="onFormReset">
                Cancel
              </VBtn>
            </VCol>
          </VRow>
        </VForm>
      </VCardText>
    </VCard>
  </VDialog>
</template>
