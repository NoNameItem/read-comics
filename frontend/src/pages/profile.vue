<script setup>
import { VSkeletonLoader } from "vuetify/labs/VSkeletonLoader";
import { useQuery } from "@tanstack/vue-query";
import { queries } from "@/queries";

const route = useRoute();
const userTab = ref(null);

const tabs = [
  {
    icon: "fasl:user",
    title: "Info",
  },
  {
    icon: "fasl:lock",
    title: "Security",
  },
];

const { isLoading, isError, error, data } = useQuery(queries.profile.profileData);
</script>

<template>
  <VRow>
    <UserInfoPanel />

    <VCol cols="12" md="7" lg="8" xl="9" xxl="10">
      <VTabs v-model="userTab" class="v-tabs-pill">
        <VTab v-for="tab in tabs" :key="tab.icon">
          <VIcon :size="18" :icon="tab.icon" class="me-1" />
          <span>{{ tab.title }}</span>
        </VTab>
      </VTabs>

      <VWindow v-model="userTab" class="mt-6 disable-tab-transition fullscreen" :touch="false">
        <VWindowItem>
          <VSkeletonLoader type="paragraph" :loading="isLoading" style="background: transparent">
            <p v-if="data?.bio" class="bio">{{ data?.bio }}</p>
          </VSkeletonLoader>
        </VWindowItem>

        <VWindowItem>
          <UserTabSecurity />
        </VWindowItem>
      </VWindow>
    </VCol>
  </VRow>
</template>

<style scoped>
p.bio {
  white-space: pre-wrap;
}

.fullscreen .v-window-container {
  height: 100px;
  overflow-y: scroll;
}
</style>

<route lang="yaml">
{ "meta": { "loginRequired": true } }
</route>
