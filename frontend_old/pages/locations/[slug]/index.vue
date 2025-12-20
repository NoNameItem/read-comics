<script setup>
import { queries } from "@/queries"
import { useBreadcrumbsStore } from "@/stores/breadcrumbs"
import { useQuery } from "@tanstack/vue-query"
import PageWithBreadcrumb from "~/components/PageWithBreadcrumb.vue"
import { onServerPrefetch } from "vue"

definePageMeta({ navActiveLink: "locations" })

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

const { data: info, isPending: infoLoading, suspense } = useQuery(queries.locations.detail(route.params.slug))

const setBreadcrumbs = () => {
  if (!infoLoading.value) {
    breadcrumb.setBreadcrumbs(info.value.name, [
      {
        title: "Locations",
        to:    "/locations",
      },
      { title: info.value.name },
    ])
  }
}

setBreadcrumbs()

useServerSeoMeta({ title: () => info.value.name })

watch([infoLoading, info], () => {
  setBreadcrumbs()
})

onServerPrefetch(async () => {
  await suspense()
  setBreadcrumbs()
})

const preparedInfo = computed(() => ({
  comicvine_url: info.value?.comicvine_url,
  dataItems:     [
    {
      title:     "Aliases",
      valueList: info.value?.aliases,
    },
    {
      title: "Start year",
      value: info.value?.start_year,
    },
    {
      title: "First Issue",
      to:    info.value?.first_issue_slug ? `/issues/${info.value?.first_issue_slug}` : null,
      value: info.value?.first_issue_name,
    },
  ],
  download_link: info.value?.download_link,
  download_size: info.value?.download_size,
  image:         info.value?.image,
  square_image:  info.value?.square_image,
  title:         info.value?.name,
}))

const description = computed(() => info.value?.description || info.value?.short_description)

// Technical info
// ---------------------------------------------------------

const { isPending: technicalInfoLoading, preparedTechnicalInfo } = usePreparedTechnicalInfo(
  queries.locations.detail(route.params.slug)._ctx.technicalInfo,
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
          :info="preparedInfo"
          :info-loading="infoLoading"
          :technical-info="preparedTechnicalInfo"
          :technical-info-loading="technicalInfoLoading"
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
            v-for="tab in tabs"
            :key="tab.icon"
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
