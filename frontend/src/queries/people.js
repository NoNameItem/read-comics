import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const people = createQueryKeys("people", {
  count: {
    queryFn: () => axios.get("/people/count/").then((res) => res.data),
  },
});
