export const useBreadcrumbsStore = defineStore("breadcrumbs", () => {
  const pageTitle = ref("");
  const breadcrumbs = ref([]);
  const htmlTitle = useTitle();
  const loading = ref(true);

  const setBreadcrumbs = (newPageTitle, newBreadcrumbs) => {
    pageTitle.value = newPageTitle;
    breadcrumbs.value = newBreadcrumbs;
    htmlTitle.value = newPageTitle;
    loading.value = false;
  };

  const fullBreadcrumbs = computed(() => [{ icon: "fasl:home", title: "Home", to: "/" }, ...breadcrumbs.value]);

  return { pageTitle, breadcrumbs, loading, fullBreadcrumbs, setBreadcrumbs };
});
