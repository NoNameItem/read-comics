<script setup>
import { VSkeletonLoader } from "vuetify/labs/components";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  color: {
    type: String,
    required: false,
    default: "primary",
  },
  icon: {
    type: String,
    required: true,
  },
  stats: {
    type: String,
    required: false,
  },
  cardProps: {
    type: Object,
    required: false,
    default(_) {
      return {};
    },
  },
  statsLoading: {
    type: Boolean,
    required: false,
    default: false,
  },
});
</script>

<template>
  <VCard v-bind="props.cardProps" :loading="props.statsLoading">
    <VCardText class="d-flex align-center justify-space-between">
      <div>
        <VSkeletonLoader class="stats-skeleton-loader" type="text" :loading="props.statsLoading">
          <div class="d-flex align-center flex-wrap stats-wrapper">
            <span class="text-h5">{{ props.stats }}</span>
          </div>
        </VSkeletonLoader>
        <span class="text-body-2">{{ props.title }}</span>
      </div>

      <VAvatar :icon="props.icon" :color="props.color" :size="42" variant="tonal" />
    </VCardText>
  </VCard>
</template>

<style scoped>
:deep(.v-skeleton-loader__text) {
  margin-left: 0;
  width: 100px;
}
</style>
