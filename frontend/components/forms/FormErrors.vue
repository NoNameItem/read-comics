<template>
  <VCol v-if="$attrs['error-messages']?.length" cols="12" class="pt-1 pb-1">
    <VInput
      v-bind="{
        ...$attrs,
      }"
      :error="false"
      max-errors="100">
    </VInput>
  </VCol>
</template>
