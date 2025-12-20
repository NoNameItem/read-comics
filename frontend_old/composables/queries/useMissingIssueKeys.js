import { createQueryKeys } from "@lukemorales/query-key-factory"

export const useMissingIssueKeys = () => {
  const axios = useAxios()

  return createQueryKeys("missingIssues", { count: { queryFn: () => axios.get("/missing-issues/count/").then(res => res.data) } })
}
