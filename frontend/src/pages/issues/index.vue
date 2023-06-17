<script setup>
import { useBreadcrumbsStore } from "@/stores/breadcrumbs";
import { queries } from "@/queries";
import { useGetListData } from "@/composables/useGetListData";
import { formatDate } from "@/utils/format_utils";
import { DateTime } from "luxon";

const breadcrumb = useBreadcrumbsStore();

breadcrumb.setBreadcrumbs("Issues", [{ title: "Issues" }]);

const orderingVariants = [
  {
    title: "Name",
    icon: "fasl:arrow-down-a-z",
    value: "volume__name,volume__start_year,numerical_number,number",
  },
  {
    title: "Name",
    icon: "fasl:arrow-down-z-a",
    value: "-volume__name,-volume__start_year,-numerical_number,-number",
  },
  {
    title: "Cover date",
    icon: "fasl:arrow-down-1-9",
    value: "cover_date,volume__name,volume__start_year,numerical_number,number",
  },
  {
    title: "Cover date",
    icon: "fasl:arrow-down-9-1",
    value: "-cover_date,-volume__name,-volume__start_year,-numerical_number,-number",
  },
];

const defaultOrdering = "cover_date,volume__name,volume__start_year,numerical_number,number";

const { isLoading, isError, error, data, page } = useGetListData(queries.issues.list, {
  "hide-finished": "yes",
  ordering: defaultOrdering,
  page: 1,
});

const route = useRoute();

const ordering = computed(() => route.query?.ordering ?? defaultOrdering);

const getBreaks = (item) => {
  if (ordering.value.includes("cover_date")) {
    return {
      groupBreak: item.cover_date ? DateTime.fromISO(item.cover_date).toFormat("yyyy") : "Unknown year",
      groupSubBreak: item.cover_date ? DateTime.fromISO(item.cover_date).toFormat("LLLL yyyy") : "Unknown month",
    };
  }
  return {
    groupBreak: item.volume.display_name,
    groupBreakTo: `/volumes/${item.volume.slug}`,
  };
};

const items = computed(() =>
  (data.value?.results ?? []).map((item) => ({
    ...item,
    ...getBreaks(item),
    subtitleItems: [item.publisher?.name ?? "No publisher", formatDate(item.cover_date) || "Cover date unknown"],
    to: route.query?.ordering ? `/issues/${item.slug}?ordering=${route.query?.ordering}` : `/issues/${item.slug}`,
    isFinished: item.finished_flg === 1,
  }))
);

const pagesNumber = ref(0);

watch(data, () => {
  if (data.value?.pages_count > 0) {
    pagesNumber.value = data.value.pages_count;
  }
});
</script>

<template>
  <DBCardsList
    :ordering-variants="orderingVariants"
    default-ordering="name"
    without-issues-label="characters"
    show-finished-toggle
    :items="items"
    :loading="isLoading"
    :pages-number="pagesNumber" />
</template>
