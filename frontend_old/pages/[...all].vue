<script setup>
import misc404 from "@images/pages/404.jpg"

definePageMeta({ layout: "blank" })

useHead({ title: "Page not found" })
</script>

<template>
  <div class="misc-wrapper">
    <!-- 👉 Image -->
    <div class="misc-avatar w-100 text-center">
      <VImg
        :max-width="600"
        :src="misc404"
        alt="Coming Soon"
        class="mx-auto"
      />
    </div>

    <ErrorHeader
      class=""
      error-description="We couldn't find the page you are looking for."
      error-title="Page Not Found :("
    />
    <VBtn
      class="mb-12"
      to="/"
    >
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

<route lang="json">
{ "meta": { "layout": "blank" } }
</route>
