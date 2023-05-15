import { useToast } from "vue-toastification";
import TitledToast from "@/components/TitledToast.vue";

export function useTitledToast() {
  const t = useToast();

  function toast(title, message, config) {
    t(
      {
        component: TitledToast,
        props: {
          title: title,
          message: message,
        },
      },
      config
    );
  }

  function info(title, message, config) {
    t.info(
      {
        component: TitledToast,
        props: {
          title: title,
          message: message,
        },
      },
      config
    );
  }

  function success(title, message, config) {
    t.success(
      {
        component: TitledToast,
        props: {
          title: title,
          message: message,
        },
      },
      config
    );
  }

  function warning(title, message, config) {
    t.warning(
      {
        component: TitledToast,
        props: {
          title: title,
          message: message,
        },
      },
      config
    );
  }

  function error(title, message, config) {
    t.error(
      {
        component: TitledToast,
        props: {
          title: title,
          message: message,
        },
      },
      config
    );
  }

  return {
    toast,
    info,
    success,
    warning,
    error,
  };
}
