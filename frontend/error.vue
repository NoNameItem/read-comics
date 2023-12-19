<script setup>
import pages500 from "@images/pages/500.jpg"

definePageMeta({
  layout: "blank",
})

useHead({ title: "Server error" })
</script>

<template>
  <div class="misc-wrapper">
    <!-- 👉 Image -->
    <div class="misc-avatar w-100 text-center">
      <VImg
        :src="pages500"
        alt="Coming Soon"
        :max-width="600"
        class="mx-auto"
      />
    </div>

    <ErrorHeader
      error-title="Internal server error 👨🏻‍💻"
      error-description="Oops, something went wrong!"
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
