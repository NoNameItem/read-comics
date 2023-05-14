import { breakpointsVuetify } from "@vueuse/core";
import { VIcon } from "vuetify/components/VIcon";

// ❗ Logo SVG must be imported with ?raw suffix
import logo from "@/assets/logo.png";
import { defineThemeConfig } from "@core";
import { RouteTransitions, Skins } from "@core/enums";
import { AppContentLayoutNav, ContentWidth, FooterType, NavbarType } from "@layouts/enums";

export const { themeConfig, layoutConfig } = defineThemeConfig({
  app: {
    title: "Read-Comics.Net",
    logo: h("img", { src: logo, alt: "app-logo" }),
    contentWidth: ContentWidth.Fluid,
    contentLayoutNav: AppContentLayoutNav.Vertical,
    overlayNavFromBreakpoint: breakpointsVuetify.md + 16,
    enableI18n: false,
    theme: "system",
    isRtl: false,
    skin: Skins.Default,
    routeTransition: RouteTransitions.Fade,
    iconRenderer: VIcon,
  },
  navbar: {
    type: NavbarType.Sticky,
    navbarBlur: true,
  },
  footer: { type: FooterType.Static },
  verticalNav: {
    isVerticalNavCollapsed: false,
    defaultNavItemIconProps: { icon: "tabler-circle", size: 10 },
    isVerticalNavSemiDark: false,
  },
  horizontalNav: {
    type: "sticky",
    transition: "slide-y-reverse-transition",
  },
  icons: {
    chevronDown: { icon: "fat-chevron-down" },
    chevronRight: { icon: "fat-chevron-right", size: 18 },
    close: { icon: "tabler-x" },
    verticalNavPinned: { icon: "tabler-circle-dot" },
    verticalNavUnPinned: { icon: "tabler-circle" },
    sectionTitlePlaceholder: { icon: "tabler-separator" },
  },
});
