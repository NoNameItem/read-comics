import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const locations = createQueryKeys("locations", {
  count: {
    queryFn: () => axios.get("/locations/count/").then((res) => res.data),
  },
  list: (params) => ({
    queryKey: [params],
    queryFn: () =>
      axios
        .get("/locations/", {
          params: params.value,
        })
        .then((res) => res.data),
  }),
});
