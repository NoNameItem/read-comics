<script setup>
import { computed, onServerPrefetch } from "vue"
import { useBreadcrumbsStore } from "@/stores/breadcrumbs"
import { queries } from "@/queries"
import { useGetListData } from "@/composables/useGetListData"

useServerSeoMeta({
  title: "Characters",
})

const breadcrumb = useBreadcrumbsStore()

breadcrumb.setBreadcrumbs("Characters", [{ title: "Characters" }])

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

const { isPending, data, suspense } = useGetListData(queries.characters.list, {
  "show-all": "no",
  "ordering": "name",
  "page":     1,
})

const items = computed(() =>
  (data.value?.results ?? []).map(item => ({
    ...item,
    subtitleItems: [
      item.publisher?.name ?? "No publisher",
      `${item.volumes_count} volume(s)`,
      `${item.issues_count} issue(s)`,
    ],
    to: `/characters/${item.slug}`,
  })),
)

const pagesNumber = computed(() => data.value?.pages_count > 0 ? data.value?.pages_count : 0)

onServerPrefetch(async () => suspense())
</script>

<template>
  <PageWithBreadcrumb>
    <DBCardsList
      :ordering-variants="orderingVariants"
      default-ordering="name"
      without-issues-label="characters"
      show-without-issues-toggle
      :items="items"
      :loading="isPending"
      :pages-number="pagesNumber"
    />
  </PageWithBreadcrumb>
</template>
