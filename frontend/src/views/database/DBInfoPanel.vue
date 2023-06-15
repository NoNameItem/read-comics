<script setup>
import { avatarText } from "@core/utils/formatters";
import { VSkeletonLoader } from "vuetify/labs/VSkeletonLoader";

const props = defineProps({
  data: {
    type: Object,
    required: false,
  },
  loading: {
    type: Boolean,
    required: false,
    default: true,
  },
});

const isImageDialogVisible = ref(false);

const openImageDialog = () => {
  isImageDialogVisible.value = true;
};

const closeImageDialog = () => {
  isImageDialogVisible.value = false;
};
</script>

<template>
  <VSkeletonLoader v-if="loading" :loading="props.loading" type="card, text@7" width="100%" />

  <VCard v-else position="sticky">
    <VCardText class="text-center pt-15">
      <!-- 👉 Avatar -->
      <div class="avatar-with-badge-btn">
        <div class="avatar-wrapper">
          <VAvatar
            rounded
            class="main-image"
            :size="300"
            :color="!props.data.image ? 'primary' : undefined"
            :variant="!props.data.image ? 'tonal' : undefined"
            @click="openImageDialog">
            <VImg v-if="props.data.image" ref="imageDisplayRef" cover :src="props.data.square_image">
              <template #placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <VSkeletonLoader type="avatar"></VSkeletonLoader>
                </div>
              </template>
            </VImg>
            <span v-else class="text-5xl font-weight-medium">
              {{ avatarText(props.data.title) }}
            </span>
          </VAvatar>
        </div>
      </div>

      <h6 class="text-h4 mt-4">
        {{ props.data.title }}
      </h6>

      <VChip v-if="props.data.subtitle" label color="info" size="small" class="text-capitalize mt-3">
        {{ props.data.subtitle }}
      </VChip>
    </VCardText>

    <VCardText class="d-flex justify-center">
      <BatchDownloadButton :download-link="props.data?.download_link" :download-size="props.data?.download_size" />
    </VCardText>

    <VDivider />

    <!-- 👉 Details -->
    <VCardText>
      <!-- 👉 User Details list -->
      <VList class="card-list" density="compact" :lines="false">
        <DataBlock
          v-for="(item, index) in props.data.dataItems"
          :key="index"
          :item="item"
          :last="index === props.data.dataItems.length - 1" />
      </VList>
    </VCardText>

    <VDivider />

    <VCardText v-if="props.data?.comicvine_url" class="d-flex justify-start">
      <a target="_blank" rel="noopener noreferrer" :href="props.data.comicvine_url">See at ComicVine</a>
    </VCardText>
  </VCard>

  <!-- 👉 Image dialog -->
  <VDialog v-model="isImageDialogVisible" fullscreen>
    <DialogCloseBtn class="image-dialog-close-btn" @click="closeImageDialog" />
    <VCard>
      <VImg width="100%" height="100%" :src="props.data.image"></VImg>
    </VCard>
  </VDialog>
</template>

<style lang="scss" scoped>
.card-list {
  --v-card-list-gap: 0.75rem;
}

.main-image {
  cursor: pointer;
}

.image-dialog-close-btn {
  inset-block-start: 15px;
  inset-inline-end: 15px;
}
</style>
