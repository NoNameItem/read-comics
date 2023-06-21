<script setup>
import { useBreadcrumbsStore } from "@/stores/breadcrumbs";
import { VSkeletonLoader } from "vuetify/labs/components";

const breadcrumbs = useBreadcrumbsStore();
</script>

<template>
  <VSkeletonLoader class="breadcrumb-loader" type="text" :loading="breadcrumbs.loading">
    <VBreadcrumbs v-if="!breadcrumbs.loading" :items="breadcrumbs.fullBreadcrumbs">
      <template #prepend>
        <span class="page-title">{{ breadcrumbs.pageTitle }}</span>
      </template>

      <template #title="{ item }">
        <VIcon v-if="item.icon" :icon="item.icon"></VIcon>
        <span v-else>{{ item.title }}</span>
      </template>
    </VBreadcrumbs>
  </VSkeletonLoader>
</template>

<style lang="scss" scoped>
.page-title {
  border-right: 1px solid #828d99;
  padding-right: 1rem;
  margin-right: 1rem;
  font-weight: 800;
}

.breadcrumb-loader {
  background: rgb(var(--v-theme-background));
}
</style>
