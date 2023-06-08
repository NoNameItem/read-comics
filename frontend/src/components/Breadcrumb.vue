<script setup>
import { useBreadcrumbsStore } from "@/stores/breadcrumbs";

const breadcrumbs = useBreadcrumbsStore();
</script>

<template>
  <VBreadcrumbs :items="breadcrumbs.fullBreadcrumbs">
    <template #prepend>
      <span class="page-title">{{ breadcrumbs.pageTitle }}</span>
    </template>

    <template #title="{ item }">
      <VIcon v-if="item.icon" :icon="item.icon"></VIcon>
      <span v-else>{{ item.title }}</span>
    </template>
  </VBreadcrumbs>
</template>

<style scoped>
.page-title {
  border-right: 1px solid #828d99;
  padding-right: 1rem;
  margin-right: 1rem;
  font-weight: 800;
}
</style>
