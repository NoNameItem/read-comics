import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const teams = createQueryKeys("teams", {
  count: {
    queryFn: () => axios.get("/teams/count/").then((res) => res.data),
  },
  list: (params) => ({
    queryKey: [params],
    queryFn: () =>
      axios
        .get("/teams/", {
          params: params.value,
        })
        .then((res) => res.data),
  }),
});
