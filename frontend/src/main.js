/* eslint-disable import/order */
import "@/@iconify/icons-bundle";
import App from "@/App.vue";
import layoutsPlugin from "@/plugins/layouts";
import vuetify from "@/plugins/vuetify";
import { loadFonts } from "@/plugins/webfontloader";
import router from "@/router";
import "@core/scss/template/index.scss";
import "@styles/styles.scss";
import { createPinia } from "pinia";
import { createApp } from "vue";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { VueQueryPlugin } from "@tanstack/vue-query";

import initIconLibrary from "@/plugins/icons";

loadFonts();
initIconLibrary();

// Create vue app
const app = createApp(App);

// Use plugins
app.use(vuetify);

app.component("FontAwesomeIcon", FontAwesomeIcon); // Register component globally

const pinia = createPinia();

pinia.use(piniaPluginPersistedstate);
app.use(pinia);
app.use(router);
app.use(layoutsPlugin);
app.use(Toast, {
  transition: "Vue-Toastification__bounce",
  maxToasts: 20,
  newestOnTop: true,
});
app.use(VueQueryPlugin);

// Mount vue app
app.mount("#app");
