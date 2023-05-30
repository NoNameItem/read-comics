import { createQueryKeys } from "@lukemorales/query-key-factory";
import axios from "@axios";

const PROFILE_URL = "/profile/";
const FINISHED_STATS_URL = "/profile/finished-stats/";

export const profile = createQueryKeys("profile", {
  profileData: {
    queryFn: () => axios.get(PROFILE_URL).then((res) => res.data),
  },
  finishedStats: {
    queryFn: () => axios.get(FINISHED_STATS_URL).then((res) => res.data),
  },
});
