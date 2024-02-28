import { createQueryKeys } from "@lukemorales/query-key-factory"

export const useLocationKeys = () => {
  const axios = useAxios()

  return createQueryKeys("locations", {
    count:  { queryFn: () => axios.get("/locations/count/").then(res => res.data) },
    detail: slug => ({
      contextQueries: {
        technicalInfo: {
          queryFn:  () => axios.get(`/locations/${slug}/technical-info/`).then(res => res.data),
          queryKey: null,
        },
      },
      queryFn:  () => axios.get(`/locations/${slug}/`).then(res => res.data),
      queryKey: [slug],
    }),
    list: params => ({
      queryFn: () =>
        axios
          .get("/locations/", { params: params.value })
          .then(res => res.data),
      queryKey: [params],
    }),
  })
}
