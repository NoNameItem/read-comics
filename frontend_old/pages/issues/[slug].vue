<script setup>
import { queries } from "@/queries"
import { useBreadcrumbsStore } from "@/stores/breadcrumbs"
import { useQuery } from "@tanstack/vue-query"
import { onServerPrefetch, watch } from "vue"

definePageMeta({ navActiveLink: "issues" })

const route = useRoute()

const breadcrumb = useBreadcrumbsStore()

// Tabs
// ---------------------------------------------------------
const tabs = [
  {
    icon:  "fasl:circle-info",
    title: "Info",
  },
]

const activeTab = ref(null)

// Info
// ---------------------------------------------------------

const addOrdering = issueLink =>
  route.query?.ordering ? `${issueLink}?ordering=${route.query.ordering}` : issueLink

const { data: info, isPending: infoLoading, suspense } = useQuery(
  queries.issues.detail(
    route.params.slug,
    route.query?.ordering ?? "cover_date,volume__name,volume__start_year,numerical_number,number",
  ),
)

useServerSeoMeta({
  title: () => `[${info.value.number_in_sublist.toLocaleString()} / ${info.value.total_in_sublist.toLocaleString("en-us")}] ${
    info.value.volume?.display_name
  } #${info.value.number}`,
})

const setBreadcrumbs = () => {
  if (!infoLoading.value) {
    breadcrumb.setBreadcrumbs(
      `[${info.value.number_in_sublist.toLocaleString()} / ${info.value.total_in_sublist.toLocaleString("en-us")}] ${
        info.value.volume?.display_name
      } #${info.value.number}`,
      [
        {
          title: "Issues",
          to:    addOrdering("/issues"),
        },
        { title: `${info.value.volume?.display_name} #${info.value.number}` },
      ],
    )
  }
}

setBreadcrumbs()

onServerPrefetch(async () => {
  await suspense()
  setBreadcrumbs()
})

watch([infoLoading, info], () => {
  setBreadcrumbs()
})

const preparedInfo = computed(() => ({
  comicvine_url: info.value?.comicvine_url,
  dataItems:     [
    {
      title: "Volume",
      to:    `/volumes/${info.value?.volume?.slug}`,
      value: info.value?.volume?.display_name,
    },
    {
      title: "Publisher",
      to:    `/publishers/${info.value?.publisher?.slug}`,
      value: info.value?.publisher?.name,
    },
    {
      html:  `${info.value?.number} <small>(of ${info.value?.volume_last_number})</small>`,
      title: "Number",
    },
    {
      title: "Cover Date",
      value: utilsFormatDate(info.value?.cover_date),
    },
    {
      title: "Store Date",
      value: utilsFormatDate(info.value?.store_date),
    },
  ],
  download_link: info.value?.download_link,
  download_size: info.value?.download_size,
  image:         info.value?.image,
  isFinished:    info.value?.is_finished,
  nextLink:      info.value?.next_issue_slug ? addOrdering(`/issues/${info.value.next_issue_slug}`) : null,
  prevLink:      info.value?.prev_issue_slug ? addOrdering(`/issues/${info.value.prev_issue_slug}`) : null,
  square_image:  info.value?.square_image,
  subtitle:      info.value?.name,
  title:         `${info.value?.volume?.display_name} #${info.value?.number}`,
}))

const description = computed(() => info.value?.description || info.value?.short_description)

// Technical info
// ---------------------------------------------------------

const { isPending: technicalInfoLoading, preparedTechnicalInfo } = usePreparedTechnicalInfo(
  queries.issues.detail(route.params.slug)._ctx.technicalInfo,
)
</script>

<template>
  <PageWithBreadcrumb>
    <VRow>
      <VCol
        cols="12"
        lg="4"
        md="5"
        xl="3"
        xxl="2"
      >
        <DBInfoFlipper
          :batch-download="false"
          :info="preparedInfo"
          :info-loading="infoLoading"
          :technical-info="preparedTechnicalInfo"
          :technical-info-loading="technicalInfoLoading"
          show-prev-next-buttons
        />
      </VCol>
      <VCol
        cols="12"
        lg="8"
        md="7"
        xl="9"
        xxl="10"
      >
        <VTabs
          v-model="activeTab"
          class="v-tabs-pill"
        >
          <VTab
            v-for="(tab, index) in tabs"
            :key="index"
            :value="index"
          >
            <VIcon
              :icon="tab.icon"
              :size="18"
              class="me-1"
            />
            <span>{{ tab.title }}</span>
          </VTab>
        </VTabs>

        <VWindow
          v-model="activeTab"
          :touch="false"
          class="mt-6 fullscreen"
        >
          <VWindowItem>
            <DBDescriptionTab
              :description="description"
              :loading="infoLoading"
            />
          </VWindowItem>
        </VWindow>
      </VCol>
    </VRow>
  </PageWithBreadcrumb>
</template>
