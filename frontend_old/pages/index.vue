<script setup>
import { useBreadcrumbsStore } from "@/stores/breadcrumbs"
import { useUserStore } from "@/stores/user"
import TotalProgress from "@/views/home/TotalProgress.vue"

const user = useUserStore()
const breadcrumb = useBreadcrumbsStore()

useServerSeoMeta({ title: "Home" })

breadcrumb.setBreadcrumbs("Home", [])
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
          card-url-base="volumes"
          query-name="volumes.started"
          title="volumes"
        />
      </VCol>
      <VCol
        col="12"
        md="6"
      >
        <StartedAndNotFinished
          card-url-base="story-arcs"
          query-name="storyArcs.started"
          title="story arcs"
        />
      </VCol>
    </VRow>

    <HomeStatistics />
  </PageWithBreadcrumb>
</template>
