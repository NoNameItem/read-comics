import { setupLayouts } from "virtual:generated-layouts";
import { createRouter, createWebHistory } from "vue-router";
import routes from "~pages";
import { useUserStore } from "@/stores/user";
import { useBreadcrumbsStore } from "@/stores/breadcrumbs";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [...setupLayouts(routes)],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

// Docs: https://router.vuejs.org/guide/advanced/navigation-guards.html#global-before-guards
router.beforeEach((to, from) => {
  const user = useUserStore();
  // instead of having to check every route record with
  // to.matched.some(record => record.meta.requiresAuth)
  if (to.meta?.loginRequired && !user.loggedIn) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    return {
      path: "/login",
      // save the location we were at to come back later
      query: { to: to.fullPath },
    };
  }
});

router.afterEach((to, from) => {
  const breadcrumbs = useBreadcrumbsStore();
  if (to.path !== from.path) {
    breadcrumbs.loading = true;
  }
});
export default router;
