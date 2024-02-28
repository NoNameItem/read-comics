import { createQueryKeys } from "@lukemorales/query-key-factory"

export const usePublisherKeys = () => {
  const axios = useAxios()

  return createQueryKeys("publishers", {
    count: { queryFn: () => axios.get("/publishers/count/").then(res => res.data) },
    list:  params => ({
      queryFn: () =>
        axios
          .get("/publishers/", { params: params.value })
          .then(res => res.data),
      queryKey: [params],
    }),
  })
}
