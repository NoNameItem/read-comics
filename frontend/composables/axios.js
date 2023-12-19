import axios from "axios"
import { useUserStore } from "@/stores/user"

export function useAxios() {
  const runtimeConfig = useRuntimeConfig()

  const axiosIns = axios.create({
    baseURL: runtimeConfig.apiURL,
  })

  axiosIns.interceptors.request.use(
    async (config) => {
      const userStore = useUserStore()

      userStore.$hydrate()
      if (userStore.accessToken)
        config.headers.Authorization = `Bearer ${userStore.accessToken}`

      return config
    },
    (error) => {
      return Promise.reject(error)
    },
  )

  // ℹ️ Add response interceptor to handle 401 response
  axiosIns.interceptors.response.use(
    (response) => {
      // Any status code that lie within the range of 2xx cause this function to trigger
      // Do something with response data
      return response
    },
    async (error) => {
      const userStore = useUserStore()

      // Any status codes that falls outside the range of 2xx cause this function to trigger
      // Do something with response error
      const originalRequest = error.config
      if (error.response?.status === 401 && originalRequest.url.includes("auth/token/refresh/")) {
        userStore.logout()
        userStore.$persist()

        return Promise.reject(error)
      }
      else if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true
        userStore.$hydrate()
        if (!userStore.refreshingToken) {
          userStore.refreshingToken = true
          userStore.$persist()
          await userStore.refreshTokens()
          userStore.refreshingToken = false
          userStore.$persist()

          return axiosIns(originalRequest)
        }
        else {
          const intervalId = setInterval(() => {
            userStore.$hydrate()
            if (!userStore.refreshingToken) {
              clearInterval(intervalId)

              return axiosIns(originalRequest)
            }
          }, 100)
        }
      }

      return Promise.reject(error)
    },
  )

  return axiosIns
}
