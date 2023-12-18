import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const missingIssues = createQueryKeys("missingIssues", {
  count: {
    queryFn: () => axios.get("/missing-issues/count/").then((res) => res.data),
  },
});
