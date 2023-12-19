<script setup lang="ts">
import type { ThemeSwitcherTheme } from "@layouts/types"

const themes: ThemeSwitcherTheme[] = [
  {
    name: "system",
    icon: "fasl:laptop",
  },
  {
    name: "light",
    icon: "fasl:sun-bright",
  },
  {
    name: "dark",
    icon: "fasl:moon",
  },
]
</script>

<template>
  <ThemeSwitcher :themes="themes" />
</template>
