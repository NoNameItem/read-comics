export const useBreadcrumbsStore = defineStore("breadcrumbs", () => {
  const pageTitle = ref("")
  const breadcrumbs = ref([])
  const loading = ref(true)

  const setBreadcrumbs = (newPageTitle, newBreadcrumbs) => {
    pageTitle.value = newPageTitle
    breadcrumbs.value = newBreadcrumbs

    if (process.client) { useHead({ title: newPageTitle }) }

    loading.value = false
  }

  const fullBreadcrumbs = computed(() => [
    {
      exact: true,
      icon:  "fasl:home",
      title: "Home",
      to:    "/",
    },
    ...breadcrumbs.value.map(item => ({ ...item, exact: true })),
  ])

  return { breadcrumbs, fullBreadcrumbs, loading, pageTitle, setBreadcrumbs }
})
