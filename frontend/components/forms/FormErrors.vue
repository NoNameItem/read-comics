<template>
  <VCol v-if="$attrs['error-messages']?.length" class="pt-1 pb-1" cols="12">
    <VInput
      v-bind="{
        ...$attrs,
      }"
      :error="false"
      max-errors="100"
    />
  </VCol>
</template>
