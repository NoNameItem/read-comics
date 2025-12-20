<script lang="ts" setup>
import Footer from "@/layouts/components/Footer.vue"
import NavbarThemeSwitcher from "@/layouts/components/NavbarThemeSwitcher.vue"
import UserProfile from "@/layouts/components/UserProfile.vue"
import navItems from "@/navigation/vertical"
import NavBarI18n from "@core/components/I18n.vue"
// Components
import { VerticalNavLayout } from "@layouts"
import { themeConfig } from "@themeConfig"

// @layouts plugin
</script>

<template>
  <VerticalNavLayout :nav-items="navItems">
    <!-- 👉 navbar -->
    <template #navbar="{ toggleVerticalOverlayNavActive }">
      <div class="d-flex h-100 align-center">
        <IconBtn
          id="vertical-nav-toggle-btn"
          class="ms-n3 d-lg-none"
          @click="toggleVerticalOverlayNavActive(true)"
        >
          <VIcon
            icon="fasl:bars"
            size="26"
          />
        </IconBtn>

        <NavbarThemeSwitcher />

        <VSpacer />

        <NavBarI18n
          v-if="themeConfig.app.i18n.enable && themeConfig.app.i18n.langConfig?.length"
          :languages="themeConfig.app.i18n.langConfig"
        />
        <UserProfile />
      </div>
    </template>

    <!-- 👉 Pages -->
    <slot />

    <!-- 👉 Footer -->
    <template #footer>
      <Footer />
    </template>

    <!-- 👉 Customizer -->
    <!-- <TheCustomizer /> -->
  </VerticalNavLayout>
</template>
