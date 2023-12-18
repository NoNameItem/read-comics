export const useBreadcrumbsStore = defineStore('breadcrumbs', () => {
  const pageTitle = ref('')
  const breadcrumbs = ref([])
  const loading = ref(true)

  const setBreadcrumbs = (newPageTitle, newBreadcrumbs) => {
    pageTitle.value = newPageTitle
    breadcrumbs.value = newBreadcrumbs

    if (process.client)
      useHead({ title: newPageTitle })

    loading.value = false
  }

  const fullBreadcrumbs = computed(() => [{
    icon: 'fasl:home',
    title: 'Home',
    to: '/',
    exact: true,
  }, ...breadcrumbs.value.map(item => ({ ...item, exact: true }))])

  return { pageTitle, breadcrumbs, loading, fullBreadcrumbs, setBreadcrumbs }
})
