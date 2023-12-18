import { fileURLToPath } from 'node:url'
import vuetify from 'vite-plugin-vuetify'
import { fontawesomeAutoimport } from './fontawesome-autoimport'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  app: {
    head: {
      title: '',
      titleTemplate: '%s - Read-Comics.Net',

      link: [
        {
          rel: 'icon',
          type: 'image/x-icon',
          href: '/favicon.png',
        },
      ],
    },

    pageTransition: { name: 'page', mode: 'out-in' },
  },

  devtools: {
    enabled: true,
  },

  css: ['@core/scss/template/index.scss', '@styles/styles.scss', '@fortawesome/fontawesome-svg-core/styles.css', 'vue-toastification/dist/index.css'],

  components: {
    dirs: [
      {
        path: '@/@core/components',
        pathPrefix: false,
      },
      {
        path: '~/components/global',
        global: true,
      },
      {
        path: '~/components',
        pathPrefix: false,
      },
      {
        path: '~/views',
        pathPrefix: false,
      },
    ],
  },

  // plugins: ['@/plugins/01.icons.js', '@/plugins/vuetify/index.ts'],

  imports: {
    dirs: ['./@core/utils', './@core/composable/', './plugins/*/composables/*'],
    presets: [],
  },

  hooks: {},

  experimental: {
    typedPages: true,
    inlineSSRStyles: false,
  },

  typescript: {
    tsConfig: {
      compilerOptions: {
        paths: {
          '@/*': ['../*'],
          '@themeConfig': ['../themeConfig.ts'],
          '@layouts/*': ['../@layouts/*'],
          '@layouts': ['../@layouts'],
          '@core/*': ['../@core/*'],
          '@core': ['../@core'],
          '@images/*': ['../assets/images/*'],
          '@styles/*': ['../assets/styles/*'],
          '@validators': ['../@core/utils/validators'],
          '@db/*': ['../server/fake-db/*'],
          '@api-utils/*': ['../server/utils/*'],
          '@axios': ['../utils/axios'],
        },
      },
    },
  },

  // ℹ️ Disable source maps until this is resolved: https://github.com/vuetifyjs/vuetify-loader/issues/290
  sourcemap: {
    server: true,
    client: true,
  },

  vue: {
    compilerOptions: {
      isCustomElement: tag => tag === 'swiper-container' || tag === 'swiper-slide',
    },
  },

  vite: {
    define: { 'process.env': {} },

    resolve: {
      alias: {
        '@': fileURLToPath(new URL('.', import.meta.url)),
        '@themeConfig': fileURLToPath(new URL('./themeConfig.ts', import.meta.url)),
        '@core': fileURLToPath(new URL('./@core', import.meta.url)),
        '@layouts': fileURLToPath(new URL('./@layouts', import.meta.url)),
        '@images': fileURLToPath(new URL('./assets/images/', import.meta.url)),
        '@styles': fileURLToPath(new URL('./assets/styles/', import.meta.url)),
        '@configured-variables': fileURLToPath(new URL('./assets/styles/variables/_template.scss', import.meta.url)),
        'apexcharts': fileURLToPath(new URL('node_modules/apexcharts-clevision', import.meta.url)),
        '@db': fileURLToPath(new URL('./server/fake-db/', import.meta.url)),
        '@api-utils': fileURLToPath(new URL('./server/utils/', import.meta.url)),
        '@axios': fileURLToPath(new URL('./utils/axios', import.meta.url)),
        '@validators': fileURLToPath(new URL('./@core/utils/validators', import.meta.url)),
      },
    },

    build: {
      chunkSizeWarningLimit: 5000,
    },

    optimizeDeps: {
      exclude: ['vuetify'],
      entries: ['./**/*.vue'],
    },

    plugins: [
      vuetify({
        styles: {
          configFile: 'assets/styles/variables/_vuetify.scss',
        },
      }),

      fontawesomeAutoimport(['.idea', '.vscode', '.nuxt', 'node_modules']),
      null,
    ],
  },

  build: {
    transpile: [
      'vuetify',
      '@fortawesome/fontawesome-free',
      '@fortawesome/fontawesome-svg-core',
      '@fortawesome/free-brands-svg-icons',
      '@fortawesome/sharp-light-svg-icons',
      '@fortawesome/vue-fontawesome',
      'vue-toastification',
    ]
    ,
  },

  modules: ['@vueuse/nuxt', '@nuxtjs/device', '@pinia/nuxt', '@pinia-plugin-persistedstate/nuxt', '@hebilicious/vue-query-nuxt'],

})
