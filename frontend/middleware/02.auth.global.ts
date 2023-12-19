export default defineNuxtRouteMiddleware((to, _from) => {
  const user = useUserStore()

  if (to.meta?.loginRequired && !user.loggedIn) {
    return navigateTo({
      path:  "/login",
      query: { to: to.fullPath },
    })
  }
})
