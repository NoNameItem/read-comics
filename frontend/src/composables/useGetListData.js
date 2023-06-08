import { useQuery } from "@tanstack/vue-query";

export function useGetListData(query, defaultOrdering) {
  const route = useRoute();

  const showAll = computed(() => route.query["show-all"] ?? "no");
  const ordering = computed(() => route.query.ordering ?? defaultOrdering);
  const page = computed(() => route.query.page ?? 1);

  const { isLoading, isError, error, data } = useQuery(query(showAll, ordering, page));

  return { isLoading, isError, error, data };
}
