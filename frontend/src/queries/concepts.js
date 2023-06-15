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
  detail: (slug) => ({
    queryKey: [slug],
    queryFn: () => axios.get(`concepts/${slug}/`).then((res) => res.data),
    contextQueries: {
      technicalInfo: {
        queryKey: null,
        queryFn: () => axios.get(`concepts/${slug}/technical-info/`).then((res) => res.data),
      },
    },
  }),
});
