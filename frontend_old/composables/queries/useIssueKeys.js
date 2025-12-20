import { createQueryKeys } from "@lukemorales/query-key-factory"

export const useIssueKeys = () => {
  const axios = useAxios()

  return createQueryKeys("issues", {
    count:  { queryFn: () => axios.get("/issues/count/").then(res => res.data) },
    detail: (slug, ordering) => ({
      contextQueries: {
        technicalInfo: {
          queryFn:  () => axios.get(`/issues/${slug}/technical-info/`).then(res => res.data),
          queryKey: null,
        },
      },
      queryFn:  () => axios.get(`/issues/${slug}/`, { params: { ordering } }).then(res => res.data),
      queryKey: [slug, ordering],
    }),
    list: params => ({
      queryFn: () =>
        axios
          .get("/issues/", { params: params.value })
          .then(res => res.data),
      queryKey: [params],
    }),
  })
}
