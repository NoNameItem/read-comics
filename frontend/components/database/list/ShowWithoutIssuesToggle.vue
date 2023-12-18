<script setup>
const props = defineProps({
  label: {
    type: String,
    required: true,
  },
});

const route = useRoute();
const router = useRouter();

const showAll = ref((route.query["show-all"] ?? "no") === "no");

watch(showAll, () => {
  router.push({
    name: route.name,
    query: {
      ...route.query,
      page: 1,
      "show-all": showAll.value ? "no" : "yes",
    },
  });
});
</script>

<template>
  <VSwitch v-model="showAll" :inset="false" :label="`Show only ${props.label} with issues`" />
</template>
