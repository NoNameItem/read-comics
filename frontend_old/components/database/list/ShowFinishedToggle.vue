<script setup>
const route = useRoute()
const router = useRouter()

const hideFinished = ref((route.query["hide-finished"] ?? "yes") === "yes")

watch(hideFinished, () => {
  router.push({
    name:  route.name,
    query: {
      ...route.query,
      "hide-finished": hideFinished.value ? "yes" : "no",
      "page":          1,
    },
  })
})
</script>

<template>
  <VSwitch v-model="hideFinished" :inset="false" label="Hide finished" />
</template>
