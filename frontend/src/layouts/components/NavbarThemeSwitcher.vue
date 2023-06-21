<script setup>
const themes = [
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
];
</script>

<template>
  <ThemeSwitcher :themes="themes" />
</template>
