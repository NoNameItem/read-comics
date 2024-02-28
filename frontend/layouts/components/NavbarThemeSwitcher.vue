<script setup lang="ts">
import type { ThemeSwitcherTheme } from "@layouts/types"

const themes: ThemeSwitcherTheme[] = [
  {
    icon: "fasl:laptop",
    name: "system",
  },
  {
    icon: "fasl:sun-bright",
    name: "light",
  },
  {
    icon: "fasl:moon",
    name: "dark",
  },
]
</script>

<template>
  <ThemeSwitcher :themes="themes" />
</template>
