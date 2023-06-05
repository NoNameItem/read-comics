import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const characters = createQueryKeys("characters", {
  count: {
    queryFn: () => axios.get("/characters/count/").then((res) => res.data),
  },
});
