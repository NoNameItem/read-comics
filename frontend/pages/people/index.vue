<script setup>
import { computed, onServerPrefetch } from 'vue'
import { useBreadcrumbsStore } from '@/stores/breadcrumbs'
import { queries } from '@/queries'
import { useGetListData } from '@/composables/useGetListData'
import PageWithBreadcrumb from '~/components/PageWithBreadcrumb.vue'

useServerSeoMeta({
  title: 'People',
})

const breadcrumb = useBreadcrumbsStore()

breadcrumb.setBreadcrumbs('People', [{ title: 'people' }])

const orderingVariants = [
  {
    title: 'Issues',
    icon: 'fasl:arrow-down-1-9',
    value: 'issues_count',
  },
  {
    title: 'Issues',
    icon: 'fasl:arrow-down-9-1',
    value: '-issues_count',
  },
  {
    title: 'Volumes',
    icon: 'fasl:arrow-down-1-9',
    value: 'volumes_count',
  },
  {
    title: 'Volumes',
    icon: 'fasl:arrow-down-9-1',
    value: '-volumes_count',
  },
  {
    title: 'Name',
    icon: 'fasl:arrow-down-a-z',
    value: 'name',
  },
  {
    title: 'Name',
    icon: 'fasl:arrow-down-z-a',
    value: '-name',
  },
]

const { isPending, data, suspense } = useGetListData(queries.people.list, {
  'show-all': 'no',
  'ordering': 'name',
  'page': 1,
})

onServerPrefetch(async () => suspense())

const items = computed(() =>
  (data.value?.results ?? []).map(item => ({
    ...item,
    subtitleItems: [`${item.volumes_count} volume(s)`, `${item.issues_count} issue(s)`],
    to: `/people/${item.slug}`,
  })),
)

const pagesNumber = computed(() => data.value?.pages_count > 0 ? data.value?.pages_count : 0)
</script>

<template>
  <PageWithBreadcrumb>
    <DBCardsList
      :ordering-variants="orderingVariants"
      default-ordering="name"
      without-issues-label="people"
      show-without-issues-toggle
      :items="items"
      :loading="isPending"
      :pages-number="pagesNumber"
    />
  </PageWithBreadcrumb>
</template>
