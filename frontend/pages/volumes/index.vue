<script setup>
import { useGetListData } from "@/composables/useGetListData"
import { queries } from "@/queries"
import { useBreadcrumbsStore } from "@/stores/breadcrumbs"
import { useUserStore } from "@/stores/user"
import { computed, onServerPrefetch } from "vue"

useServerSeoMeta({ title: "Volumes" })

const user = useUserStore()

const breadcrumb = useBreadcrumbsStore()

breadcrumb.setBreadcrumbs("Volumes", [{ title: "Volumes" }])

const orderingVariants = [
  {
    icon:  "fasl:arrow-down-1-9",
    title: "Issues",
    value: "issues_count",
  },
  {
    icon:  "fasl:arrow-down-9-1",
    title: "Issues",
    value: "-issues_count",
  },
  {
    icon:  "fasl:arrow-down-a-z",
    title: "Name",
    value: "name,start_year",
  },
  {
    icon:  "fasl:arrow-down-z-a",
    title: "Name",
    value: "-name,-start_year",
  },
  {
    icon:  "fasl:arrow-down-1-9",
    title: "Start year",
    value: "start_year",
  },
  {
    icon:  "fasl:arrow-down-9-1",
    title: "Start year",
    value: "-start_year",
  },
]

const { data, isPending, suspense } = useGetListData(queries.volumes.list, {
  "hide-finished": "yes",
  "ordering":      "start_year",
  "page":          1,
})

onServerPrefetch(async () => suspense())

const route = useRoute()

const ordering = computed(() => route.query?.ordering ?? "start_year")

const getGroupBreak = (item) => {
  if (ordering.value.includes("start_year")) { return `${item.start_year}` ?? "Unknown year" }

  return null
}

const items = computed(() =>
  (data.value?.results ?? []).map(item => ({
    ...item,
    groupBreak:    getGroupBreak(item),
    subtitleItems: user.loggedIn
      ? [item.publisher?.name ?? "No publisher", `${item.issues_count} issue(s)`, `${item.finished_count} finished`]
      : [item.publisher?.name ?? "No publisher", `${item.issues_count} issue(s)`],
    to: `/volumes/${item.slug}`,
  })),
)

const pagesNumber = computed(() => data.value?.pages_count > 0 ? data.value?.pages_count : 0)
</script>

<template>
  <DBCardsList
    :items="items"
    :loading="isPending"
    :ordering-variants="orderingVariants"
    :pages-number="pagesNumber"
    default-ordering="name"
    show-finished-toggle
    without-issues-label="volumes"
  />
</template>
