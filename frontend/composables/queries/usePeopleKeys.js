import { createQueryKeys } from "@lukemorales/query-key-factory"

export const usePeopleKeys = () => {
  const axios = useAxios()

  return createQueryKeys("people", {
    count: { queryFn: () => axios.get("/people/count/").then(res => res.data) },
    list:  params => ({
      queryFn: () =>
        axios
          .get("/people/", { params: params.value })
          .then(res => res.data),
      queryKey: [params],
    }),
  })
}
