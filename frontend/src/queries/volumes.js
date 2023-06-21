import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const volumes = createQueryKeys("volumes", {
  count: {
    queryFn: () => axios.get("/volumes/count/").then((res) => res.data),
  },
  list: (params) => ({
    queryKey: [params],
    queryFn: () =>
      axios
        .get("/volumes/", {
          params: params.value,
        })
        .then((res) => res.data),
  }),
  started: {
    queryFn: () => axios.get("/volumes/started/").then((res) => res.data),
  },
});
