// Docs: [[docs/frontend/stores/breadcrumbs.md]]
import { useHead } from '#unhead/composables'

export const useBreadcrumbsStore = defineStore('breadcrumbs', () => {
  const pageTitle = ref('')
  const breadcrumbs = ref([])
  const loading = ref(true)

  const setBreadcrumbs = (newPageTitle, newBreadcrumbs) => {
    pageTitle.value = newPageTitle
    breadcrumbs.value = newBreadcrumbs

    if (import.meta.client) {
      useHead({ title: newPageTitle })
    }

    loading.value = false
  }

  const fullBreadcrumbs = computed(() => [
    {
      icon: 'i-lucide-house',
      to: '/'
    },
    ...breadcrumbs.value.map((item) => ({ ...item }))
  ])

  return { breadcrumbs, fullBreadcrumbs, loading, pageTitle, setBreadcrumbs }
})
