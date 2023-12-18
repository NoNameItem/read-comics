import type { IconAliases } from 'vuetify'
import { fasl } from '@/plugins/iconsets/fasl'
import { fab } from '@/plugins/iconsets/fab'

const aliases: IconAliases = {
  calendar: 'fasl:calendar',
  collapse: 'fasl:chevron-up',
  complete: 'fasl:check',
  cancel: 'fasl:xmark-large',
  close: 'fasl:xmark-large',
  delete: 'fasl:xmark-large',
  clear: 'fasl:xmark-large',
  success: 'fasl:circle-check',
  info: 'fasl:circle-info',
  warning: 'fasl-circle-exclamation',
  error: 'fasl:xmark-large',
  prev: 'fasl:chevron-left',
  next: 'fasl:chevron-right',
  checkboxOn: 'fasl:square-check',
  checkboxOff: 'fasl:square',
  checkboxIndeterminate: 'fasl:square-minus',
  delimiter: 'fasl:circle',
  sort: 'fasl:arrow-up',
  expand: 'fasl:chevron-down',
  menu: 'fasl:bars',
  subgroup: 'fasl:caret-down',
  dropdown: 'fasl:chevron-down',
  radioOn: 'fasl:circle-dot',
  radioOff: 'fasl:circle',
  edit: 'fasl:pencil',
  ratingEmpty: 'fasl:star-sharp',
  ratingFull: 'fasl:star-sharp-half-stroke',
  ratingHalf: 'fasl:star-sharp-half',
  loading: 'fasl:arrows-rotate',
  first: 'fasl:backward-step',
  last: 'fasl:forward-step',
  unfold: 'fasl:arrows-up-down',
  file: 'fasl:paperclip',
  plus: 'fasl:plus',
  minus: 'fasl:minus',
  sortAsc: 'fasl:arrow-up',
  sortDesc: 'fasl:arrow-down',
}

export const icons = {
  defaultSet: 'fasl',
  aliases,
  sets: {
    fasl,
    fab,
  },
}
