import axios from "axios";
import { useUserStore } from "@/stores/user";

const axiosIns = axios.create({
  // You can add your headers here
  // ================================
  baseURL:
    !window?._env_?.API_BASE_URL || window?._env_?.API_BASE_URL === "$API_BASE_URL"
      ? "http://127.0.0.1:8000/api"
      : window?._env_?.API_BASE_URL,
  // timeout: 1000,
  // headers: {'X-Custom-Header': 'foobar'}
});

// ℹ️ Add request interceptor to send the authorization header on each subsequent request after login
axiosIns.interceptors.request.use(
  async (config) => {
    const userStore = useUserStore();

    userStore.$hydrate();
    if (userStore.accessToken) {
      config.headers.Authorization = `Bearer ${userStore.accessToken}`;
    }

    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

// ℹ️ Add response interceptor to handle 401 response
axiosIns.interceptors.response.use(
  function (response) {
    // Any status code that lie within the range of 2xx cause this function to trigger
    // Do something with response data
    return response;
  },
  async function (error) {
    const userStore = useUserStore();
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    // Do something with response error
    const originalRequest = error.config;
    if (error.response?.status === 401 && originalRequest.url.includes("auth/token/refresh/")) {
      userStore.logout();
      userStore.$persist();

      return Promise.reject(error);
    } else if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      userStore.$hydrate();
      await userStore.refreshTokens();
      userStore.$persist();

      return axiosIns(originalRequest);
    }

    return Promise.reject(error);
  }
);
export default axiosIns;
