<script setup>
import { useTheme } from "vuetify";

const { global } = useTheme();

const authProviders = [
  {
    icon: "fab:facebook",
    color: "#4267b2",
  },
  {
    icon: "fab:google",
    color: "#dd4b39",
  },
  {
    icon: "fab:twitter",
    color: "#1da1f2",
  },
];
</script>

<template>
  <div class="d-flex justify-center flex-wrap gap-3">
    <VBtn
      v-for="link in authProviders"
      :key="link.icon"
      icon
      variant="tonal"
      size="38"
      :color="global.name.value === 'dark' ? link.colorInDark : link.color"
      class="rounded"
    >
      <VIcon size="18" :icon="link.icon" />
    </VBtn>
  </div>
</template>
