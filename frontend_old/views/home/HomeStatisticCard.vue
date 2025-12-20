<script setup>
import { useQuery } from "@tanstack/vue-query"

const props = defineProps({
  cardProps: {
    default(_) {
      return {}
    },
    required: false,
    type:     Object,
  },
  color: {
    default:  "primary",
    required: false,
    type:     String,
  },
  countQuery: {
    required: true,
    type:     String,
  },
  icon: {
    required: true,
    type:     String,
  },
  title: {
    required: true,
    type:     String,
  },
})

const { getQueryByString } = useQueryKeys()

const { data, isPending, suspense } = useQuery(getQueryByString(props.countQuery))

onServerPrefetch(async () => {
  await suspense()
})
</script>

<template>
  <CardStatisticsHorizontalLink v-bind="{ ...props, statsLoading: isPending, stats: data?.count?.toLocaleString('en-US') }" />
</template>
