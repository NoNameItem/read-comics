<script setup>
const props = defineProps({
  errorCode: {
    required: false,
    type:     String,
  },
  errorDescription: {
    required: false,
    type:     String,
  },
  errorTitle: {
    required: false,
    type:     String,
  },
})
</script>

<template>
  <div class="text-center">
    <!-- 👉 Title and subtitle -->
    <h1 v-if="props.errorCode" class="text-h1 font-weight-medium">
      {{ props.errorCode }}
    </h1>
    <h4 v-if="props.errorTitle" class="text-h4 font-weight-medium mb-3">
      {{ props.errorTitle }}
    </h4>
    <p v-if="props.errorDescription">
      {{ props.errorDescription }}
    </p>
  </div>
</template>
