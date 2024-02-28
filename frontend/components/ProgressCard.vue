<script setup>
import { VSkeletonLoader } from "vuetify/labs/components"

const props = defineProps({
  current: {
    required: false,
    type:     Number,
  },
  delta: {
    default:  0,
    required: false,
    type:     Number,
  },
  loading: {
    default:  false,
    required: false,
    type:     Boolean,
  },
  title: {
    default:  "",
    required: false,
    type:     String,
  },
  total: {
    required: false,
    type:     Number,
  },
})

const percentage = computed(() => Math.ceil((props.current / props.total) * 100))

const color = computed(() => {
  if (percentage.value < 35) { return "error" }

  if (percentage.value < 65) { return "warning" }

  return "success"
})
</script>

<template>
  <VCard :loading="props.loading">
    <VCardItem>
      <VCardTitle>
        {{ props.title }}
        <VChip
          v-if="props.delta > 0"
          color="success"
        >
          +{{ props.delta }}
        </VChip>
      </VCardTitle>
    </VCardItem>
    <VCardText>
      <VSkeletonLoader
        :loading="props.loading"
        type="text"
      >
        <VProgressLinear
          :bg-color="color"
          :color="color"
          :model-value="percentage"
          height="20"
        >
          <strong>{{ current.toLocaleString('en-US') }} / {{ total.toLocaleString('en-US') }}</strong>
        </VProgressLinear>
      </VSkeletonLoader>
    </VCardText>
  </VCard>
</template>
