<script setup lang="ts">
import { useUserStore } from "@/stores/user"
import { avatarText, kFormatter } from "@core/utils/formatters"
import { useMutation, useQuery } from "@tanstack/vue-query"
import { DateTime } from "luxon"
import { VSkeletonLoader } from "vuetify/labs/VSkeletonLoader"

const axios = useAxios()
const { queries } = useQueryKeys()

const GENDER_COLORS = {
  F: "error",
  M: "primary",
  O: "info",
  U: "success",
}

const user = useUserStore()

user.$hydrate()

const { data, isError, isPending, suspense } = useQuery(queries.profile.finishedStats)

onServerPrefetch(async () => {
  await suspense()
})

const isUserInfoEditDialogVisible = ref(false)

const emailBadgeColor = computed(() => (user.email_verified ? "success" : "danger"))
const emailBadgeText = computed(() => (user.email_verified ? "Verified" : "Not verified"))
const genderBadgeColor = computed(() => GENDER_COLORS[user.gender?.value])

const role = computed(() => {
  if (user.isSuperuser) {
    return {
      color: "success",
      text:  "Superuser",
    }
  }
  if (user.isStaff) {
    return {
      color: "warning",
      text:  "Staff",
    }
  }

  return {
    color: "primary",
    text:  "Reader",
  }
})

const { resentConfirmation } = useResentEmailConfirmation()

// User image

const imageInputRef = ref(null)
const imageDisplayRef = ref(null)
const resetImageButtonRef = ref(null)

const showImageResetBadge = computed(() => user.images && imageDisplayRef.value?.state === "loaded")

// Change Image
const changeImageMutation = useMutation({
  mutationFn: formData =>
    axios.patch("/profile/", formData, { headers: { "Content-Type": "multipart/form-data" } }),
  mutationKey: "changeImage",
})

const changeImage = async (file): void => {
  const { files } = file.target
  if (files?.length) {
    const formData = new FormData()

    formData.append("images", files[0])
    try {
      const result = await changeImageMutation.mutateAsync(formData)
      const data = await result.data

      user.setImage(data)
    }
    catch (error) {
      const toast = useTitledToast()

      toast.error("Could not upload image")
    }
  }
}

const resetImageMutation = useMutation({
  mutationFn:  () => axios.patch("/profile/", { images: null }),
  mutationKey: "resetImage",
})

const resetImage = async () => {
  try {
    await resetImageMutation.mutateAsync(null)
    user.resetImage()
    user.$persist()
  }
  catch (error) {
    const toast = useTitledToast()

    toast.error("Could not reset image")
  }
}
</script>

<template>
  <div>
    <VCol
      cols="12"
      lg="4"
      md="5"
      xl="3"
      xxl="2"
    >
      <VRow>
        <!-- SECTION User Details -->
        <VCol cols="12">
          <VCard position="sticky">
            <VCardText class="text-center pt-15">
              <!-- 👉 Avatar -->
              <div class="avatar-with-badge-btn">
                <div class="avatar-wrapper">
                  <VAvatar
                    :color="!user.image ? 'primary' : undefined"
                    :size="100"
                    :variant="!user.image ? 'tonal' : undefined"
                    rounded
                  >
                    <VImg
                      v-if="user.image"
                      ref="imageDisplayRef"
                      :src="user.image"
                    >
                      <template #placeholder>
                        <div class="d-flex align-center justify-center fill-height">
                          <VSkeletonLoader type="avatar" />
                        </div>
                      </template>
                    </VImg>
                    <span
                      v-else
                      class="text-5xl font-weight-medium"
                    >
                      {{ avatarText(user.name || user.username) }}
                    </span>
                  </VAvatar>
                  <VBtn
                    v-if="showImageResetBadge"
                    ref="resetImageButtonRef"
                    :loading="resetImageMutation.isPending.value"
                    class="reset-image-btn"
                    color="error"
                    elevation="20"
                    icon="fasl:xmark-large"
                    size="x-small"
                    @click="resetImage"
                  />
                  <VTooltip
                    v-if="showImageResetBadge"
                    :activator="resetImageButtonRef"
                    location="bottom"
                  >
                    Reset Image
                  </VTooltip>
                </div>
              </div>

              <!-- 👉 User fullName -->
              <h6 class="text-h4 mt-4">
                {{ user.name || `@${user.username}` }}
              </h6>

              <!-- 👉 Role chip -->
              <VChip
                :color="role.color"
                class="text-capitalize mt-3"
                label
                size="small"
              >
                {{ role.text }}
              </VChip>
            </VCardText>

            <VCardText class="d-flex justify-center mt-3">
              <div class="d-flex align-center me-4">
                <VSkeletonLoader
                  v-if="!isError"
                  :loading="isPending"
                  type="list-item-avatar-two-line"
                >
                  <VAvatar
                    :size="38"
                    class="me-3"
                    color="primary"
                    rounded
                    variant="tonal"
                  >
                    <VIcon icon="fasl:circle-check" />
                  </VAvatar>

                  <div>
                    <h6 class="text-h6">
                      {{ kFormatter(data.finished_count) }}
                      <VChip
                        v-if="data.today_finished_count > 0"
                        color="success"
                        size="x-small"
                      >
                        +{{ data.today_finished_count }}
                      </VChip>
                    </h6>
                    <span class="text-sm">Finished issues</span>
                  </div>
                </VSkeletonLoader>
              </div>

              <div class="d-flex align-center">
                <VSkeletonLoader
                  v-if="!isError"
                  :loading="isPending"
                  type="list-item-avatar-two-line"
                >
                  <VAvatar
                    :size="38"
                    class="me-3"
                    color="primary"
                    rounded
                    variant="tonal"
                  >
                    <VIcon icon="fasl:gauge-high" />
                  </VAvatar>

                  <div>
                    <h6 class="text-h6">
                      {{ Math.ceil(data.reading_speed).toLocaleString() }}
                    </h6>
                    <span class="text-sm">issues/day</span>
                  </div>
                </VSkeletonLoader>
              </div>
            </VCardText>

            <VDivider />

            <!-- 👉 Details -->
            <VCardText>
              <p class="text-sm text-uppercase text-disabled">
                Details
              </p>

              <!-- 👉 User Details list -->
              <VList class="card-list mt-2">
                <VListItem>
                  <VListItemTitle>
                    <h6 class="text-h6">
                      Username:
                      <span class="text-body-1">
                        {{ user.username }}
                      </span>
                    </h6>
                  </VListItemTitle>
                </VListItem>

                <VListItem>
                  <VListItemTitle>
                    <h6 class="text-h6">
                      Email:
                      <span class="text-body-1">{{ user.email }}</span>
                      <br>
                      <VChip
                        :color="emailBadgeColor"
                        class="text-capitalize ml-1"
                        label
                        size="small"
                      >
                        {{ emailBadgeText }}
                      </VChip>
                      <VBtn
                        v-if="!user.email_verified"
                        color="info"
                        size="x-small"
                        variant="plain"
                        @click="resentConfirmation"
                      >
                        <VIcon icon="fasl:arrows-rotate" />
                        <VTooltip
                          activator="parent"
                          location="bottom"
                        >
                          Resent confirmation
                        </VTooltip>
                      </VBtn>
                    </h6>
                  </VListItemTitle>
                </VListItem>

                <VListItem>
                  <VListItemTitle>
                    <h6 class="text-h6">
                      Gender:

                      <VChip
                        :color="genderBadgeColor"
                        class="text-capitalize ml-1"
                        label
                        size="small"
                      >
                        {{ user.gender?.label }}
                      </VChip>
                    </h6>
                  </VListItemTitle>
                </VListItem>

                <VListItem>
                  <VListItemTitle>
                    <h6 class="text-h6">
                      Birth date:
                      <span class="text-capitalize text-body-1">
                        {{ formatDate(user.birthDate) }}
                      </span>
                    </h6>
                  </VListItemTitle>
                </VListItem>

                <VListItem>
                  <VListItemTitle>
                    <h6 class="text-h6">
                      Registered:
                      <span class="text-capitalize text-body-1">
                        {{ DateTime.fromISO(user.registerDate).toRelative({ locale: 'en-US' }) }}
                        <VTooltip
                          activator="parent"
                          location="end"
                          open-delay="500"
                        >
                          {{ formatDateTimeMinutes(user.registerDate) }}
                        </VTooltip>
                      </span>
                    </h6>
                  </VListItemTitle>
                </VListItem>
              </VList>
            </VCardText>

            <!-- 👉 Edit and Change image button -->
            <VCardText class="d-flex justify-center">
              <VBtn
                class="me-4"
                variant="elevated"
                @click="isUserInfoEditDialogVisible = true"
              >
                Edit
              </VBtn>

              <VBtn
                variant="elevated"
                @click="imageInputRef?.click()"
              >
                Change avatar
              </VBtn>
              <input
                ref="imageInputRef"
                accept=".jpeg,.png,.jpg,GIF"
                hidden
                name="avatar"
                type="file"
                @input="changeImage"
              >
            </VCardText>
          </VCard>
        </VCol>
        <!-- !SECTION -->
      </VRow>
    </VCol>

    <!-- 👉 Edit user info dialog -->
    <UserInfoEditDialog v-model:isDialogVisible="isUserInfoEditDialogVisible" />
  </div>
</template>

<style lang="scss" scoped>
.card-list {
  --v-card-list-gap: 0.75rem;
}

.text-capitalize {
  text-transform: capitalize !important;
}

.avatar-with-badge-btn {
  display: inline-block;
  line-height: 1;
}

.avatar-wrapper {
  display: flex;
  position: relative;
}

.reset-image-btn {
  top: -30px;
  right: -30px;
  display: inline-flex;
  pointer-events: auto;
  position: absolute;
}
</style>
