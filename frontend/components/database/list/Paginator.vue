<script setup>
const props = defineProps({
  length: {
    required: true,
    type:     Number,
  },
})

const route = useRoute()
const router = useRouter()
const currentPage = ref(Number(route.query.page ?? "1"))

watch(route, () => (currentPage.value = Number(route.query.page ?? "1")))

watch(currentPage, () => {
  router.push({ name: route.name, query: { ...route.query, page: currentPage.value } })
})

const scrollToTop = () => {
  setTimeout(() => {
    window.scrollTo({
      behavior: "instant",
      top:      0,
    })
  }, 200)
}
</script>

<template>
  <VPagination
    v-model="currentPage"
    :length="props.length"
    :total-visible="15"
    class="paginator ma-auto"
    variant="outlined"
    @update:model-value="scrollToTop"
  />
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
