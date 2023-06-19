<script setup>
import { useBreadcrumbsStore } from "@/stores/breadcrumbs";
import { useQuery } from "@tanstack/vue-query";
import { queries } from "@/queries";

const route = useRoute();

const breadcrumb = useBreadcrumbsStore();

// Tabs
//---------------------------------------------------------
const tabs = [
  {
    icon: "fasl:circle-info",
    title: "Info",
  },
];

const activeTab = ref(null);

const { isLoading: infoLoading, data: info } = useQuery(queries.locations.detail(route.params.slug));

const setBreadcrumbs = () => {
  if (!infoLoading.value) {
    breadcrumb.setBreadcrumbs(info.value.name, [
      {
        title: "Locations",
        to: "/locations",
      },
      { title: info.value.name },
    ]);
  }
};

setBreadcrumbs();

watch([infoLoading, info], () => {
  setBreadcrumbs();
});

const preparedInfo = computed(() => ({
  title: info.value?.name,
  image: info.value?.image,
  square_image: info.value?.square_image,
  download_link: info.value?.download_link,
  download_size: info.value?.download_size,
  comicvine_url: info.value?.comicvine_url,
  dataItems: [
    {
      title: "Aliases",
      valueList: info.value?.aliases,
    },
    {
      title: "Start year",
      value: info.value?.start_year,
    },
    {
      title: "First Issue",
      value: info.value?.first_issue_name,
      to: info.value?.first_issue_slug ? `/issues/${info.value?.first_issue_slug}` : null,
    },
  ],
}));

const description = computed(() => info.value?.description || info.value?.short_description);

// Technical info
//---------------------------------------------------------

const { isLoading: technicalInfoLoading, preparedTechnicalInfo } = usePreparedTechnicalInfo(
  queries.locations.detail(route.params.slug)._ctx.technicalInfo
);
</script>

<template>
  <VRow>
    <VCol cols="12" md="5" lg="4" xl="3" xxl="2">
      <DBInfoFlipper
        :info="preparedInfo"
        :info-loading="infoLoading"
        :technical-info-loading="technicalInfoLoading"
        :technical-info="preparedTechnicalInfo" />
    </VCol>
    <VCol cols="12" md="7" lg="8" xl="9" xxl="10">
      <VTabs v-model="activeTab" class="v-tabs-pill">
        <VTab v-for="tab in tabs" :key="tab.icon">
          <VIcon :size="18" :icon="tab.icon" class="me-1" />
          <span>{{ tab.title }}</span>
        </VTab>
      </VTabs>

      <VWindow v-model="activeTab" class="mt-6 fullscreen" :touch="false">
        <VWindowItem>
          <DBDescriptionTab :loading="infoLoading" :description="description" />
        </VWindowItem>
      </VWindow>
    </VCol>
  </VRow>
</template>

<route lang="json">
{ "meta": { "navActiveLink": "locations" } }
</route>
