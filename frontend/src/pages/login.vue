<script setup>
import authV1BottomShape from "@images/svg/auth-v1-bottom-shape.svg?raw";
import authV1TopShape from "@images/svg/auth-v1-top-shape.svg?raw";
import { VNodeRenderer } from "@layouts/components/VNodeRenderer";
import { themeConfig } from "@themeConfig";
import { useUserStore } from "@/stores/user";
import { requiredValidator } from "@validators";
import { useTitledToast } from "@/composables/useTitledToast";

const htmlTitle = useTitle();

htmlTitle.value = "Login";

const form = reactive({
  username: "",
  password: "",
  loading: false,
  valid: false,
  formErrors: null,
});

const isPasswordVisible = ref(false);
const loginForm = ref(null);

const userStore = useUserStore();
const route = useRoute();
const router = useRouter();

async function login() {
  form.loading = true;
  form.formErrors = null;
  await loginForm.value.validate();
  if (!form.valid) {
    form.loading = false;
    return;
  }

  const toast = useTitledToast();
  const loginError = await userStore.login(form.username, form.password);

  userStore.$persist();

  if (loginError) {
    if (loginError?.response?.status === 400) {
      toast.error("Bad credentials", "");
      form.formErrors = loginError.response.data.non_field_errors;
    } else {
      toast.error("We experencing network troubles", "Please, try again later", { timeout: false });
    }
  } else {
    toast.success(`${userStore.name || userStore.username}, welcome back!`, "We missed you...");
    await router.replace(route.query.to ? String(route.query.to) : "/");
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
        class="text-primary auth-v1-top-shape d-none d-sm-block" />

      <!-- 👉 Bottom shape -->
      <VNodeRenderer
        :nodes="h('div', { innerHTML: authV1BottomShape })"
        class="text-primary auth-v1-bottom-shape d-none d-sm-block" />

      <!-- 👉 Auth Card -->
      <VCard class="auth-card pa-4" max-width="448">
        <VCardItem class="justify-center">
          <template #prepend>
            <div class="d-flex">
              <VNodeRenderer :nodes="themeConfig.app.logo" />
            </div>
          </template>

          <VCardTitle class="font-weight-bold text-capitalize text-h5 py-1">
            {{ themeConfig.app.title }}
          </VCardTitle>
        </VCardItem>

        <VCardText class="pt-1">
          <h5 class="text-h5 mb-1">
            Welcome to <span class="text-capitalize">{{ themeConfig.app.title }}</span
            >! 👋🏻
          </h5>
          <p class="mb-0">Please sign-in to your account and start the adventure</p>
        </VCardText>

        <VCardText>
          <VForm ref="loginForm" v-model="form.valid" @submit.prevent="login">
            <VRow>
              <!-- username -->
              <VCol cols="12">
                <AppTextField v-model="form.username" autofocus label="Username" :rules="[requiredValidator]" />
              </VCol>

              <!-- password -->
              <VCol cols="12">
                <AppTextField
                  v-model="form.password"
                  label="Password"
                  :type="isPasswordVisible ? 'text' : 'password'"
                  :append-inner-icon="isPasswordVisible ? 'fasl:eye-slash' : 'fasl:eye'"
                  :rules="[requiredValidator]"
                  @click:append-inner="isPasswordVisible = !isPasswordVisible" />
              </VCol>

              <FormErrors :error="false" :error-messages="form.formErrors"></FormErrors>

              <VCol cols-12 class="pt-1 pb-1">
                <RouterLink class="text-primary ms-2 mb-1" :to="{ name: 'reset-password' }">
                  Forgot Password?
                </RouterLink>
              </VCol>

              <VCol cols="12" class="pt-1 pb-1">
                <VBtn block type="submit" color="primary" :loading="form.loading">
                  Login
                  <VIcon end icon="fasl:arrow-right-to-bracket" />
                </VBtn>
              </VCol>

              <!-- create account -->
              <VCol cols="12" class="text-center text-base">
                <span>New on our platform?</span>
                <RouterLink class="text-primary ms-2" :to="{ name: 'register', query: route.query }">
                  Create an account
                </RouterLink>
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

<route lang="yaml">
{ "meta": { "layout": "blank" } }
</route>
