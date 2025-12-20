import { createQueryKeys } from "@lukemorales/query-key-factory"

export const useCharacterKeys = () => {
  const axios = useAxios()

  return createQueryKeys("characters", {
    count:  { queryFn: () => axios.get("/characters/count/").then(res => res.data) },
    detail: slug => ({
      contextQueries: {
        technicalInfo: {
          queryFn:  () => axios.get(`/characters/${slug}/technical-info/`).then(res => res.data),
          queryKey: null,
        },
      },
      queryFn:  () => axios.get(`/characters/${slug}/`).then(res => res.data),
      queryKey: [slug],
    }),
    list: params => ({
      queryFn: () =>
        axios
          .get("/characters/", { params: params.value })
          .then(res => res.data),
      queryKey: [params],
    }),
  })
}
