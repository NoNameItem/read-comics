<script setup>
import { useUserStore } from "@/stores/user";
import F from "@images/avatars/F_thumb.png";
import M from "@images/avatars/M_thumb.png";
import O from "@images/avatars/O_thumb.png";
import U from "@images/avatars/U_thumb.png";

const userStore = useUserStore();
const route = useRoute();

const images = {
  F: F,
  M: M,
  O: O,
  U: U,
};
</script>

<template>
  <VBtn
    v-if="!userStore.username"
    color="primary"
    variant="text"
    :to="{ path: 'login', query: { to: route.fullPath } }">
    Login
    <VIcon end icon="fasl:arrow-right-to-bracket" />
  </VBtn>
  <VBadge v-else dot location="bottom right" offset-x="3" offset-y="3" bordered color="success">
    <VAvatar class="cursor-pointer avatar" color="primary" variant="tonal">
      <VImg :src="userStore.thumbnail" class="bg-white" />

      <!-- SECTION Menu -->
      <VMenu activator="parent" width="230" location="bottom end" offset="14px">
        <VList>
          <!-- 👉 User Avatar & Name -->
          <VListItem>
            <template #prepend>
              <VListItemAction start>
                <VBadge dot location="bottom right" offset-x="3" offset-y="3" color="success">
                  <VAvatar class="avatar" color="primary" variant="tonal">
                    <VImg :src="userStore.thumbnail" />
                  </VAvatar>
                </VBadge>
              </VListItemAction>
            </template>

            <VListItemTitle class="font-weight-semibold"> {{ userStore.name }}</VListItemTitle>
            <VListItemSubtitle>@{{ userStore.username }}</VListItemSubtitle>
          </VListItem>

          <VDivider class="my-2" />

          <!-- 👉 Profile -->
          <VListItem to="profile">
            <template #prepend>
              <VIcon class="me-2" icon="fasl:user" size="22" />
            </template>

            <VListItemTitle>Profile</VListItemTitle>
          </VListItem>

          <!-- Divider -->
          <VDivider class="my-2" />

          <!-- 👉 Logout -->
          <VListItem @click="userStore.logout">
            <template #prepend>
              <VIcon class="me-2" icon="fasl:arrow-right-from-bracket" size="22" />
            </template>

            <VListItemTitle>Logout</VListItemTitle>
          </VListItem>
        </VList>
      </VMenu>
      <!-- !SECTION -->
    </VAvatar>
  </VBadge>
</template>

<style>
.avatar .v-img__img {
  background-color: white;
}
</style>
