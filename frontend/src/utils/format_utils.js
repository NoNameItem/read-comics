import { DateTime } from "luxon";

export function formatDate(dttmString) {
  return dttmString ? DateTime.fromISO(dttmString).toLocaleString(DateTime.DATE_FULL) : "";
}

export function formatDateTimeMinutes(dttmString) {
  return dttmString ? DateTime.fromISO(dttmString).toLocaleString(DateTime.DATETIME_FULL) : "";
}

export function formatDateTimeSeconds(dttmString) {
  return dttmString ? DateTime.fromISO(dttmString).toLocaleString(DateTime.DATETIME_FULL_WITH_SECONDS) : "";
}
