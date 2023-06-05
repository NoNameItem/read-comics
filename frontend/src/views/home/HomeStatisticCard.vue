<script setup>
import { useQuery } from "@tanstack/vue-query";
import { getQueryByString } from "@/queries";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  color: {
    type: String,
    required: false,
    default: "primary",
  },
  icon: {
    type: String,
    required: true,
  },
  cardProps: {
    type: Object,
    required: false,
    default(_) {
      return {};
    },
  },
  countQuery: {
    type: String,
    required: true,
  },
});

const { isLoading, data } = useQuery(getQueryByString(props.countQuery));
</script>

<template>
  <CardStatisticsHorizontalLink v-bind="{ ...props, statsLoading: isLoading, stats: data?.count?.toLocaleString() }" />
</template>
