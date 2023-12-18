<script setup>
const route = useRoute();
const router = useRouter();

const hideFinished = ref((route.query["hide-finished"] ?? "yes") === "yes");

watch(hideFinished, () => {
  router.push({
    name: route.name,
    query: {
      ...route.query,
      page: 1,
      "hide-finished": hideFinished.value ? "yes" : "no",
    },
  });
});
</script>

<template>
  <VSwitch v-model="hideFinished" :inset="false" label="Hide finished" />
</template>
