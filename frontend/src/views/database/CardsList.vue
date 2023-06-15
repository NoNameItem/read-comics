<script setup>
import OrderingSelector from "@/components/database/list/OrderingSelector.vue";
import { VSkeletonLoader } from "vuetify/labs/components";

const props = defineProps({
  orderingVariants: {
    type: Array,
    required: true,
  },
  defaultOrdering: {
    type: String,
    required: true,
  },
  withoutIssuesLabel: {
    type: String,
    required: true,
  },
  items: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    required: true,
  },
  pagesNumber: {
    type: Number,
    required: true,
  },
});
</script>

<template>
  <VRow>
    <VCol cols="auto">
      <OrderingSelector :variants="props.orderingVariants" :default-ordering="props.defaultOrdering" />
    </VCol>
    <VCol cols="auto">
      <ShowWithoutIssuesToggle :label="props.withoutIssuesLabel" />
    </VCol>
  </VRow>
  <VRow v-if="props.loading">
    <VCol v-for="n in 48" :key="n" cols="12" sm="6" md="4" lg="3" xxl="2">
      <VSkeletonLoader type="card" loading></VSkeletonLoader>
    </VCol>
  </VRow>
  <VRow v-else class="match-height">
    <VCol v-for="item in items" :key="item.slug" cols="12" sm="6" md="4" lg="3" xxl="2">
      <VCard :to="item.to">
        <VImg :src="item.image" min-height="250px">
          <template #placeholder>
            <div class="d-flex align-center justify-center fill-height">
              <VProgressCircular color="grey-lighten-4" indeterminate></VProgressCircular>
            </div>
          </template>
        </VImg>

        <VCardText class="position-relative">
          <VAvatar v-if="item.publisher" size="75" class="avatar-center" :image="item.publisher.image" />

          <div class="d-flex justify-space-between flex-wrap pt-8">
            <div class="me-2 mb-2">
              <VCardTitle class="pa-0 text-wrap">{{ item.name }}</VCardTitle>
              <VCardSubtitle class="text-caption pa-0">
                <ul class="list-inline">
                  <li v-for="(subtitleItem, index) in item.subtitleItems" :key="index">{{ subtitleItem }}</li>
                </ul>
              </VCardSubtitle>
              <VCardText class="pl-0 pr-0">{{ item.short_description }}</VCardText>
            </div>
          </div>
        </VCardText>
      </VCard>
    </VCol>
  </VRow>
  <VRow>
    <Paginator :length="props.pagesNumber" />
  </VRow>
</template>

<style lang="scss" scoped>
.avatar-center {
  position: absolute;
  border: 3px solid rgb(var(--v-theme-surface));
  inset-block-start: -2rem;
  inset-inline-start: 1rem;
}

.list-inline {
  padding-left: 0;
  list-style: none;
  margin-left: -5px;

  li {
    display: inline-block;
    padding-left: 5px;
  }
}

.list-inline > li + li:before {
  content: " | ";
}
</style>
