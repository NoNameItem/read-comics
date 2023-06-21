<script setup>
import { useBreadcrumbsStore } from "@/stores/breadcrumbs";
import { queries } from "@/queries";
import { useGetListData } from "@/composables/useGetListData";
import { useUserStore } from "@/stores/user";

const breadcrumb = useBreadcrumbsStore();

breadcrumb.setBreadcrumbs("Story Arcs", [{ title: "Story Arcs" }]);

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
    title: "Volumes",
    icon: "fasl:arrow-down-1-9",
    value: "volumes_count",
  },
  {
    title: "Volumes",
    icon: "fasl:arrow-down-9-1",
    value: "-volumes_count",
  },
  {
    title: "Name",
    icon: "fasl:arrow-down-a-z",
    value: "name",
  },
  {
    title: "Name",
    icon: "fasl:arrow-down-z-a",
    value: "-name",
  },
];

const { isLoading, isError, error, data, page } = useGetListData(queries.storyArcs.list, {
  "hide-finished": "yes",
  ordering: "name",
  page: 1,
});

const user = useUserStore();

const items = computed(() =>
  (data.value?.results ?? []).map((item) => ({
    ...item,
    subtitleItems: user.loggedIn
      ? [
          item.publisher?.name ?? "No publisher",
          `${item.volumes_count} volume(s)`,
          `${item.issues_count} issue(s)`,
          `${item.finished_count} finished`,
        ]
      : [item.publisher?.name ?? "No publisher", `${item.volumes_count} volume(s)`, `${item.issues_count} issue(s)`],
    to: `/story-arcs/${item.slug}`,
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
    without-issues-label="story arcs"
    show-finished-toggle
    :items="items"
    :loading="isLoading"
    :pages-number="pagesNumber" />
</template>
