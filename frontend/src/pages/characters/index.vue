<script setup>
import { useBreadcrumbsStore } from "@/stores/breadcrumbs";
import CardsList from "@/views/database/CardsList.vue";
import { queries } from "@/queries";
import { useGetListData } from "@/composables/useGetListData";

const breadcrumb = useBreadcrumbsStore();

breadcrumb.setBreadcrumbs("Characters", [{ title: "Characters" }]);

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

const { isLoading, isError, error, data, page } = useGetListData(queries.characters.list);

const items = computed(() =>
  (data.value?.results ?? []).map((item) => ({
    ...item,
    subtitleItems: [
      item.publisher?.name ?? "No publisher",
      `${item.volumes_count} volume(s)`,
      `${item.issues_count} issue(s)`,
    ],
    to: `/characters/${item.slug}`,
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
  <CardsList
    :ordering-variants="orderingVariants"
    default-ordering="name"
    without-issues-label="characters"
    :items="items"
    :loading="isLoading"
    :pages-number="pagesNumber" />
</template>
