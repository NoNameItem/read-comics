<script setup>
import { VSkeletonLoader } from "vuetify/labs/components";

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
</script>

<template>
  <VSkeletonLoader v-if="loading" :loading="props.loading" type="text@6" width="100%" />
  <VCard v-else position="sticky">
    <VCardText>
      <!-- 👉 User Details list -->
      <VList class="card-list" density="compact" :lines="false">
        <DataBlock
          v-for="(item, index) in props.data"
          :key="index"
          :item="item"
          :last="index === props.data.length - 1" />
      </VList>
    </VCardText>
  </VCard>
</template>
