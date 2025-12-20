<script setup>
import pages500 from "@images/pages/500.jpg"

definePageMeta({ layout: "blank" })

useHead({ title: "Server error" })
</script>

<template>
  <div class="misc-wrapper">
    <!-- 👉 Image -->
    <div class="misc-avatar w-100 text-center">
      <VImg
        :max-width="600"
        :src="pages500"
        alt="Coming Soon"
        class="mx-auto"
      />
    </div>

    <ErrorHeader
      error-description="Oops, something went wrong!"
      error-title="Internal server error 👨🏻‍💻"
    />
    <VBtn to="/">
      Back to Home
    </VBtn>
  </div>
</template>

<style lang="scss">
@use "@core/scss/template/pages/misc.scss";

.misc-avatar {
  margin-bottom: 30px;
}
</style>

<route lang="yaml">
meta:
layout: blank
</route>
