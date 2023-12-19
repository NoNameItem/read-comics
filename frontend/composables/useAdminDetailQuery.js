import { useQuery } from "@tanstack/vue-query"
import { useUserStore } from "@/stores/user"

export function useAdminDetailQuery(query) {
  const user = useUserStore()

  const {
    isPending,
    isError,
    error,
    data: requestData,
  } = user.isSuperuserOrStaff
    ? useQuery(query)
    : {
        isPending: false,
        isError:   false,
        error:     null,
        data:      ref(null),
      }

  const data = computed(() => (user.isSuperuserOrStaff ? requestData.value : null))

  return { isPending, isError, error, data }
}
