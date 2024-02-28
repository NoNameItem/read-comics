<script setup>
const componentProps = defineProps({
  defaultOrdering: { required: true, type: String },
  variants:        { required: true, type: Array },
})

const route = useRoute()
const router = useRouter()

const setOrdering = (ordering) => {
  router.push({ name: route.name, query: { ...route.query, ordering, page: 1 } })
}

const currentOrdering = computed(() => route.query.ordering ?? componentProps.defaultOrdering)
</script>

<template>
  <VMenu>
    <template #activator="{ props }">
      <VBtn color="primary" v-bind="props">
        Order By
      </VBtn>
    </template>

    <VList density="compact">
      <VListItem
        v-for="item in componentProps.variants"
        :key="item.value"
        :active="item.value === currentOrdering"
        :value="item.value"
        @click="setOrdering(item.value)"
      >
        <template #prepend>
          <VIcon :icon="item.icon" />
        </template>
        <VListItemTitle>{{ item.title }}</VListItemTitle>
      </VListItem>
    </VList>
  </VMenu>
</template>
