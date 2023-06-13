<script setup>
import { VSkeletonLoader } from "vuetify/labs/VSkeletonLoader";

const props = defineProps({
  loading: {
    type: Boolean,
    required: false,
  },
  description: {
    type: String,
    required: false,
  },
});
</script>

<template>
  <VSkeletonLoader class="detail-full-description-loader" type="paragraph" :loading="props.loading">
    <p class="detail-full-description" v-html="props.description"></p>
  </VSkeletonLoader>
</template>

<style lang="scss">
.detail-full-description-loader {
  background: rgb(var(--v-theme-background));
}

.detail-full-description figure {
  margin: 0 2rem 2rem 0;
  width: fit-content !important;
  max-width: 250px;
  float: left;
  clear: both;
}

.detail-full-description figure img {
  width: 100%;
}

.detail-full-description figure figcaption {
  clear: both;
  display: block;
  font-family: Georgia, serif;
  font-style: oblique;
  text-align: center;
}

.detail-full-description h2 {
  margin-bottom: 20px;
  padding-bottom: 5px;
  border-bottom: 1px solid #bfbfbf;
  font-size: 2.13rem;
}

.detail-full-description h3 {
  font-size: 1.73rem;
}

.detail-full-description ul,
.detail-full-description ol {
  padding-inline-start: 40px;
}

.detail-full-description h2,
.detail-full-description h3,
.detail-full-description h4 {
  clear: both;
}
</style>
