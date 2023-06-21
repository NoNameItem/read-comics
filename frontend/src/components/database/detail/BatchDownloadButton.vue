<script setup>
const componentProps = defineProps({
  downloadLink: {
    type: String,
    required: false,
  },
  downloadSize: {
    type: String,
    required: false,
  },
});

const linkVariants = computed(() => [
  {
    icon: "fasl:folder",
    title: "Grouped by publisher and volume",
    link: componentProps.downloadLink,
  },
  {
    icon: "fasl:arrow-down-1-9",
    title: "Chronologically by cover date",
    link: `${componentProps.downloadLink}?names=ordered`,
  },
]);
</script>

<template>
  <VMenu v-if="componentProps.downloadLink">
    <template #activator="{ props }">
      <VBtn color="info" v-bind="props">
        <VIcon start icon="fasl:download" />
        Download (~{{ componentProps.downloadSize }})
      </VBtn>
    </template>

    <VList density="compact">
      <VListItem v-for="item in linkVariants" :key="item.link" :href="item.link">
        <template #prepend>
          <VIcon :icon="item.icon"></VIcon>
        </template>
        <VListItemTitle>{{ item.title }}</VListItemTitle>
      </VListItem>
    </VList>
  </VMenu>
</template>
