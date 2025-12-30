<script setup lang="ts">
import type { DropdownMenuItem } from '@nuxt/ui'

defineProps<{
  collapsed?: boolean
}>()

const route = useRoute()
const userStore = useUserStore()

const user = computed(() => ({
  name: userStore.displayName,
  avatar: {
    src: userStore.thumbnail,
    alt: userStore.displayName
  }
}))

const handleLogout = async () => {
  // Check if the current page requires authentication or admin privileges
  const requiresAuth = route.meta?.loginRequired
  const requiresAdmin = route.meta?.staffRequired || route.meta?.superuserRequired

  await userStore.logout()

  // If page requires auth or admin privileges - redirect to login
  if (requiresAuth || requiresAdmin) {
    await navigateTo({
      path: '/users/login',
      query: { to: route.fullPath }
    })
  }
  // Otherwise stay on the current page
}

const items = computed<DropdownMenuItem[][]>(() => [
  [
    {
      type: 'label',
      label: user.value.name,
      avatar: user.value.avatar
    }
  ],
  [
    {
      label: 'Profile',
      icon: 'i-lucide-user'
    }
  ],
  [
    {
      label: 'Log out',
      icon: 'i-lucide-log-out',
      onSelect: handleLogout
    }
  ]
])
</script>

<template>
  <UDropdownMenu
    v-if="userStore.loggedIn"
    :items="items"
    :content="{ align: 'center', collisionPadding: 12 }"
    :ui="{ content: collapsed ? 'w-48' : 'w-(--reka-dropdown-menu-trigger-width)' }"
  >
    <UButton
      v-bind="{
        ...user,
        label: collapsed ? undefined : user.name || '',
        trailingIcon: collapsed ? undefined : 'i-lucide-chevrons-up-down'
      }"
      color="neutral"
      variant="ghost"
      block
      :square="collapsed"
      class="data-[state=open]:bg-elevated"
      :ui="{
        trailingIcon: 'text-dimmed'
      }"
    />

    <template #chip-leading="{ item }">
      <div class="inline-flex items-center justify-center shrink-0 size-5">
        <span
          class="rounded-full ring ring-bg bg-(--chip-light) dark:bg-(--chip-dark) size-2"
          :style="{
            '--chip-light': `var(--color-${(item as any).chip}-500)`,
            '--chip-dark': `var(--color-${(item as any).chip}-400)`
          }"
        />
      </div>
    </template>
  </UDropdownMenu>
  <UButton
    v-else
    v-bind="{
      label: collapsed ? undefined : 'Log in',
      trailingIcon: collapsed ? undefined : 'i-lucide-log-in',
      leadingIcon: collapsed ? 'i-lucide-log-in' : undefined
    }"
    color="neutral"
    variant="ghost"
    block
    :square="collapsed"
    :ui="{
      trailingIcon: 'text-dimmed',
      leadingIcon: 'text-dimmed'
    }"
    :to="{ path: '/users/login', query: { to: route.fullPath } }"
  />
</template>
