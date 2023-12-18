<script setup>
import { VSkeletonLoader } from 'vuetify/labs/components'
import { useBreadcrumbsStore } from '@/stores/breadcrumbs'

const breadcrumbs = useBreadcrumbsStore()
</script>

<template>
  <ClientOnly>
    <VSkeletonLoader
      class="breadcrumb-loader"
      type="text"
      :loading="breadcrumbs.loading"
    >
      <VBreadcrumbs
        v-if="!breadcrumbs.loading"
        :items="breadcrumbs.fullBreadcrumbs"
      >
        <template #prepend>
          <span class="page-title">{{ breadcrumbs.pageTitle }}</span>
        </template>

        <template #title="{ item }">
          <VIcon
            v-if="item.icon"
            :icon="item.icon"
          />
          <span v-else>{{ item.title }}</span>
        </template>
      </VBreadcrumbs>
    </VSkeletonLoader>
    <!--    <template #fallback> -->
    <!--      <VSkeletonLoader -->
    <!--        class="breadcrumb-loader" -->
    <!--        type="text" -->
    <!--        :loading="true" -->
    <!--      /> -->
    <!--    </template> -->
    <template #fallback>
      <VBreadcrumbs
        v-if="!breadcrumbs.loading"
        :items="breadcrumbs.fullBreadcrumbs"
      >
        <template #prepend>
          <span class="page-title">{{ breadcrumbs.pageTitle }}</span>
        </template>

        <template #title="{ item }">
          <VIcon
            v-if="item.icon"
            :icon="item.icon"
          />
          <span v-else>{{ item.title }}</span>
        </template>
      </VBreadcrumbs>
    </template>
  </ClientOnly>
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
