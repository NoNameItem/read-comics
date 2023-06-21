import axios from "@axios";
import { useUserStore } from "@/stores/user";

export function useResentEmailConfirmation() {
  const user = useUserStore();
  const toast = useTitledToast();

  async function resentConfirmation() {
    await axios.post("/auth/registration/resend-email/", { email: user.email });
    toast.success(`Confirmation resent to ${user.email}`, "Please, check your inbox");
  }

  return { resentConfirmation };
}
