<script setup>
import { avatarText } from "@core/utils/formatters"
import { VSkeletonLoader } from "vuetify/labs/VSkeletonLoader"

const props = defineProps({
  batchDownload: {
    default:  true,
    required: false,
    type:     Boolean,
  },
  data: {
    required: false,
    type:     Object,
  },
  loading: {
    default:  true,
    required: false,
    type:     Boolean,
  },
  showPrevNextButtons: {
    default:  false,
    required: false,
    type:     Boolean,
  },
})

const isImageDialogVisible = ref(false)

const openImageDialog = () => {
  isImageDialogVisible.value = true
}

const closeImageDialog = () => {
  isImageDialogVisible.value = false
}
</script>

<template>
  <VSkeletonLoader v-if="loading" :loading="props.loading" type="card, text@7" width="100%" />

  <VCard v-else position="sticky">
    <VCardText class="text-center pt-15">
      <VBadge :model-value="!!props.data.isFinished" color="success" icon="fasl:check">
        <VAvatar
          :color="!props.data.image ? 'primary' : undefined"
          :size="300"
          :variant="!props.data.image ? 'tonal' : undefined"
          class="main-image"
          rounded
          @click="openImageDialog"
        >
          <VImg v-if="props.data.image" :src="props.data.square_image" cover>
            <template #placeholder>
              <div class="d-flex align-center justify-center fill-height">
                <VSkeletonLoader type="avatar" />
              </div>
            </template>
          </VImg>
          <span v-else class="text-5xl font-weight-medium">
            {{ avatarText(props.data.title) }}
          </span>
        </VAvatar>
      </VBadge>

      <h6 class="text-h4 mt-4">
        {{ props.data.title }}
      </h6>

      <VChip v-if="props.data.subtitle" class="text-capitalize mt-3" color="info" label size="small">
        {{ props.data.subtitle }}
      </VChip>
    </VCardText>

    <VCardText class="d-flex justify-center">
      <VBtn
        v-if="props.showPrevNextButtons"
        :disabled="!props.data?.prevLink"
        :to="props.data?.prevLink"
        class="mr-1"
        size="38"
      >
        <VIcon icon="fasl:chevron-left" size="22" />
      </VBtn>
      <BatchDownloadButton
        v-if="props.batchDownload"
        :download-link="props.data?.download_link"
        :download-size="props.data?.download_size"
      />
      <VBtn v-else color="info" v-bind="props" :href="props.data?.download_link">
        <VIcon icon="fasl:download" start />
        Download ({{ props.data?.download_size }})
      </VBtn>
      <VBtn
        v-if="props.showPrevNextButtons"
        :disabled="!props.data?.nextLink"
        :to="props.data?.nextLink"
        class="ml-1"
        size="38"
      >
        <VIcon icon="fasl:chevron-right" size="22" />
      </VBtn>
    </VCardText>

    <VDivider />

    <!-- 👉 Details -->
    <VCardText>
      <!-- 👉 User Details list -->
      <VList :lines="false" class="card-list" density="compact">
        <DataBlock
          v-for="(item, index) in props.data.dataItems"
          :key="index"
          :item="item"
          :last="index === props.data.dataItems.length - 1"
        />
      </VList>
    </VCardText>

    <VDivider />

    <VCardText v-if="props.data?.comicvine_url" class="d-flex justify-start">
      <a :href="props.data.comicvine_url" rel="noopener noreferrer" target="_blank">See at ComicVine</a>
    </VCardText>
  </VCard>

  <!-- 👉 Image dialog -->
  <VDialog v-model="isImageDialogVisible" fullscreen>
    <DialogCloseBtn class="image-dialog-close-btn" @click="closeImageDialog" />
    <VCard>
      <VImg :src="props.data.image" height="100%" width="100%" />
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
