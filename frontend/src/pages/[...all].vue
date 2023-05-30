<script setup>
import { useGenerateImageVariant } from "@core/composable/useGenerateImageVariant";
import misc404 from "@images/pages/404.jpg";
import miscMaskDark from "@images/pages/misc-mask-dark.png";
import miscMaskLight from "@images/pages/misc-mask-light.png";

const authThemeMask = useGenerateImageVariant(miscMaskLight, miscMaskDark);
</script>

<template>
  <div class="misc-wrapper">
    <!-- 👉 Image -->
    <div class="misc-avatar w-100 text-center">
      <VImg :src="misc404" alt="Coming Soon" :max-width="600" class="mx-auto" />
    </div>

    <ErrorHeader
      class=""
      error-title="Page Not Found :("
      error-description="We couldn't find the page you are looking for." />
    <VBtn to="/" class="mb-12"> Back to Home </VBtn>
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
  action: read
  subject: Auth
</route>
