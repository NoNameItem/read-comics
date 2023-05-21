<script setup>
import AuthProvider from "@/views/pages/authentication/AuthProvider.vue";
import authV1BottomShape from "@images/svg/auth-v1-bottom-shape.svg?raw";
import authV1TopShape from "@images/svg/auth-v1-top-shape.svg?raw";
import { VNodeRenderer } from "@layouts/components/VNodeRenderer";
import { themeConfig } from "@themeConfig";
import { useTitledToast } from "@/composables/titled-toast";
import { useUsersStore } from "@/stores/user";
import { requiredValidator } from "@validators";

const route = useRoute();
const router = useRouter();

const registerForm = ref(null);

const form = reactive({
  username: "",
  email: "",
  password: "",
  loading: false,
  valid: false,
  formErrors: null,
});

const backendErrors = ref({
  username: [],
  email: [],
  password1: [],
  non_field_errors: [],
});

const isPasswordVisible = ref(false);

const userStore = useUsersStore();

async function register() {
  form.loading = true;
  backendErrors.value = {
    username: [],
    email: [],
    password1: [],
    non_field_errors: [],
  };
  await registerForm.value.validate();
  if (!form.valid) {
    form.loading = false;
    return;
  }

  const toast = useTitledToast();
  const registerError = await userStore.register(form.username, form.email, form.password);

  if (registerError) {
    if (registerError?.response?.status === 400) {
      backendErrors.value = registerError.response.data;
    } else {
      toast.error("We experencing network troubles", "Please, try again later", { timeout: false });
    }
  } else {
    toast.success(`${userStore.username}, nice to meet you!`, "Hope you will like us...");
    // await router.replace(route.query.to ? String(route.query.to) : "/");
    await router.replace({ name: "verify-email", query: { to: route.query.to } });
  }
  form.loading = false;
}
</script>

<template>
  <div class="auth-wrapper d-flex align-center justify-center pa-4">
    <div class="position-relative my-sm-16">
      <!-- 👉 Top shape -->
      <VNodeRenderer
        :nodes="h('div', { innerHTML: authV1TopShape })"
        class="text-primary auth-v1-top-shape d-none d-sm-block"
      />

      <!-- 👉 Bottom shape -->
      <VNodeRenderer
        :nodes="h('div', { innerHTML: authV1BottomShape })"
        class="text-primary auth-v1-bottom-shape d-none d-sm-block"
      />

      <!-- 👉 Auth card -->
      <VCard class="auth-card pa-4" max-width="448">
        <VCardItem class="justify-center">
          <template #prepend>
            <div class="d-flex">
              <VNodeRenderer :nodes="themeConfig.app.logo" />
            </div>
          </template>

          <VCardTitle class="font-weight-bold text-h5 text-capitalize py-1">
            {{ themeConfig.app.title }}
          </VCardTitle>
        </VCardItem>

        <VCardText class="pt-2">
          <h5 class="text-h5 mb-1">Adventure starts here 🚀</h5>
        </VCardText>

        <VCardText>
          <VForm ref="registerForm" v-model="form.valid" @submit.prevent="register">
            <VRow>
              <!-- Username -->
              <VCol cols="12">
                <AppTextField
                  v-model="form.username"
                  autofocus
                  label="Username"
                  :rules="[requiredValidator]"
                  :error-messages="backendErrors.username"
                />
              </VCol>
              <!-- email -->
              <VCol cols="12">
                <AppTextField
                  v-model="form.email"
                  label="Email"
                  type="email"
                  :error-messages="backendErrors.email"
                  :rules="[requiredValidator]"
                />
              </VCol>

              <!-- password -->
              <VCol cols="12">
                <AppTextField
                  v-model="form.password"
                  label="Password"
                  :rules="[requiredValidator]"
                  :error-messages="backendErrors.password1"
                  :type="isPasswordVisible ? 'text' : 'password'"
                  :append-inner-icon="isPasswordVisible ? 'tabler-eye-off' : 'tabler-eye'"
                  @click:append-inner="isPasswordVisible = !isPasswordVisible"
                />
              </VCol>

              <FormErrors :error="false" :error-messages="backendErrors.non_field_errors"></FormErrors>

              <VCol cols="12" class="pt-1 pb-1">
                <VBtn block type="submit" :loading="form.loading">
                  Sign up
                  <VIcon end icon="fasl:arrow-right-to-bracket" />
                </VBtn>
              </VCol>

              <!-- login instead -->
              <VCol cols="12" class="text-center text-base">
                <span>Already have an account?</span>
                <RouterLink class="text-primary ms-2" :to="{ name: 'login', query: { to: route.query.to } }">
                  Sign in instead
                </RouterLink>
              </VCol>

              <VCol cols="12" class="d-flex align-center">
                <VDivider />
                <span class="mx-4">or</span>
                <VDivider />
              </VCol>

              <!-- auth providers -->
              <VCol cols="12" class="text-center">
                <AuthProvider />
              </VCol>
            </VRow>
          </VForm>
        </VCardText>
      </VCard>
    </div>
  </div>
</template>

<style lang="scss">
@use "@core/scss/template/pages/page-auth.scss";
</style>

<route lang="json">
{ "meta": { "layout": "blank" } }
</route>
