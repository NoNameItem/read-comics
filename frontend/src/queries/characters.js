import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const characters = createQueryKeys("characters", {
  count: {
    queryFn: () => axios.get("/characters/count/").then((res) => res.data),
  },
  list: (showAll, ordering, page) => ({
    queryKey: [showAll, ordering, page],
    queryFn: () =>
      axios
        .get("/characters/", {
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
    queryFn: () => axios.get(`characters/${slug}/`).then((res) => res.data),
    contextQueries: {
      technicalInfo: {
        queryKey: null,
        queryFn: () => axios.get(`characters/${slug}/technical-info/`).then((res) => res.data),
      },
    },
  }),
});
