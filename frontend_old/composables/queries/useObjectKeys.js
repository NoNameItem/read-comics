import { createQueryKeys } from "@lukemorales/query-key-factory"

export const useObjectKeys = () => {
  const axios = useAxios()

  return createQueryKeys("objects", {
    count: { queryFn: () => axios.get("/objects/count/").then(res => res.data) },
    list:  params => ({
      queryFn: () =>
        axios
          .get("/objects/", { params: params.value })
          .then(res => res.data),
      queryKey: [params],
    }),
  })
}
