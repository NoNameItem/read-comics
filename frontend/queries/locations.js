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
  detail: (slug) => ({
    queryKey: [slug],
    queryFn: () => axios.get(`/locations/${slug}/`).then((res) => res.data),
    contextQueries: {
      technicalInfo: {
        queryKey: null,
        queryFn: () => axios.get(`/locations/${slug}/technical-info/`).then((res) => res.data),
      },
    },
  }),
});
