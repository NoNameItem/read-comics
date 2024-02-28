<script setup>
const componentProps = defineProps({
  downloadLink: {
    required: false,
    type:     String,
  },
  downloadSize: {
    required: false,
    type:     String,
  },
})

const linkVariants = computed(() => [
  {
    icon:  "fasl:folder",
    link:  componentProps.downloadLink,
    title: "Grouped by publisher and volume",
  },
  {
    icon:  "fasl:arrow-down-1-9",
    link:  `${componentProps.downloadLink}?names=ordered`,
    title: "Chronologically by cover date",
  },
])
</script>

<template>
  <VMenu v-if="componentProps.downloadLink">
    <template #activator="{ props }">
      <VBtn color="info" v-bind="props">
        <VIcon icon="fasl:download" start />
        Download (~{{ componentProps.downloadSize }})
      </VBtn>
    </template>

    <VList density="compact">
      <VListItem v-for="item in linkVariants" :key="item.link" :href="item.link">
        <template #prepend>
          <VIcon :icon="item.icon" />
        </template>
        <VListItemTitle>{{ item.title }}</VListItemTitle>
      </VListItem>
    </VList>
  </VMenu>
</template>
