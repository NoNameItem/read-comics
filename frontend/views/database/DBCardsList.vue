<script setup>
import OrderingSelector from "@/components/database/list/OrderingSelector.vue"
import { useUserStore } from "@/stores/user"
import { VSkeletonLoader } from "vuetify/labs/components"

const props = defineProps({
  defaultOrdering: {
    required: true,
    type:     String,
  },
  items: {
    required: true,
    type:     Array,
  },
  loading: {
    required: true,
    type:     Boolean,
  },
  orderingVariants: {
    required: true,
    type:     Array,
  },
  pagesNumber: {
    required: true,
    type:     Number,
  },
  showFinishedToggle: {
    default:  false,
    required: false,
    type:     Boolean,
  },
  showWithoutIssuesToggle: {
    default:  false,
    required: false,
    type:     Boolean,
  },
  withoutIssuesLabel: {
    required: false,
    type:     String,
  },
})

const user = useUserStore()
</script>

<template>
  <div>
    <VRow>
      <VCol cols="auto">
        <OrderingSelector
          :default-ordering="props.defaultOrdering"
          :variants="props.orderingVariants"
        />
      </VCol>
      <VCol
        v-if="props.showWithoutIssuesToggle"
        cols="auto"
      >
        <ShowWithoutIssuesToggle :label="props.withoutIssuesLabel" />
      </VCol>
      <VCol
        v-if="props.showFinishedToggle && user.loggedIn"
        cols="auto"
      >
        <ShowFinishedToggle />
      </VCol>
    </VRow>
    <VRow v-if="props.loading">
      <VCol
        v-for="n in 48"
        :key="n"
        cols="12"
        lg="3"
        md="4"
        sm="6"
        xxl="2"
      >
        <VSkeletonLoader
          loading
          type="card"
        />
      </VCol>
    </VRow>
    <VRow
      v-else
      class="match-height"
    >
      <template
        v-for="(item, index) in items"
        :key="item.slug"
      >
        <VCol
          v-if="item.groupBreak && (index === 0 || items[index - 1].groupBreak !== item.groupBreak)"
          cols="12"
        >
          <NuxtLink
            v-if="item.groupBreakTo"
            :to="item.groupBreakTo"
          >
            <h1 class="group-break-link">
              {{ item.groupBreak }}
            </h1>
          </NuxtLink>
          <h1 v-else>
            {{ item.groupBreak }}
          </h1>
        </VCol>
        <VCol
          v-if="item.groupSubBreak && (index === 0 || items[index - 1].groupSubBreak !== item.groupSubBreak)"
          cols="12"
        >
          <h2>{{ item.groupSubBreak }}</h2>
        </VCol>
        <VCol
          cols="12"
          lg="3"
          md="4"
          sm="6"
          xxl="2"
        >
          <VBadge
            :model-value="!!item?.is_finished"
            color="success"
            icon="fasl:check"
          >
            <VCard
              :class="{ finished: item?.is_finished }"
              :to="item.to"
            >
              <VImg
                :src="item.image"
                min-height="250px"
              >
                <template #placeholder>
                  <div class="d-flex align-center justify-center fill-height">
                    <VProgressCircular
                      color="grey-lighten-4"
                      indeterminate
                    />
                  </div>
                </template>
              </VImg>

              <VCardText class="position-relative">
                <VAvatar
                  v-if="item.publisher"
                  :image="item.publisher.image"
                  class="avatar-center"
                  size="75"
                />
                <div class="d-flex justify-space-between flex-wrap pt-8">
                  <div class="me-2 mb-2">
                    <VCardTitle class="pa-0 text-wrap">
                      {{ item.name }}
                    </VCardTitle>
                    <VCardSubtitle class="text-caption pa-0">
                      <ul class="list-inline">
                        <li
                          v-for="(subtitleItem, subtitleIndex) in item.subtitleItems"
                          :key="subtitleIndex"
                        >
                          {{ subtitleItem }}
                        </li>
                      </ul>
                    </VCardSubtitle>
                    <VCardText class="pl-0 pr-0">
                      {{ item.short_description }}
                    </VCardText>
                  </div>
                </div>
              </VCardText>
            </VCard>
          </VBadge>
        </VCol>
      </template>
    </VRow>
    <VRow>
      <Paginator :length="props.pagesNumber" />
    </VRow>
  </div>
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

.finished {
  opacity: 0.4;
}

.finished:hover {
  opacity: 1;
}

:deep(.v-badge),
:deep(.v-badge__wrapper),
:deep(a.v-card) {
  width: 100%;
  height: 100%;
}

.group-break-link {
  color: rgb(var(--v-theme-primary));
}
</style>
