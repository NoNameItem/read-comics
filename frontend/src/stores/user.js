import { defineStore } from "pinia";
import axios from "@axios";

export const useUsersStore = defineStore("user", {
  state: () => ({
    accessToken: null,
    refreshToken: null,

    username: null,
    name: null,
    gender: null,
    images: null,
    isSuperuser: false,
    isStaff: false,
  }),
  actions: {
    setUser(user) {
      this.username = user?.username;
      this.name = user?.name;
      this.gender = user?.gender;
      this.images = user?.images;
      this.isSuperuser = user?.is_superuser;
      this.isStaff = user?.is_staff;
    },
    setTokens(accessToken, refreshToken) {
      this.accessToken = accessToken;
      this.refreshToken = refreshToken;
    },
    async login(username, password) {
      const loginUrl = "/auth/login/";
      try {
        const response = await axios.post(loginUrl, { username, password });
        if (response?.status === 200) {
          const data = await response.data;

          this.setTokens(data.access, data.refresh);
          this.setUser(data.user);
        }
      } catch (e) {
        console.log(e);
        return e;
      }
      this.$persist();
    },
    logout() {
      this.$reset();
      this.$persist();
    },
    async refreshTokens() {
      const refreshUrl = "/auth/token/refresh/";

      this.$hydrate();
      try {
        const response = await axios.post(refreshUrl, { refresh: this.refreshToken });
        if (response.status === 200) {
          const data = await response.data;

          this.setTokens(data.access, data.refresh);
          this.$persist();
        }
      } catch (e) {
        console.log(e);
      }
    },
  },
  persist: true,
});