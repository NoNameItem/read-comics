import { useUserStore } from "@/stores/user"
import { useQuery } from "@tanstack/vue-query"

export function useAdminDetailQuery(query) {
  const user = useUserStore()

  const {
    data: requestData,
    error,
    isError,
    isPending,
  } = user.isSuperuserOrStaff
    ? useQuery(query)
    : {
        data:      ref(null),
        error:     null,
        isError:   false,
        isPending: false,
      }

  const data = computed(() => (user.isSuperuserOrStaff ? requestData.value : null))

  return { data, error, isError, isPending }
}
