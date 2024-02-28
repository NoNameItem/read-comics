import { createQueryKeys } from "@lukemorales/query-key-factory"

export const useProfileKeys = () => {
  const axios = useAxios()

  return createQueryKeys("profile", {
    finishedStats: { queryFn: () => axios.get("/profile/finished-stats/").then(res => res.data) },
    profileData:   { queryFn: () => axios.get("/profile/").then(res => res.data) },
  })
}
