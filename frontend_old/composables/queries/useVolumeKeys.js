import { createQueryKeys } from "@lukemorales/query-key-factory"

export const useVolumeKeys = () => {
  const axios = useAxios()

  return createQueryKeys("volumes", {
    count: { queryFn: () => axios.get("/volumes/count/").then(res => res.data) },
    list:  params => ({
      queryFn: () =>
        axios
          .get("/volumes/", { params: params.value })
          .then(res => res.data),
      queryKey: [params],
    }),
    started: { queryFn: () => axios.get("/volumes/started/").then(res => res.data) },
  })
}
