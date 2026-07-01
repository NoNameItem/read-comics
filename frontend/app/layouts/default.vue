<!-- Docs: [[docs/frontend/layouts/default.md]] -->
<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'
import { ref } from 'vue'

const open = ref(false)

const brand: NavigationMenuItem[] = [
  {
    label: 'Read Comics',
    to: '/',
    avatar: { src: '/images/logo.png', alt: 'RC', size: 'md', class: 'rounded-none' },
    active: false,
    ui: { linkLabel: 'text-xl text-primary' }
  }
]

const menuItems: NavigationMenuItem[] = [
  {
    label: 'Home',
    icon: 'i-lucide-house',
    to: '/',
    onSelect: () => {
      open.value = false
    }
  }
]
</script>

<template>
  <UDashboardGroup unit="rem">
    <UDashboardSidebar
      id="default"
      v-model:open="open"
      collapsible
      resizable
      class="bg-elevated/25"
      :ui="{ footer: 'lg:border-t lg:border-default' }"
    >
      <template #header="{ collapsed }">
        <UNavigationMenu
          :collapsed="collapsed"
          :items="brand"
          orientation="vertical"
          tooltip
          popover
        />
      </template>

      <template #default="{ collapsed }">
        <UDashboardSearchButton :collapsed="collapsed" class="bg-transparent ring-default" />

        <UNavigationMenu
          :collapsed="collapsed"
          :items="menuItems"
          orientation="vertical"
          tooltip
          popover
        />
      </template>

      <template #footer="{ collapsed }">
        <UserMenu :collapsed="collapsed" />
      </template>
    </UDashboardSidebar>

    <!--    <UDashboardSearch :groups="groups" /> -->
    <slot />
  </UDashboardGroup>
</template>
