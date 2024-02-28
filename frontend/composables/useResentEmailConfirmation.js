import { useUserStore } from "@/stores/user"

const axios = useAxios()

export function useResentEmailConfirmation() {
  const user = useUserStore()
  const toast = useTitledToast()

  async function resentConfirmation() {
    await axios.post("/auth/registration/resend-email/", { email: user.email })
    toast.success(`Confirmation resent to ${user.email}`, "Please, check your inbox")
  }

  return { resentConfirmation }
}
