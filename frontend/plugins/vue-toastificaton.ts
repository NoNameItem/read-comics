import type { PluginOptions } from "vue-toastification"
import Toast from "vue-toastification"

const options: PluginOptions = {}

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(Toast, options)
})
