<script setup>
import { useQuery } from "@tanstack/vue-query"
import { queries } from "@/queries"

const { isPending: finishedisPending, data: finishedData, suspense: finishedSuspense } = useQuery(queries.profile.finishedStats)
const { isPending: totalisPending, data: totalData, suspense: totalSuspense } = useQuery(queries.issues.count)

onServerPrefetch(async () => {
  await finishedSuspense()
  await totalSuspense()
})
</script>

<template>
  <ProgressCard
    title="Reading progress"
    :total="totalData?.count"
    :current="finishedData?.finished_count"
    :delta="finishedData?.today_finished_count"
    :loading="finishedisPending || totalisPending"
  />
</template>
