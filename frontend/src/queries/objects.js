import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const objects = createQueryKeys("objects", {
  count: {
    queryFn: () => axios.get("/objects/count/").then((res) => res.data),
  },
});
