<script setup>
import AppSearchHeaderBg from "@images/pages/app-search-header-bg.png"

defineOptions({ inheritAttrs: false })

const props = defineProps({
  customClass: {
    required: false,
    type:     String,
  },
  subtitle: {
    required: false,
    type:     String,
  },
  title: {
    required: false,
    type:     String,
  },
})
</script>

<template>
  <!-- 👉 Search Banner  -->
  <VCard
    :class="props.customClass"
    :style="`background: url(${AppSearchHeaderBg});`"
    class="text-center search-header"
    flat
  >
    <VCardText>
      <h5 class="text-h3 font-weight-medium">
        {{ props.title }}
      </h5>

      <!-- 👉 Search Input -->
      <AppTextField
        v-bind="$attrs"
        class="search-header-input mx-auto my-3"
        density="comfortable"
        placeholder="Search a question..."
      >
        <template #prepend-inner>
          <VIcon icon="tabler-search" size="23" />
        </template>
      </AppTextField>

      <p class="mb-0">
        {{ props.subtitle }}
      </p>
    </VCardText>
  </VCard>
</template>

<style lang="scss">
.search-header {
  padding: 4rem !important;
  background-size: cover !important;
}

// search input
.search-header-input {
  border-radius: 0.25rem !important;
  border-radius: 0.375rem !important;
  background-color: rgb(var(--v-theme-surface));
  max-inline-size: 40.125rem !important;

  .v-field__prepend-inner {
    i {
      inset-block-start: 3px !important;
    }
  }
}

@media (max-width: 37.5rem) {
  .search-header {
    padding: 1.5rem !important;
  }
}
</style>
