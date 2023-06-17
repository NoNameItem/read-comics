import { DateTime } from "luxon";

export function formatDate(dttmString) {
  return dttmString ? DateTime.fromISO(dttmString).toLocaleString(DateTime.DATE_FULL) : "";
}

export function formatDateTimeMinutes(dttmString) {
  return dttmString ? DateTime.fromISO(dttmString).toLocaleString(DateTime.DATETIME_SHORT) : "";
}

export function formatDateTimeSeconds(dttmString) {
  return dttmString ? DateTime.fromISO(dttmString).toLocaleString(DateTime.DATETIME_SHORT_WITH_SECONDS) : "";
}
