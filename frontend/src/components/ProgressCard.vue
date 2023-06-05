<script setup>
import { VSkeletonLoader } from "vuetify/labs/components";

const props = defineProps({
  title: {
    type: String,
    required: false,
    default: "",
  },
  current: {
    type: Number,
    required: false,
  },
  delta: {
    type: Number,
    required: false,
    default: 0,
  },
  total: {
    type: Number,
    required: false,
  },
  loading: {
    type: Boolean,
    required: false,
    default: false,
  },
});

const percentage = computed(() => Math.ceil((props.current / props.total) * 100));

const color = computed(() => {
  if (percentage.value < 35) {
    return "error";
  }
  if (percentage.value < 65) {
    return "warning";
  }
  return "success";
});
</script>

<template>
  <VCard :loading="props.loading">
    <VCardItem>
      <VCardTitle>
        {{ props.title }}
        <VChip v-if="props.delta > 0" color="success"> +{{ props.delta }}</VChip>
      </VCardTitle>
    </VCardItem>
    <VCardText>
      <VSkeletonLoader :loading="props.loading" type="text">
        <VProgressLinear height="20" :model-value="percentage" :color="color" :bg-color="color">
          <strong>{{ current.toLocaleString() }} / {{ total.toLocaleString() }}</strong>
        </VProgressLinear>
      </VSkeletonLoader>
    </VCardText>
  </VCard>
</template>
