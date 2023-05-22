import axios from "@axios";

export function usePostForm({ url, formInitialValue, customConstructPostData, customProcessErrors }) {
  const formData = ref(formInitialValue ?? {});
  const valid = ref(true);
  const formRef = ref(null);
  const status = ref(null);
  const responseData = ref(null);
  const responseStatus = ref(null);

  const errors = ref({
    ...Object.keys(formData.value).reduce((acc, formElement) => ({ ...acc, [formElement]: [] }), {}),
    non_field_errors: [],
  });

  const loading = computed(() => status.value === "loading");

  async function post() {
    status.value = "loading";
    errors.value = {
      ...Object.keys(formData.value).reduce((acc, formElement) => ({ ...acc, [formElement]: [] }), {}),
      non_field_errors: [],
    };

    await formRef.value?.validate();
    if (!valid.value) {
      status.value = "validation_error";
      return;
    }

    const postBody = customConstructPostData ? customConstructPostData(formData.value) : formData.value;
    try {
      const response = await axios.post(url, postBody);

      responseData.value = await response.data;
      responseStatus.value = response.status;
      status.value = "success";
    } catch (e) {
      if (e?.response) {
        if (e.response.status === 403) {
          status.value = "auth_error";
        } else if (e.response.status === 400) {
          errors.value = customProcessErrors ? customProcessErrors(e.response.data) : e.response.data;
          status.value = "validation_error";
        }
      } else {
        status.value = "network_error";
      }
    }
  }

  return { formData, valid, formRef, status, loading, errors, responseData, responseStatus, post };
}
