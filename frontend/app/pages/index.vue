<!-- Docs: [[docs/frontend/pages/index.md]] -->
<script setup lang="ts">
const breadcrumb = useBreadcrumbsStore()
useServerSeoMeta({ title: 'Read Comics' })
breadcrumb.setBreadcrumbs('Read Comics', [])
</script>

<template>
  <PageWithHeader>
    <p>Home</p>
  </PageWithHeader>
</template>
