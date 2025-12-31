// Docs: [[docs/frontend/middleware/auth.global.md]]
export default defineNuxtRouteMiddleware((to, _from) => {
  const user = useUserStore()

  if (to.meta?.loginRequired && !user.loggedIn) {
    return navigateTo({
      path: '/users/login',
      query: { to: to.fullPath }
    })
  }
})
