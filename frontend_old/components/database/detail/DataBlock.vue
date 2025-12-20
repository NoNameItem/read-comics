<script setup>
const props = defineProps({
  item: {
    required: false,
    type:     Object,
  },
  last: {
    default:  true,
    required: false,
    type:     Boolean,
  },
})

const show = computed(() => props.item.value || props.item.html || props.item.valueList?.length > 0)
</script>

<template>
  <VListItem
    v-if="show"
    class="info-item"
  >
    <VListItemTitle class="text-capitalize text-h6">
      {{ item?.title }}
    </VListItemTitle>
    <VListItemSubtitle class="ml-5">
      <NuxtLink
        v-if="item?.to"
        :to="item?.to"
      >
        {{ item?.value }}
      </NuxtLink>
      <ul v-else-if="item?.valueList">
        <li
          v-for="value in item?.valueList"
          :key="value"
          class="text-disabled"
        >
          {{ value }}
        </li>
      </ul>
      <span
        v-else-if="item?.html"
        class="text-disabled"
        v-html="item?.html"
      />
      <span
        v-else
        class="text-disabled"
      >{{ item?.value }}</span>
    </VListItemSubtitle>
  </VListItem>
  <VDivider
    v-if="show && !props.last"
    class="mb-3"
  />
</template>
