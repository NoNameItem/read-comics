import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

export const storyArcs = createQueryKeys("storyArcs", {
  count: {
    queryFn: () => axios.get("/story-arcs/count/").then((res) => res.data),
  },
  started: {
    queryFn: () => axios.get("/story-arcs/started/").then((res) => res.data),
  },
});
