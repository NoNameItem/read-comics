import { createQueryKeys } from "@lukemorales/query-key-factory"

export const useTeamKeys = () => {
  const axios = useAxios()

  return createQueryKeys("teams", {
    count: { queryFn: () => axios.get("/teams/count/").then(res => res.data) },
    list:  params => ({
      queryFn: () =>
        axios
          .get("/teams/", { params: params.value })
          .then(res => res.data),
      queryKey: [params],
    }),
  })
}
