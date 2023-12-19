<script setup>
import { useQuery } from "@tanstack/vue-query"
import { getQueryByString } from "@/queries"

const props = defineProps({
  title: {
    type:     String,
    required: true,
  },
  color: {
    type:     String,
    required: false,
    default:  "primary",
  },
  icon: {
    type:     String,
    required: true,
  },
  cardProps: {
    type:     Object,
    required: false,
    default(_) {
      return {}
    },
  },
  countQuery: {
    type:     String,
    required: true,
  },
})

const { isPending, data, suspense } = useQuery(getQueryByString(props.countQuery))

onServerPrefetch(async () => {
  await suspense()
})
</script>

<template>
  <CardStatisticsHorizontalLink v-bind="{ ...props, statsLoading: isPending, stats: data?.count?.toLocaleString('en-US') }" />
</template>
