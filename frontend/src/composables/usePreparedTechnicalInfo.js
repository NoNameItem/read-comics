import { useAdminDetailQuery } from "@/composables/useAdminDetailQuery";
import { formatDateTimeSeconds } from "@/utils/format_utils";

export function usePreparedTechnicalInfo(query) {
  const { isLoading, data } = useAdminDetailQuery(query);

  const preparedTechnicalInfo = computed(() =>
    data.value
      ? [
          {
            title: "ID",
            value: data.value?.id,
          },
          {
            title: "ComicVine ID",
            value: data.value?.comicvine_id,
          },
          {
            title: "ComicVine Status",
            value: data.value?.comicvine_status,
          },
          {
            title: "ComicVine last match",
            value: formatDateTimeSeconds(data.value?.comicvine_last_match),
          },
          {
            title: "Created",
            value: formatDateTimeSeconds(data.value?.created_dt),
          },
          {
            title: "Modified",
            value: formatDateTimeSeconds(data.value?.modified_dt),
          },
        ]
      : null
  );

  return { isLoading, preparedTechnicalInfo };
}
