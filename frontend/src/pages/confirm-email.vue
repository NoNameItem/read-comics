<script setup>
import authV1BottomShape from "@images/svg/auth-v1-bottom-shape.svg?raw";
import authV1TopShape from "@images/svg/auth-v1-top-shape.svg?raw";
import { VNodeRenderer } from "@layouts/components/VNodeRenderer";
import { themeConfig } from "@themeConfig";
import { useUsersStore } from "@/stores/user";
import axios from "@axios";

const user = useUsersStore();
const route = useRoute();
const loading = ref(true);

async function confimEmail() {
  await axios.post("/auth/registration/verify-email/", { key: route.query.key });
  loading.value = false;
}

onMounted(confimEmail);
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
      <VCard class="auth-card pa-4" max-width="448" :loading="loading">
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

        <VCardText v-if="loading" class="pt-2">
          <h5 class="text-h5 mb-1">Verifying your email</h5>
          <p>It can take few seconds. Please be patient.</p>
        </VCardText>
        <VCardText v-else class="pt-2">
          <h5 class="text-h5 mb-1">Your email verified</h5>
          <p>Your email address {{ user.email }} verified.</p>

          <VBtn block to="/" class="mb-6"> Start reading </VBtn>
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
