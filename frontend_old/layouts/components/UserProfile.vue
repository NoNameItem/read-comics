<script setup>
const userStore = useUserStore()
const route = useRoute()
</script>

<template>
  <VBtn
    v-if="!userStore.username"
    :to="{ path: '/login', query: { to: route.fullPath } }"
    color="primary"
    variant="text"
  >
    Login
    <VIcon
      end
      icon="fasl:arrow-right-to-bracket"
    />
  </VBtn>
  <VBadge
    v-else
    bordered
    color="success"
    dot
    location="bottom right"
    offset-x="3"
    offset-y="3"
  >
    <VAvatar
      class="cursor-pointer avatar"
      color="primary"
      variant="tonal"
    >
      <VImg
        :src="userStore.thumbnail"
        class="bg-white"
      />

      <!-- SECTION Menu -->
      <VMenu
        activator="parent"
        location="bottom end"
        offset="14px"
        width="230"
      >
        <VList>
          <!-- 👉 User Avatar & Name -->
          <VListItem>
            <template #prepend>
              <VListItemAction start>
                <VBadge
                  color="success"
                  dot
                  location="bottom right"
                  offset-x="3"
                  offset-y="3"
                >
                  <VAvatar
                    class="avatar"
                    color="primary"
                    variant="tonal"
                  >
                    <VImg :src="userStore.thumbnail" />
                  </VAvatar>
                </VBadge>
              </VListItemAction>
            </template>

            <VListItemTitle class="font-weight-semibold">
              {{ userStore.name }}
            </VListItemTitle>
            <VListItemSubtitle>@{{ userStore.username }}</VListItemSubtitle>
          </VListItem>

          <VDivider class="my-2" />

          <!-- 👉 Profile -->
          <VListItem to="/profile">
            <template #prepend>
              <VIcon
                class="me-2"
                icon="fasl:user"
                size="22"
              />
            </template>

            <VListItemTitle>Profile</VListItemTitle>
          </VListItem>

          <!-- Divider -->
          <VDivider class="my-2" />

          <!-- 👉 Logout -->
          <VListItem @click="userStore.logout">
            <template #prepend>
              <VIcon
                class="me-2"
                icon="fasl:arrow-right-from-bracket"
                size="22"
              />
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
