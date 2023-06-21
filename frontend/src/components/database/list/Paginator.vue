<script setup>
const props = defineProps({
  length: {
    type: Number,
    required: true,
  },
});

const route = useRoute();
const router = useRouter();
const currentPage = ref(Number(route.query.page ?? "1"));

watch(route, () => (currentPage.value = Number(route.query.page ?? "1")));

watch(currentPage, () => {
  router.push({ name: route.name, query: { ...route.query, page: currentPage.value } });
});
</script>

<template>
  <VPagination
    v-model="currentPage"
    class="paginator ma-auto"
    variant="outlined"
    :length="props.length"
    :total-visible="15" />
</template>

<style lang="scss" scoped>
.paginator :deep(.v-btn--icon.v-btn--density-comfortable) {
  width: auto;
  min-width: calc(var(--v-btn-height) + 0px);

  .v-btn__content {
    margin: 5px;
  }
}
</style>
