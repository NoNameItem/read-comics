<script setup>
import { VSkeletonLoader } from "vuetify/labs/components"

const props = defineProps({
  data: {
    required: false,
    type:     Object,
  },
  loading: {
    default:  true,
    required: false,
    type:     Boolean,
  },
})
</script>

<template>
  <VSkeletonLoader v-if="loading" :loading="props.loading" type="text@6" width="100%" />
  <VCard v-else position="sticky">
    <VCardText>
      <!-- 👉 User Details list -->
      <VList :lines="false" class="card-list" density="compact">
        <DataBlock
          v-for="(item, index) in props.data"
          :key="index"
          :item="item"
          :last="index === props.data.length - 1"
        />
      </VList>
    </VCardText>
  </VCard>
</template>
