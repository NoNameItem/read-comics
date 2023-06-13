<script setup>
const props = defineProps({
  item: {
    type: Object,
    required: false,
  },
  last: {
    type: Boolean,
    required: false,
    default: true,
  },
});

const show = computed(() => props.item.value || props.item.valueList?.length > 0);
</script>

<template>
  <VListItem v-if="show" class="info-item">
    <VListItemTitle class="text-capitalize text-h6">{{ item?.title }}</VListItemTitle>
    <VListItemSubtitle class="ml-5">
      <RouterLink v-if="item?.to" :to="item?.to">{{ item?.value }}</RouterLink>
      <ul v-else-if="item?.valueList">
        <li v-for="value in item?.valueList" :key="value" class="text-disabled">{{ value }}</li>
      </ul>
      <span v-else class="text-disabled">{{ item?.value }}</span>
    </VListItemSubtitle>
  </VListItem>
  <VDivider v-if="show && !props.last" class="mb-3" />
</template>
