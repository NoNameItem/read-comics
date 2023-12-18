export default defineNuxtRouteMiddleware((_to, _from) => {
  const user = useUserStore()

  if (process.server && user.refreshToken)
    user.refreshTokens()
})
