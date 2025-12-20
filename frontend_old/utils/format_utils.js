import { DateTime } from "luxon"

export function utilsFormatDate(dttmString) {
  return dttmString ? DateTime.fromISO(dttmString).setLocale("en-us").toLocaleString(DateTime.DATE_FULL) : ""
}

export function formatDateTimeMinutes(dttmString) {
  return dttmString ? DateTime.fromISO(dttmString).setLocale("en-us").toLocaleString(DateTime.DATETIME_FULL) : ""
}

export function formatDateTimeSeconds(dttmString) {
  return dttmString ? DateTime.fromISO(dttmString).setLocale("en-us").toLocaleString(DateTime.DATETIME_FULL_WITH_SECONDS) : ""
}
