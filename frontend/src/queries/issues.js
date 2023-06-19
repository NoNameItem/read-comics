import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const issues = createQueryKeys("issues", {
  count: {
    queryFn: () => axios.get("/issues/count/").then((res) => res.data),
  },
  list: (params) => ({
    queryKey: [params],
    queryFn: () =>
      axios
        .get("/issues/", {
          params: params.value,
        })
        .then((res) => res.data),
  }),
  detail: (slug, ordering) => ({
    queryKey: [slug, ordering],
    queryFn: () => axios.get(`issues/${slug}/`, { params: { ordering: ordering } }).then((res) => res.data),
    contextQueries: {
      technicalInfo: {
        queryKey: null,
        queryFn: () => axios.get(`issues/${slug}/technical-info/`).then((res) => res.data),
      },
    },
  }),
});
