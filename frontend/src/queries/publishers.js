import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const publishers = createQueryKeys("publishers", {
  count: {
    queryFn: () => axios.get("/publishers/count/").then((res) => res.data),
  },
});
