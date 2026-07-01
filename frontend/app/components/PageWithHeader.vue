<!-- Docs: [[docs/frontend/components/PageWithHeader.md]] -->
<script setup lang="ts">
const breadcrumb = useBreadcrumbsStore()
</script>

<template>
  <UDashboardPanel id="home">
    <template #header>
      <UDashboardNavbar
        :title="breadcrumb.pageTitle"
        :ui="{ right: 'gap-3', title: 'text-primary text-lg' }"
      >
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>
        <template #trailing>
          <UBreadcrumb
            :items="breadcrumb.fullBreadcrumbs"
            class="border-l-primary border-l-2 pl-2"
          />
        </template>
        <template #right>
          <UColorModeSelect />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <slot />
    </template>
  </UDashboardPanel>
</template>
