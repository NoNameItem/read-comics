<script setup>
import TotalProgress from "@/views/home/TotalProgress.vue";
import { useUserStore } from "@/stores/user";
import StatisticCards from "@/views/home/HomeStatistics.vue";
import StartedAndNotFinished from "@/views/home/StartedAndNotFinished.vue";
import { useBreadcrumbsStore } from "@/stores/breadcrumbs";

const user = useUserStore();
const breadcrumb = useBreadcrumbsStore();

breadcrumb.setBreadcrumbs("Home", []);
</script>

<template>
  <div>
    <VRow>
      <VCol v-if="user.loggedIn" col="12">
        <TotalProgress />
      </VCol>
    </VRow>

    <VRow v-if="user.loggedIn">
      <VCol col="12" md="6">
        <StartedAndNotFinished query-name="volumes.started" card-url-base="volumes" title="volumes" />
      </VCol>
      <VCol col="12" md="6">
        <StartedAndNotFinished query-name="storyArcs.started" card-url-base="story-arcs" title="story arcs" />
      </VCol>
    </VRow>

    <StatisticCards />
  </div>
</template>
