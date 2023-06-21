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

const addOrdering = (issueLink) =>
  route.query?.ordering ? `${issueLink}?ordering=${route.query.ordering}` : issueLink;

const { isLoading: infoLoading, data: info } = useQuery(
  queries.issues.detail(
    route.params.slug,
    route.query?.ordering ?? "cover_date,volume__name,volume__start_year,numerical_number,number"
  )
);

const setBreadcrumbs = () => {
  if (!infoLoading.value) {
    breadcrumb.setBreadcrumbs(
      `[${info.value.number_in_sublist.toLocaleString()} / ${info.value.total_in_sublist.toLocaleString()}] ${
        info.value.volume?.display_name
      } #${info.value.number}`,
      [
        {
          title: "Issues",
          to: addOrdering("/issues"),
        },
        { title: `${info.value.volume?.display_name} #${info.value.number}` },
      ]
    );
  }
};

setBreadcrumbs();

watch([infoLoading, info], () => {
  setBreadcrumbs();
});

const preparedInfo = computed(() => ({
  title: `${info.value?.volume?.display_name} #${info.value?.number}`,
  subtitle: info.value?.name,
  image: info.value?.image,
  square_image: info.value?.square_image,
  download_link: info.value?.download_link,
  download_size: info.value?.download_size,
  comicvine_url: info.value?.comicvine_url,
  isFinished: info.value?.is_finished,
  prevLink: info.value?.prev_issue_slug ? addOrdering(`/issues/${info.value.prev_issue_slug}`) : null,
  nextLink: info.value?.next_issue_slug ? addOrdering(`/issues/${info.value.next_issue_slug}`) : null,
  dataItems: [
    {
      title: "Volume",
      value: info.value?.volume?.display_name,
      to: `/volumes/${info.value?.volume?.slug}`,
    },
    {
      title: "Publisher",
      value: info.value?.publisher?.name,
      to: `/publishers/${info.value?.publisher?.slug}`,
    },
    {
      title: "Number",
      html: `${info.value?.number} <small>(of ${info.value?.volume_last_number})</small>`,
    },
    {
      title: "Cover Date",
      value: formatDate(info.value?.cover_date),
    },
    {
      title: "Store Date",
      value: formatDate(info.value?.store_date),
    },
  ],
}));

const description = computed(() => info.value?.description || info.value?.short_description);

// Technical info
//---------------------------------------------------------

const { isLoading: technicalInfoLoading, preparedTechnicalInfo } = usePreparedTechnicalInfo(
  queries.issues.detail(route.params.slug)._ctx.technicalInfo
);
</script>

<template>
  <VRow>
    <VCol cols="12" md="5" lg="4" xl="3" xxl="2">
      <DBInfoFlipper
        :info="preparedInfo"
        :info-loading="infoLoading"
        :technical-info-loading="technicalInfoLoading"
        :technical-info="preparedTechnicalInfo"
        :batch-download="false"
        show-prev-next-buttons />
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
{ "meta": { "navActiveLink": "issues" } }
</route>
