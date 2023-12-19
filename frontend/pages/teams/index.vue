<script setup>
import { computed, onServerPrefetch } from "vue"
import { useBreadcrumbsStore } from "@/stores/breadcrumbs"
import { queries } from "@/queries"
import { useGetListData } from "@/composables/useGetListData"

useServerSeoMeta({
  title: "Teams",
})

const breadcrumb = useBreadcrumbsStore()

breadcrumb.setBreadcrumbs("Teams", [{ title: "Teams" }])

const orderingVariants = [
  {
    title: "Issues",
    icon:  "fasl:arrow-down-1-9",
    value: "issues_count",
  },
  {
    title: "Issues",
    icon:  "fasl:arrow-down-9-1",
    value: "-issues_count",
  },
  {
    title: "Volumes",
    icon:  "fasl:arrow-down-1-9",
    value: "volumes_count",
  },
  {
    title: "Volumes",
    icon:  "fasl:arrow-down-9-1",
    value: "-volumes_count",
  },
  {
    title: "Name",
    icon:  "fasl:arrow-down-a-z",
    value: "name",
  },
  {
    title: "Name",
    icon:  "fasl:arrow-down-z-a",
    value: "-name",
  },
]

const { isPending, data, suspense } = useGetListData(queries.teams.list, {
  "show-all": "no",
  "ordering": "name",
  "page":     1,
})

onServerPrefetch(async () => suspense())

const items = computed(() =>
  (data.value?.results ?? []).map(item => ({
    ...item,
    subtitleItems: [
      item.publisher?.name ?? "No publisher",
      `${item.volumes_count} volume(s)`,
      `${item.issues_count} issue(s)`,
    ],
    to: `/teams/${item.slug}`,
  })),
)

const pagesNumber = computed(() => data.value?.pages_count > 0 ? data.value?.pages_count : 0)
</script>

<template>
  <DBCardsList
    :ordering-variants="orderingVariants"
    default-ordering="name"
    without-issues-label="teams"
    show-without-issues-toggle
    :items="items"
    :loading="isPending"
    :pages-number="pagesNumber"
  />
</template>
