import { createQueryKeys } from "@lukemorales/query-key-factory"

export const useStoryArcKeys = () => {
  const axios = useAxios()

  return createQueryKeys("storyArcs", {
    count: { queryFn: () => axios.get("/story-arcs/count/").then(res => res.data) },
    list:  params => ({
      queryFn: () =>
        axios
          .get("/story-arcs/", { params: params.value })
          .then(res => res.data),
      queryKey: [params],
    }),
    started: { queryFn: () => axios.get("/story-arcs/started/").then(res => res.data) },
  })
}
