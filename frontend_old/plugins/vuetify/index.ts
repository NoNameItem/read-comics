import defaults from "./defaults"
import { icons } from "./icons"
import { staticPrimaryColor, themes } from "./theme"
// Styles
import { cookieRef } from "@/@layouts/stores/config"
import { deepMerge } from "@antfu/utils"
import "@core/scss/template/libs/vuetify/index.scss"
import { createVuetify } from "vuetify"
import { VBtn } from "vuetify/components/VBtn"
import "vuetify/styles"

export default defineNuxtPlugin((nuxtApp) => {
  const cookieThemeValues = {
    defaultTheme: resolveVuetifyTheme(),
    themes:       {
      dark:  { colors: { primary: cookieRef("darkThemePrimaryColor", staticPrimaryColor).value } },
      light: { colors: { primary: cookieRef("lightThemePrimaryColor", staticPrimaryColor).value } },
    },
  }

  const optionTheme = deepMerge({ themes }, cookieThemeValues)

  const vuetify = createVuetify({
    aliases: { IconBtn: VBtn },
    defaults,
    icons,
    ssr:     true,
    theme:   optionTheme,
  })

  nuxtApp.vueApp.use(vuetify)
})
