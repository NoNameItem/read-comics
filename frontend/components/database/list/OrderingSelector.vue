<script setup>
const componentProps = defineProps({
  variants: { type: Array, required: true },
  defaultOrdering: { type: String, required: true },
});

const route = useRoute();
const router = useRouter();

const setOrdering = (ordering) => {
  router.push({ name: route.name, query: { ...route.query, page: 1, ordering: ordering } });
};

const currentOrdering = computed(() => route.query.ordering ?? componentProps.defaultOrdering);
</script>

<template>
  <VMenu>
    <template #activator="{ props }">
      <VBtn color="primary" v-bind="props"> Order By</VBtn>
    </template>

    <VList density="compact">
      <VListItem
        v-for="item in componentProps.variants"
        :key="item.value"
        :value="item.value"
        :active="item.value === currentOrdering"
        @click="setOrdering(item.value)">
        <template #prepend>
          <VIcon :icon="item.icon"></VIcon>
        </template>
        <VListItemTitle>{{ item.title }}</VListItemTitle>
      </VListItem>
    </VList>
  </VMenu>
</template>
