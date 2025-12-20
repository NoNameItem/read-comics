import { fab } from "@/plugins/iconsets/fab"
import { fasl } from "@/plugins/iconsets/fasl"
import type { IconAliases } from "vuetify"

const aliases: IconAliases = {
  calendar:              "fasl:calendar",
  cancel:                "fasl:xmark-large",
  checkboxIndeterminate: "fasl:square-minus",
  checkboxOff:           "fasl:square",
  checkboxOn:            "fasl:square-check",
  clear:                 "fasl:xmark-large",
  close:                 "fasl:xmark-large",
  collapse:              "fasl:chevron-up",
  complete:              "fasl:check",
  delete:                "fasl:xmark-large",
  delimiter:             "fasl:circle",
  dropdown:              "fasl:chevron-down",
  edit:                  "fasl:pencil",
  error:                 "fasl:xmark-large",
  expand:                "fasl:chevron-down",
  file:                  "fasl:paperclip",
  first:                 "fasl:backward-step",
  info:                  "fasl:circle-info",
  last:                  "fasl:forward-step",
  loading:               "fasl:arrows-rotate",
  menu:                  "fasl:bars",
  minus:                 "fasl:minus",
  next:                  "fasl:chevron-right",
  plus:                  "fasl:plus",
  prev:                  "fasl:chevron-left",
  radioOff:              "fasl:circle",
  radioOn:               "fasl:circle-dot",
  ratingEmpty:           "fasl:star-sharp",
  ratingFull:            "fasl:star-sharp-half-stroke",
  ratingHalf:            "fasl:star-sharp-half",
  sort:                  "fasl:arrow-up",
  sortAsc:               "fasl:arrow-up",
  sortDesc:              "fasl:arrow-down",
  subgroup:              "fasl:caret-down",
  success:               "fasl:circle-check",
  unfold:                "fasl:arrows-up-down",
  warning:               "fasl-circle-exclamation",
}

export const icons = {
  aliases,
  defaultSet: "fasl",
  sets:       {
    fab,
    fasl,
  },
}
