import { fontawesomeAutoimport } from "./fontawesome-autoimport"
import { fileURLToPath } from "node:url"
import vuetify from "vite-plugin-vuetify"

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  app: {
    head: {
      link: [
        {
          href: "/favicon.png",
          rel:  "icon",
          type: "image/x-icon",
        },
      ],
      title: "",

      titleTemplate: "%s - Read-Comics.Net",
    },

    pageTransition: { mode: "out-in", name: "page" },
  },

  build: {
    transpile: [
      "vuetify",
      "@fortawesome/fontawesome-free",
      "@fortawesome/fontawesome-svg-core",
      "@fortawesome/free-brands-svg-icons",
      "@fortawesome/sharp-light-svg-icons",
      "@fortawesome/vue-fontawesome",
      "vue-toastification",
    ]
    ,
  },

  components: {
    dirs: [
      {
        path:       "@/@core/components",
        pathPrefix: false,
      },
      {
        global: true,
        path:   "~/components/global",
      },
      {
        path:       "~/components",
        pathPrefix: false,
      },
      {
        path:       "~/views",
        pathPrefix: false,
      },
    ],
  },

  css: ["@core/scss/template/index.scss", "@styles/styles.scss", "@fortawesome/fontawesome-svg-core/styles.css", "vue-toastification/dist/index.css"],

  // plugins: ['@/plugins/01.icons.js', '@/plugins/vuetify/index.ts'],

  devtools: { enabled: true },

  experimental: {
    inlineSSRStyles: false,
    typedPages:      true,
  },

  hooks: {},

  imports: {
    dirs:    ["./@core/utils", "./@core/composable/", "./plugins/*/composables/*"],
    presets: [],
  },

  modules: [
    "@vueuse/nuxt",
    "@nuxtjs/device",
    "@pinia/nuxt",
    "@pinia-plugin-persistedstate/nuxt",
    "@hebilicious/vue-query-nuxt",
  ],

  // ℹ️ Disable source maps until this is resolved: https://github.com/vuetifyjs/vuetify-loader/issues/290
  sourcemap: {
    client: false,
    server: false,
  },

  typescript: {
    tsConfig: {
      compilerOptions: {
        paths: {
          "@/*":          ["../*"],
          "@api-utils/*": ["../server/utils/*"],
          "@core":        ["../@core"],
          "@core/*":      ["../@core/*"],
          "@db/*":        ["../server/fake-db/*"],
          "@images/*":    ["../assets/images/*"],
          "@layouts":     ["../@layouts"],
          "@layouts/*":   ["../@layouts/*"],
          "@styles/*":    ["../assets/styles/*"],
          "@themeConfig": ["../themeConfig.ts"],
          "@validators":  ["../@core/utils/validators"],
        },
      },
    },
  },

  vite: {
    build: { chunkSizeWarningLimit: 5000 },

    define: { "process.env": {} },

    optimizeDeps: {
      entries: ["./**/*.vue"],
      exclude: ["vuetify"],
    },

    plugins: [
      vuetify({ styles: { configFile: "assets/styles/variables/_vuetify.scss" } }),
      fontawesomeAutoimport([".idea", ".vscode", ".nuxt", "node_modules"]),
      null,
    ],

    resolve: {
      alias: {
        "@":                     fileURLToPath(new URL(".", import.meta.url)),
        "@api-utils":            fileURLToPath(new URL("./server/utils/", import.meta.url)),
        "@configured-variables": fileURLToPath(new URL("./assets/styles/variables/_template.scss", import.meta.url)),
        "@core":                 fileURLToPath(new URL("./@core", import.meta.url)),
        "@db":                   fileURLToPath(new URL("./server/fake-db/", import.meta.url)),
        "@images":               fileURLToPath(new URL("./assets/images/", import.meta.url)),
        "@layouts":              fileURLToPath(new URL("./@layouts", import.meta.url)),
        "@styles":               fileURLToPath(new URL("./assets/styles/", import.meta.url)),
        "@themeConfig":          fileURLToPath(new URL("./themeConfig.ts", import.meta.url)),
        "@validators":           fileURLToPath(new URL("./@core/utils/validators", import.meta.url)),
        "apexcharts":            fileURLToPath(new URL("node_modules/apexcharts-clevision", import.meta.url)),
      },
    },
  },

  vue: { compilerOptions: { isCustomElement: tag => tag === "swiper-container" || tag === "swiper-slide" } },

})
