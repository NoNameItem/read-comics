export default defineNuxtRouteMiddleware((to, from) => {
  const user = useUserStore()

  if (to.meta?.loginRequired && !user.loggedIn) {
    return navigateTo({
      path: '/login',
      query: { to: to.fullPath },
    })
  }
})
