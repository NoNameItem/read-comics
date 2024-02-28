<script setup>
import { useGetListData } from "@/composables/useGetListData"
import { queries } from "@/queries"
import { useBreadcrumbsStore } from "@/stores/breadcrumbs"
import { computed, onServerPrefetch } from "vue"

useServerSeoMeta({ title: "Concepts" })

const breadcrumb = useBreadcrumbsStore()

breadcrumb.setBreadcrumbs("Concepts", [{ title: "Concepts" }])

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
    icon:  "fasl:arrow-down-1-9",
    title: "Volumes",
    value: "volumes_count",
  },
  {
    icon:  "fasl:arrow-down-9-1",
    title: "Volumes",
    value: "-volumes_count",
  },
  {
    icon:  "fasl:arrow-down-a-z",
    title: "Name",
    value: "name",
  },
  {
    icon:  "fasl:arrow-down-z-a",
    title: "Name",
    value: "-name",
  },
]

const { data, isPending, suspense } = useGetListData(queries.concepts.list, {
  "ordering": "name",
  "page":     1,
  "show-all": "no",
})

onServerPrefetch(async () => suspense())

const items = computed(() =>
  (data.value?.results ?? []).map(item => ({
    ...item,
    subtitleItems: [`${item.volumes_count} volume(s)`, `${item.issues_count} issue(s)`],
    to:            `/concepts/${item.slug}`,
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
      show-without-issues-toggle
      without-issues-label="concepts"
    />
  </PageWithBreadcrumb>
</template>
