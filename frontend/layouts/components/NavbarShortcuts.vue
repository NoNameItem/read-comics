<script setup lang="ts">
const shortcuts = [
  {
    icon:     "tabler-calendar",
    subtitle: "Appointments",
    title:    "Calendar",
    to:       { name: "apps-calendar" },
  },
  {
    icon:     "tabler-file",
    subtitle: "Manage Accounts",
    title:    "Invoice App",
    to:       { name: "apps-invoice-list" },
  },
  {
    icon:     "tabler-user",
    subtitle: "Manage Users",
    title:    "Users",
    to:       { name: "apps-user-list" },
  },
  {
    icon:     "tabler-lock",
    subtitle: "Permission",
    title:    "Role Management",
    to:       { name: "apps-roles" },
  },
  {
    icon:     "tabler-layout-dashboard",
    subtitle: "Dashboard Analytics",
    title:    "Dashboard",
    to:       { name: "dashboards-analytics" },
  },
  {
    icon:     "tabler-settings",
    subtitle: "Account Settings",
    title:    "Settings",
    to:       { name: "pages-account-settings-tab", params: { tab: "account" } },
  },
]
</script>

<template>
  <Shortcuts :shortcuts="shortcuts" />
</template>
