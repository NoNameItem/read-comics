import { createLayouts } from "@layouts"
import "@layouts/styles/index.scss"
import { layoutConfig } from "@themeConfig"

export default defineNuxtPlugin((nuxtApp) => {
  // ℹ️ We generate layout config from our themeConfig so you don't have to write config twice
  nuxtApp.vueApp.use(createLayouts(layoutConfig))
})
