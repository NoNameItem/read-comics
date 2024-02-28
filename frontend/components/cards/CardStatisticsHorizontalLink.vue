<script setup>
import { VSkeletonLoader } from "vuetify/labs/components"

const props = defineProps({
  cardProps: {
    default(_) {
      return {}
    },
    required: false,
    type:     Object,
  },
  color: {
    default:  "primary",
    required: false,
    type:     String,
  },
  icon: {
    required: true,
    type:     String,
  },
  stats: {
    required: false,
    type:     String,
  },
  statsLoading: {
    default:  false,
    required: false,
    type:     Boolean,
  },
  title: {
    required: true,
    type:     String,
  },
})
</script>

<template>
  <VCard v-bind="props.cardProps" :loading="props.statsLoading">
    <VCardText class="d-flex align-center justify-space-between">
      <div>
        <VSkeletonLoader :loading="props.statsLoading" class="stats-skeleton-loader" type="text">
          <div class="d-flex align-center flex-wrap stats-wrapper">
            <span class="text-h5">{{ props.stats }}</span>
          </div>
        </VSkeletonLoader>
        <span class="text-body-2">{{ props.title }}</span>
      </div>

      <VAvatar :color="props.color" :icon="props.icon" :size="42" variant="tonal" />
    </VCardText>
  </VCard>
</template>

<style scoped>
:deep(.v-skeleton-loader__text) {
  margin-left: 0;
  width: 100px;
}
</style>
