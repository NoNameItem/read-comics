<script setup>
import { useUserStore } from "@/stores/user";

const cardPropsUnauthorized = [
  {
    title: "Issues",
    icon: "fasl:book-open",
    color: "info",
    "count-query": "issues.count",
    "card-props": {
      to: "/issues",
    },
  },
  {
    title: "Publishers",
    icon: "fasl:building",
    color: "warning",
    "count-query": "publishers.count",
    "card-props": {
      to: "/publishers",
    },
  },
  {
    title: "Story Arcs",
    icon: "fasl:books",
    color: "error",
    "count-query": "storyArcs.count",
    "card-props": {
      to: "/story-arcs",
    },
  },
  {
    title: "Volumes",
    icon: "fasl:book-sparkles",
    color: "primary",
    "count-query": "volumes.count",
    "card-props": {
      to: "/volumes",
    },
  },
  {
    title: "Characters",
    icon: "fasl:bat",
    color: "info",
    "count-query": "characters.count",
    "card-props": {
      to: "/characters",
    },
  },
  {
    title: "Teams",
    icon: "fasl:users",
    color: "warning",
    "count-query": "teams.count",
    "card-props": {
      to: "/teams",
    },
  },
  {
    title: "Locations",
    icon: "fasl:location-dot",
    color: "error",
    "count-query": "locations.count",
    "card-props": {
      to: "/locations",
    },
  },
  {
    title: "Objects",
    icon: "fasl:swords-laser",
    color: "primary",
    "count-query": "objects.count",
    "card-props": {
      to: "/objects",
    },
  },
  {
    title: "Concepts",
    icon: "fasl:brain",
    color: "info",
    "count-query": "concepts.count",
    "card-props": {
      to: "/concepts",
    },
  },
  {
    title: "People",
    icon: "fasl:people-carry-box",
    color: "warning",
    "count-query": "people.count",
    "card-props": {
      to: "/people",
    },
  },
];

const missingIssueCard = {
  title: "Missing issues",
  icon: "fasl:eye",
  color: "error",
  "count-query": "missingIssues.count",
  "card-props": {
    to: "/missing-issues",
  },
};

const user = useUserStore();

const cardProps = computed(() =>
  user.loggedIn ? [...cardPropsUnauthorized, missingIssueCard] : cardPropsUnauthorized
);
</script>

<template>
  <VRow justify="center">
    <VCol v-for="cardProp in cardProps" :key="cardProp.title" cols="12" sm="6" md="3" xl="2">
      <HomeStatisticCard v-bind="cardProp" />
    </VCol>
  </VRow>
</template>
