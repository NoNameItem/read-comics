export default {
  IconBtn: {
    color:   "default",
    density: "comfortable",
    icon:    true,
    variant: "text",
    VIcon:   { size: 22 },
  },
  VAlert: {
    density: "comfortable",
    VBtn:    { color: undefined },
  },
  VAutocomplete: {
    color:       "primary",
    density:     "compact",
    hideDetails: "auto",
    menuProps:   { contentClass: "app-autocomplete__content v-autocomplete__content" },
    variant:     "outlined",
    VChip:       {
      color: "primary",
      label: true,
    },
  },

  // VImg: {
  //   eager: true,
  VAvatar: {
    // ℹ️ Remove after next release
    variant: "flat",
  },
  // },
  VBadge: {
    // set v-badge default color to primary
    color: "primary",
  },
  VBtn: {
    // set v-btn default color to primary
    color: "primary",
  },
  VCheckbox: {
    // set v-checkbox default color to primary
    color:       "primary",
    density:     "comfortable",
    hideDetails: "auto",
  },
  VCheckboxBtn: { color: "primary" },
  VChip:        { size: "small" },
  VCombobox:    {
    color:       "primary",
    density:     "compact",
    hideDetails: "auto",
    variant:     "outlined",
    VChip:       {
      color: "primary",
      label: true,
    },
  },
  VDataTable: {
    VDataTableFooter: {
      VBtn: {
        color:   "default",
        density: "comfortable",
      },
    },
  },
  VExpansionPanel: {
    collapseIcon: "tabler-chevron-right",
    expandIcon:   "tabler-chevron-right",
  },
  VExpansionPanelTitle: {
    collapseIcon: "tabler-chevron-right",
    expandIcon:   "tabler-chevron-right",
  },
  VFileInput: {
    color:       "primary",
    density:     "compact",
    hideDetails: "auto",
    variant:     "outlined",
  },
  VList: {
    density:      "comfortable",
    VCheckboxBtn: { density: "compact" },
  },
  VPagination: {
    activeColor: "primary",
    density:     "comfortable",
    variant:     "tonal",
  },
  VProgressCircular: {
    // set v-progress-circular default color to primary
    color: "primary",
  },
  VProgressLinear: {
    color:      "primary",
    height:     12,
    rounded:    true,
    roundedBar: true,
  },
  VRadio: {
    density:     "comfortable",
    hideDetails: "auto",
  },
  VRadioGroup: {
    color:       "primary",
    density:     "comfortable",
    hideDetails: "auto",
  },
  VRangeSlider: {
    // set v-range-slider default color to primary
    color:       "primary",
    density:     "comfortable",
    hideDetails: "auto",
    thumbLabel:  true,
    thumbSize:   7,
    trackColor:  "rgb(var(--v-theme-on-surface),0.06)",
    trackSize:   6,
  },
  VRating: {
    // set v-rating default color to primary
    color: "warning",
  },
  VSelect: {
    color:       "primary",
    density:     "compact",
    hideDetails: "auto",
    variant:     "outlined",
    VChip:       {
      color: "primary",
      label: true,
    },
  },
  VSlider: {
    // set v-slider default color to primary
    color:       "primary",
    hideDetails: "auto",
    thumbSize:   7,
    trackColor:  "rgb(var(--v-theme-on-surface),0.06)",
    trackSize:   6,
  },
  VSwitch: {
    color:       "primary",
    hideDetails: "auto",
    // set v-switch default color to primary
    inset:       true,
  },
  VTabs: {
    // set v-tabs default color to primary
    color:       "primary",
    density:     "comfortable",
    VSlideGroup: { showArrows: true },
  },
  VTextarea: {
    color:       "primary",
    density:     "compact",
    hideDetails: "auto",
    variant:     "outlined",
  },
  VTextField: {
    color:       "primary",
    density:     "compact",
    hideDetails: "auto",
    variant:     "outlined",
  },
  VTimeline: { lineThickness: 1 },

  VTooltip: {
    // set v-tooltip default location to top
    location: "top",
  },
}
