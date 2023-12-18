<script setup>
import TotalProgress from '@/views/home/TotalProgress.vue'
import { useUserStore } from '@/stores/user'
import { useBreadcrumbsStore } from '@/stores/breadcrumbs'

const user = useUserStore()
const breadcrumb = useBreadcrumbsStore()

useServerSeoMeta({
  title: 'Home',
})

breadcrumb.setBreadcrumbs('Home', [])
</script>

<template>
  <PageWithBreadcrumb>
    <VRow>
      <VCol
        v-if="user.loggedIn"
        col="12"
      >
        <TotalProgress />
      </VCol>
    </VRow>

    <VRow v-if="user.loggedIn">
      <VCol
        col="12"
        md="6"
      >
        <StartedAndNotFinished
          query-name="volumes.started"
          card-url-base="volumes"
          title="volumes"
        />
      </VCol>
      <VCol
        col="12"
        md="6"
      >
        <StartedAndNotFinished
          query-name="storyArcs.started"
          card-url-base="story-arcs"
          title="story arcs"
        />
      </VCol>
    </VRow>

    <HomeStatistics />
  </PageWithBreadcrumb>
</template>
