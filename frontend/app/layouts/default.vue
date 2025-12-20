<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'
import { ref } from 'vue'

const open = ref(false)

const breadcrumb = useBreadcrumbsStore()

const bredcrumbItems = ref([
  {
    label: 'Docs',
    to: '/docs'
  },
  {
    label: 'Components',
    to: '/docs/components'
  },
  {
    label: 'Breadcrumb',
    to: '/docs/components/breadcrumb'
  }
])

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
  },
  {
    label: 'Inbox',
    icon: 'i-lucide-inbox',
    to: '/inbox',
    badge: '4',
    onSelect: () => {
      open.value = false
    }
  },
  {
    label: 'Customers',
    icon: 'i-lucide-users',
    to: '/customers',
    onSelect: () => {
      open.value = false
    }
  },
  {
    label: 'Settings',
    to: '/settings',
    icon: 'i-lucide-settings',
    defaultOpen: true,
    type: 'trigger',
    children: [
      {
        label: 'General',
        to: '/settings',
        exact: true,
        onSelect: () => {
          open.value = false
        }
      },
      {
        label: 'Members',
        to: '/settings/members',
        onSelect: () => {
          open.value = false
        }
      },
      {
        label: 'Notifications',
        to: '/settings/notifications',
        onSelect: () => {
          open.value = false
        }
      },
      {
        label: 'Security',
        to: '/settings/security',
        onSelect: () => {
          open.value = false
        }
      }
    ]
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

    <!--    <UDashboardSearch :groups="groups" />-->
    <slot />
  </UDashboardGroup>
</template>
