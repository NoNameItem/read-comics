import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const concepts = createQueryKeys("concepts", {
  count: {
    queryFn: () => axios.get("/concepts/count/").then((res) => res.data),
  },
  list: (showAll, ordering, page) => ({
    queryKey: [showAll, ordering, page],
    queryFn: () =>
      axios
        .get("/concepts/", {
          params: {
            ordering: ordering.value,
            page: page.value,
            "show-all": showAll.value,
          },
        })
        .then((res) => res.data),
  }),
});
