import { useQuery } from "@tanstack/vue-query";
import { useUserStore } from "@/stores/user";

export function useAdminDetailQuery(query) {
  const user = useUserStore();

  const {
    isLoading,
    isError,
    error,
    data: requestData,
  } = user.isSuperuserOrStaff
    ? useQuery(query)
    : {
        isLoading: false,
        isError: false,
        error: null,
        data: ref(null),
      };

  const data = computed(() => (user.isSuperuserOrStaff ? requestData.value : null));

  return { isLoading, isError, error, data };
}
