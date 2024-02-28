import { createQueryKeys } from "@lukemorales/query-key-factory"

export const useConceptKeys = () => {
  const axios = useAxios()

  return createQueryKeys("concepts", {
    count:  { queryFn: () => axios.get("/concepts/count/").then(res => res.data) },
    detail: slug => ({
      contextQueries: {
        technicalInfo: {
          queryFn:  () => axios.get(`/concepts/${slug}/technical-info/`).then(res => res.data),
          queryKey: null,
        },
      },
      queryFn:  () => axios.get(`/concepts/${slug}/`).then(res => res.data),
      queryKey: [slug],
    }),
    list: params => ({
      queryFn: () =>
        axios
          .get("/concepts/", { params: params.value })
          .then(res => res.data),
      queryKey: [params],
    }),
  })
}
