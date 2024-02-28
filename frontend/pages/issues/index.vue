<script setup>
import { useGetListData } from "@/composables/useGetListData"
import { queries } from "@/queries"
import { useBreadcrumbsStore } from "@/stores/breadcrumbs"
import { DateTime } from "luxon"
import { computed, onServerPrefetch } from "vue"

useServerSeoMeta({ title: "Issues" })

const breadcrumb = useBreadcrumbsStore()

breadcrumb.setBreadcrumbs("Issues", [{ title: "Issues" }])

const orderingVariants = [
  {
    icon:  "fasl:arrow-down-a-z",
    title: "Name",
    value: "volume__name,volume__start_year,numerical_number,number",
  },
  {
    icon:  "fasl:arrow-down-z-a",
    title: "Name",
    value: "-volume__name,-volume__start_year,-numerical_number,-number",
  },
  {
    icon:  "fasl:arrow-down-1-9",
    title: "Cover date",
    value: "cover_date,volume__name,volume__start_year,numerical_number,number",
  },
  {
    icon:  "fasl:arrow-down-9-1",
    title: "Cover date",
    value: "-cover_date,-volume__name,-volume__start_year,-numerical_number,-number",
  },
]

const defaultOrdering = "cover_date,volume__name,volume__start_year,numerical_number,number"

const { data, isPending, suspense } = useGetListData(queries.issues.list, {
  "hide-finished": "yes",
  "ordering":      defaultOrdering,
  "page":          1,
})

onServerPrefetch(async () => suspense())

const route = useRoute()

const ordering = computed(() => route.query?.ordering ?? defaultOrdering)

const getBreaks = (item) => {
  if (ordering.value.includes("cover_date")) {
    return {
      groupBreak:    item.cover_date ? DateTime.fromISO(item.cover_date).toFormat("yyyy") : "Unknown year",
      groupSubBreak: item.cover_date ? DateTime.fromISO(item.cover_date).toFormat("LLLL yyyy") : "Unknown month",
    }
  }

  return {
    groupBreak:   item.volume.display_name,
    groupBreakTo: `/volumes/${item.volume.slug}`,
  }
}

const items = computed(() =>
  (data.value?.results ?? []).map(item => ({
    ...item,
    ...getBreaks(item),
    subtitleItems: [item.publisher?.name ?? "No publisher", utilsFormatDate(item.cover_date) || "Cover date unknown"],
    to:            route.query?.ordering ? `/issues/${item.slug}?ordering=${route.query?.ordering}` : `/issues/${item.slug}`,
  })),
)

const pagesNumber = computed(() => data.value?.pages_count > 0 ? data.value?.pages_count : 0)
</script>

<template>
  <PageWithBreadcrumb>
    <DBCardsList
      :items="items"
      :loading="isPending"
      :ordering-variants="orderingVariants"
      :pages-number="pagesNumber"
      default-ordering="name"
      show-finished-toggle
      without-issues-label="characters"
    />
  </PageWithBreadcrumb>
</template>
