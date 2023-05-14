<script setup>
const themes = [
  {
    name: "system",
    icon: "fat-laptop",
  },
  {
    name: "light",
    icon: "fat-sun-bright",
  },
  {
    name: "dark",
    icon: "fat-moon",
  },
];
</script>

<template>
  <ThemeSwitcher :themes="themes" />
</template>
