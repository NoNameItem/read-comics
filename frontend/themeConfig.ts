import { defineThemeConfig } from "@core"
import { Skins } from "@core/enums"
// ❗ Logo SVG must be imported with ?raw suffix
import logo from "@images/logo.png"
import { AppContentLayoutNav, ContentWidth, FooterType, NavbarType } from "@layouts/enums"
import { breakpointsVuetify } from "@vueuse/core"
import { VIcon } from "vuetify/components/VIcon"

export const { layoutConfig, themeConfig } = defineThemeConfig({
  app: {
    contentLayoutNav: AppContentLayoutNav.Vertical,
    contentWidth:     ContentWidth.Fluid,
    i18n:             {
      defaultLocale: "en",
      enable:        false,
      langConfig:    [
        {
          i18nLang: "en",
          isRTL:    false,
          label:    "English",
        },
        {
          i18nLang: "fr",
          isRTL:    false,
          label:    "French",
        },
        {
          i18nLang: "ar",
          isRTL:    true,
          label:    "Arabic",
        },
      ],
    },
    iconRenderer:             VIcon,
    logo:                     h("img", { alt: "app-logo", src: logo }),
    overlayNavFromBreakpoint: breakpointsVuetify.md + 16, // 16 for scrollbar. Docs: https://next.vuetifyjs.com/en/features/display-and-platform/
    skin:                     Skins.Default,
    theme:                    "system",
    title:                    "read-comics.net",
  },
  footer:        { type: FooterType.Hidden },
  horizontalNav: {
    transition: "slide-y-reverse-transition",
    type:       "sticky",
  },
  /*
  // ℹ️  In below Icons section, you can specify icon for each component. Also you can use other props of v-icon component like `color` and `size` for each icon.
  // Such as: chevronDown: { icon: 'tabler-chevron-down', color:'primary', size: '24' },
  */
  icons: {
    chevronDown:             { icon: "fasl:chevron-down" },
    chevronRight:            { icon: "fasl:chevron-right", size: 18 },
    close:                   { icon: "fasl:xmark-large" },
    sectionTitlePlaceholder: { icon: "fasl:ellipsis" },
    verticalNavPinned:       { icon: "fasl:circle-o" },
    verticalNavUnPinned:     { icon: "fasl:circle" },
  },
  navbar: {
    navbarBlur: true,
    type:       NavbarType.Sticky,
  },

  verticalNav: {
    defaultNavItemIconProps: { icon: "fasl:circle", size: 10 },
    isVerticalNavCollapsed:  false,
    isVerticalNavSemiDark:   false,
  },
})
