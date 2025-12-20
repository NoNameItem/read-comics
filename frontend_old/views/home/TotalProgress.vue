<script setup>
import { useQuery } from "@tanstack/vue-query"

const { queries } = useQueryKeys()

const { data: finishedData, isPending: finishedIsPending, suspense: finishedSuspense } = useQuery(queries.profile.finishedStats)
const { data: totalData, isPending: totalIsPending, suspense: totalSuspense } = useQuery(queries.issues.count)

onServerPrefetch(async () => {
  await finishedSuspense()
  await totalSuspense()
})
</script>

<template>
  <ProgressCard
    :current="finishedData?.finished_count"
    :delta="finishedData?.today_finished_count"
    :loading="finishedIsPending || totalIsPending"
    :total="totalData?.count"
    title="Reading progress"
  />
</template>
