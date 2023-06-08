export const useBreadcrumbsStore = defineStore("breadcrumbs", () => {
  const pageTitle = ref("");
  const breadcrumbs = ref([]);
  const htmlTitle = useTitle();

  const setBreadcrumbs = (newPageTitle, newBreadcrumbs) => {
    pageTitle.value = newPageTitle;
    breadcrumbs.value = newBreadcrumbs;
    htmlTitle.value = newPageTitle;
  };

  const fullBreadcrumbs = computed(() => [{ icon: "fasl:home", title: "Home", to: "/" }, ...breadcrumbs.value]);

  return { pageTitle, breadcrumbs, fullBreadcrumbs, setBreadcrumbs };
});
