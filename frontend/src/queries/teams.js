import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const teams = createQueryKeys("teams", {
  count: {
    queryFn: () => axios.get("/teams/count/").then((res) => res.data),
  },
});
