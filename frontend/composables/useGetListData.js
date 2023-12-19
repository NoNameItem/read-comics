import { useQuery } from "@tanstack/vue-query"

export function useGetListData(query, defaultParams) {
  const route = useRoute()

  const params = computed(() => {
    const filteredQuery = {}
    for (const key in route.query) {
      if (key in defaultParams)
        filteredQuery[key] = route.query[key]
    }

    return {
      ...defaultParams,
      ...filteredQuery,
    }
  })

  const { isPending, isError, error, data, suspense } = useQuery(query(params))

  return { isPending, isError, error, data, suspense }
}
