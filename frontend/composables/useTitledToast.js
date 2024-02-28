import TitledToast from "@/components/TitledToast.vue"
import { useToast } from "vue-toastification"

export function useTitledToast() {
  const t = useToast()

  function toast(title, message, config) {
    t(
      {
        component: TitledToast,
        props:     {
          message,
          title,
        },
      },
      config,
    )
  }

  function info(title, message, config) {
    t.info(
      {
        component: TitledToast,
        props:     {
          message,
          title,
        },
      },
      config,
    )
  }

  function success(title, message, config) {
    t.success(
      {
        component: TitledToast,
        props:     {
          message,
          title,
        },
      },
      config,
    )
  }

  function warning(title, message, config) {
    t.warning(
      {
        component: TitledToast,
        props:     {
          message,
          title,
        },
      },
      config,
    )
  }

  function error(title, message, config) {
    t.error(
      {
        component: TitledToast,
        props:     {
          message,
          title,
        },
      },
      config,
    )
  }

  return {
    error,
    info,
    success,
    toast,
    warning,
  }
}
