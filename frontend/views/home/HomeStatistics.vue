<script setup>
import { useUserStore } from "@/stores/user"

const cardPropsUnauthorized = [
  {
    "card-props":  { to: "/issues" },
    "color":       "info",
    "count-query": "issues.count",
    "icon":        "fasl:book-open",
    "title":       "Issues",
  },
  {
    "card-props":  { to: "/publishers" },
    "color":       "warning",
    "count-query": "publishers.count",
    "icon":        "fasl:building",
    "title":       "Publishers",
  },
  {
    "card-props":  { to: "/story-arcs" },
    "color":       "error",
    "count-query": "storyArcs.count",
    "icon":        "fasl:books",
    "title":       "Story Arcs",
  },
  {
    "card-props":  { to: "/volumes" },
    "color":       "primary",
    "count-query": "volumes.count",
    "icon":        "fasl:book-sparkles",
    "title":       "Volumes",
  },
  {
    "card-props":  { to: "/characters" },
    "color":       "info",
    "count-query": "characters.count",
    "icon":        "fasl:bat",
    "title":       "Characters",
  },
  {
    "card-props":  { to: "/teams" },
    "color":       "warning",
    "count-query": "teams.count",
    "icon":        "fasl:users",
    "title":       "Teams",
  },
  {
    "card-props":  { to: "/locations" },
    "color":       "error",
    "count-query": "locations.count",
    "icon":        "fasl:location-dot",
    "title":       "Locations",
  },
  {
    "card-props":  { to: "/objects" },
    "color":       "primary",
    "count-query": "objects.count",
    "icon":        "fasl:swords-laser",
    "title":       "Objects",
  },
  {
    "card-props":  { to: "/concepts" },
    "color":       "info",
    "count-query": "concepts.count",
    "icon":        "fasl:brain",
    "title":       "Concepts",
  },
  {
    "card-props":  { to: "/people" },
    "color":       "warning",
    "count-query": "people.count",
    "icon":        "fasl:people-carry-box",
    "title":       "People",
  },
]

const missingIssueCard = {
  "card-props":  { to: "/missing-issues" },
  "color":       "error",
  "count-query": "missingIssues.count",
  "icon":        "fasl:eye",
  "title":       "Missing issues",
}

const user = useUserStore()

const cardProps = computed(() =>
  user.loggedIn ? [...cardPropsUnauthorized, missingIssueCard] : cardPropsUnauthorized,
)
</script>

<template>
  <VRow justify="center">
    <VCol v-for="cardProp in cardProps" :key="cardProp.title" cols="12" md="3" sm="6" xl="2">
      <HomeStatisticCard v-bind="cardProp" />
    </VCol>
  </VRow>
</template>
