<script setup lang="ts">
import comics_covers from "@images/comics_covers.jpeg"
import { useQuery } from "@tanstack/vue-query"
import { DateTime } from "luxon"
import { useDisplay } from "vuetify"

const props = defineProps({
  cardUrlBase: {
    required: true,
    type:     String,
  },
  queryName: {
    required: true,
    type:     String,
  },
  title: {
    required: true,
    type:     String,
  },
})

const { getQueryByString } = useQueryKeys()

const { name: displayBreakpoint } = useDisplay()

const slide = ref(null)

const itemsOnSlide = {
  lg:  2,
  md:  1,
  sm:  1,
  xl:  3,
  xs:  1,
  xxl: 3,
}

const { data, isError, isPending, suspense } = useQuery(getQueryByString(props.queryName))

onServerPrefetch(async () => {
  await suspense()
})

const groupedData = computed(() => {
  if (isPending.value) { return }

  const res = []
  let group = []

  if (data.value?.count === 0) {
    res.push([
      {
        image: comics_covers,
        title: "There is nothing here. Good Job",
      },
    ])

    return
  }

  data.value?.results
    ?.map(elem => ({
      image:            elem.image,
      lastFinishedDate: DateTime.fromISO(elem?.max_finished_date).toRelative(),
      linkText:         "Continue",
      linkUrl:          `/${props.cardUrlBase}/${elem?.slug}`,
      stats:            `Finished ${elem?.finished_count} of ${elem?.issues_count}`,
      title:            elem?.display_name,
    }))
    .forEach((el) => {
      group.push(el)
      if (group.length === itemsOnSlide[displayBreakpoint.value]) {
        res.push([...group])
        group = []
      }
    })

  if (data.value?.next) {
    res.push([
      {
        image:    comics_covers,
        linkText: "View all",
        linkUrl:  `/${props.cardUrlBase}/started`,
        title:    "There is more...",
      },
    ])
  }

  return res
})

const nextSlide = () => {
  if (groupedData.value?.length > 1) { slide.value = slide.value + 1 < groupedData.value.length ? slide.value + 1 : 0 }
}

const intervalId = ref(null)

const nextSlideManual = () => {
  nextSlide()
  if (intervalId.value) {
    clearInterval(intervalId.value)
    intervalId.value = null
  }
}

const prevSlide = () => {
  if (groupedData.value?.length > 1) { slide.value = slide.value - 1 > 0 ? slide.value - 1 : groupedData.value.length - 1 }
}

const prevSlideManual = () => {
  prevSlide()
  if (intervalId.value) {
    clearInterval(intervalId.value)
    intervalId.value = null
  }
}

const toggleSlide = (n) => {
  slide.value = n
  if (intervalId.value) {
    clearInterval(intervalId.value)
    intervalId.value = null
  }
}

onMounted(() => {
  intervalId.value = setInterval(nextSlide, 5000)
})

onBeforeUnmount(() => {
  if (intervalId.value) { clearInterval(intervalId.value) }
})
</script>

<template>
  <VCard :loading="isPending">
    <VCardItem>
      <VCardTitle> Unfinished {{ props.title }}</VCardTitle>
    </VCardItem>
    <VCardText>
      <VWindow
        v-if="!isPending && !isError"
        v-model="slide"
        :show-arrows="false"
        continuous
        touch
      >
        <VWindowItem
          v-for="(group, index) in groupedData"
          :key="index"
        >
          <VRow class="d-flex justify-center">
            <VCol
              v-for="item in group"
              :key="item.slug"
              col="auto"
            >
              <VImg
                :src="item.image"
                class="ma-auto"
                cover
                height="250px"
                width="250px"
              >
                <template #placeholder>
                  <div class="d-flex align-center justify-center fill-height">
                    <VProgressCircular
                      color="grey-lighten-4"
                      indeterminate
                    />
                  </div>
                </template>
                <VCard class="image-overlay d-flex flex-column justify-space-between">
                  <VCardText class="text-white pt-2">
                    {{ item.title }}
                  </VCardText>
                  <div>
                    <VCardText class="text-white text-sm pa-0 pl-4 pr-4">
                      {{ item?.lastFinishedDate }}
                    </VCardText>
                    <VCardText class="text-white pa-0 pl-4 pr-4">
                      {{ item?.stats }}
                    </VCardText>
                    <VCardActions
                      v-if="item?.linkUrl"
                      class="pt-4"
                    >
                      <VBtn
                        :to="item.linkUrl"
                        color="primary"
                        variant="flat"
                      >
                        {{ item.linkText }}
                      </VBtn>
                    </VCardActions>
                  </div>
                </VCard>
              </VImg>
            </VCol>
          </VRow>
        </VWindowItem>
      </VWindow>
    </VCardText>
    <VCardActions
      v-if="!isPending && !isError && groupedData.length > 1"
      class="justify-space-between"
    >
      <VBtn
        icon="fasl:chevron-left"
        variant="plain"
        @click="prevSlideManual"
      />
      <VItemGroup
        v-model="slide"
        class="text-center"
        mandatory
      >
        <VItem
          v-for="n in groupedData.length"
          :key="`btn-${n}`"
          v-slot="{ isSelected }"
          :value="n - 1"
        >
          <VBtn
            :color="isSelected ? 'primary' : 'secondary'"
            class="pa-0"
            density="compact"
            icon="fasl:circle-small"
            size="x-small"
            variant="plain"
            @click="toggleSlide(n - 1)"
          />
        </VItem>
      </VItemGroup>
      <VBtn
        icon="fasl:chevron-right"
        variant="plain"
        @click="nextSlideManual"
      />
    </VCardActions>
  </VCard>
</template>

<style scoped>
.image-overlay {
  background: #00000060;
  height: 100%;
}
</style>
