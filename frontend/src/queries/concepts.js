import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const concepts = createQueryKeys("concepts", {
  count: {
    queryFn: () => axios.get("/concepts/count/").then((res) => res.data),
  },
});
