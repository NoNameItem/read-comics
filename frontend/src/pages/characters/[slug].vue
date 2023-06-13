<script setup>
import { useBreadcrumbsStore } from "@/stores/breadcrumbs";
import { useQuery } from "@tanstack/vue-query";
import { queries } from "@/queries";
import { formatDate } from "@/utils/format_utils";

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

// Info
//---------------------------------------------------------

const { isLoading: infoLoading, data: info } = useQuery(queries.characters.detail(route.params.slug));

breadcrumb.setBreadcrumbs(info.value?.name ?? route.params.slug, [
  {
    title: "Characters",
    to: "/characters/",
  },
  { title: info.value?.name ?? route.params.slug },
]);

watch([infoLoading, info], () => {
  if (!infoLoading.value) {
    breadcrumb.setBreadcrumbs(info.value.name, [
      {
        title: "Characters",
        to: "/characters/",
      },
      { title: info.value.name },
    ]);
  }
});

const preparedInfo = computed(() => ({
  title: info.value?.name,
  image: info.value?.image,
  square_image: info.value?.square_image,
  subtitle: info.value?.real_name,
  download_link: info.value?.download_link,
  download_size: info.value?.download_size,
  comicvine_url: info.value?.comicvine_url,
  dataItems: [
    {
      title: "Publisher",
      value: info.value?.publisher?.name,
      to: `/publishers/${info.value?.publisher?.slug}`,
    },
    {
      title: "Aliases",
      valueList: info.value?.aliases,
    },
    {
      title: "Birth date",
      value: formatDate(info.value?.birth),
    },
    {
      title: "Gender",
      value: info.value?.gender,
    },
    {
      title: "Powers",
      valueList: info.value?.powers,
    },
    {
      title: "First Issue",
      value: info.value?.first_issue_name,
      to: info.value?.first_issue_slug ? `/issues/${info.value?.first_issue_slug}` : null,
    },
  ],
}));

// Technical info
//---------------------------------------------------------

const { isLoading: technicalInfoLoading, preparedTechnicalInfo } = usePreparedTechnicalInfo(
  queries.characters.detail(route.params.slug)._ctx.technicalInfo
);
</script>

<template>
  <div>
    <Breadcrumb :loading="infoLoading" />
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
            <DBDescriptionTab :loading="infoLoading" :description="info?.description" />
          </VWindowItem>
        </VWindow>
      </VCol>
    </VRow>
  </div>
</template>
