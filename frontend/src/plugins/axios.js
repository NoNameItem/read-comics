import axios from "axios";
import router from "@/router";
import { useUsersStore } from "@/stores/user";

const axiosIns = axios.create({
  // You can add your headers here
  // ================================
  baseURL: "http://127.0.0.1:8000/api",
  // timeout: 1000,
  // headers: {'X-Custom-Header': 'foobar'}
});

// ℹ️ Add request interceptor to send the authorization header on each subsequent request after login
axiosIns.interceptors.request.use(
  async (config) => {
    const userStore = useUsersStore();

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
    const userStore = useUsersStore();
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    // Do something with response error
    const originalRequest = error.config;
    if (error.response?.status === 401 && originalRequest.url.includes("auth/token/refresh/")) {
      userStore.$reset();

      return Promise.reject(error);
    } else if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      await userStore.refreshTokens();

      return axiosIns(originalRequest);
    }

    return Promise.reject(error);
  }
);
export default axiosIns;
