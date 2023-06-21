<script setup>
import { useBreadcrumbsStore } from "@/stores/breadcrumbs";
import { queries } from "@/queries";
import { useGetListData } from "@/composables/useGetListData";
import { useUserStore } from "@/stores/user";

const user = useUserStore();

const breadcrumb = useBreadcrumbsStore();

breadcrumb.setBreadcrumbs("Volumes", [{ title: "Volumes" }]);

const orderingVariants = [
  {
    title: "Issues",
    icon: "fasl:arrow-down-1-9",
    value: "issues_count",
  },
  {
    title: "Issues",
    icon: "fasl:arrow-down-9-1",
    value: "-issues_count",
  },
  {
    title: "Name",
    icon: "fasl:arrow-down-a-z",
    value: "name,start_year",
  },
  {
    title: "Name",
    icon: "fasl:arrow-down-z-a",
    value: "-name,-start_year",
  },
  {
    title: "Start year",
    icon: "fasl:arrow-down-1-9",
    value: "start_year",
  },
  {
    title: "Start year",
    icon: "fasl:arrow-down-9-1",
    value: "-start_year",
  },
];

const { isLoading, isError, error, data, page } = useGetListData(queries.volumes.list, {
  "hide-finished": "yes",
  ordering: "start_year",
  page: 1,
});

const route = useRoute();

const ordering = computed(() => route.query?.ordering ?? "start_year");

const getGroupBreak = (item) => {
  if (ordering.value.includes("start_year")) {
    return `${item.start_year}` ?? "Unknown year";
  }
  return null;
};

const items = computed(() =>
  (data.value?.results ?? []).map((item) => ({
    ...item,
    groupBreak: getGroupBreak(item),
    subtitleItems: user.loggedIn
      ? [item.publisher?.name ?? "No publisher", `${item.issues_count} issue(s)`, `${item.finished_count} finished`]
      : [item.publisher?.name ?? "No publisher", `${item.issues_count} issue(s)`],
    to: `/volumes/${item.slug}`,
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
    without-issues-label="volumes"
    show-finished-toggle
    :items="items"
    :loading="isLoading"
    :pages-number="pagesNumber" />
</template>
