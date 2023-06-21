<script setup>
import { useQuery } from "@tanstack/vue-query";
import { queries } from "@/queries";

const { isLoading: finishedIsLoading, data: finishedData } = useQuery(queries.profile.finishedStats);
const { isLoading: totalIsLoading, data: totalData } = useQuery(queries.issues.count);

const loading = computed(() => finishedIsLoading || totalIsLoading);
</script>

<template>
  <ProgressCard
    title="Reading progress"
    :total="totalData?.count"
    :current="finishedData?.finished_count"
    :delta="finishedData?.today_finished_count"
    :loading="finishedIsLoading || totalIsLoading"></ProgressCard>
</template>
