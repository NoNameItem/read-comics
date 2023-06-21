<script setup>
import { useQuery } from "@tanstack/vue-query";
import { getQueryByString } from "@/queries";
import { useDisplay } from "vuetify";
import { DateTime } from "luxon";
import comics_covers from "@images/comics_covers.jpeg";

const props = defineProps({
  queryName: {
    type: String,
    required: true,
  },
  cardUrlBase: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
});

const { name: displayBreakpoint } = useDisplay();

const slide = ref(null);

const itemsOnSlide = {
  xs: 1,
  sm: 1,
  md: 1,
  lg: 2,
  xl: 3,
  xxl: 4,
};

const { isLoading, isError, data } = useQuery(getQueryByString(props.queryName));

const groupedData = computed(() => {
  if (isLoading.value) {
    return;
  }

  const res = [];
  let group = [];

  if (data.value?.count === 0) {
    res.push([
      {
        title: "There is nothing here. Good Job",
        image: comics_covers,
      },
    ]);
    return;
  }

  data.value?.results
    ?.map((elem) => ({
      title: elem?.display_name,
      lastFinishedDate: DateTime.fromISO(elem?.max_finished_date).toRelative(),
      stats: `Finished ${elem?.finished_count} of ${elem?.issues_count}`,
      image: elem.image,
      linkText: "Continue",
      linkUrl: `/${props.cardUrlBase}/${elem?.slug}`,
    }))
    .forEach((el) => {
      group.push(el);
      if (group.length === itemsOnSlide[displayBreakpoint.value]) {
        res.push([...group]);
        group = [];
      }
    });

  if (data.value?.next) {
    res.push([
      {
        title: "There is more...",
        image: comics_covers,
        linkText: "View all",
        linkUrl: `/${props.cardUrlBase}/started`,
      },
    ]);
  }

  return res;
});

const nextSlide = () => {
  if (groupedData.value?.length > 1) {
    slide.value = slide.value + 1 < groupedData.value.length ? slide.value + 1 : 0;
  }
};

const nextSlideManual = () => {
  nextSlide();
  if (intervalId.value) {
    clearInterval(intervalId.value);
    intervalId.value = null;
  }
};

const prevSlide = () => {
  if (groupedData.value?.length > 1) {
    slide.value = slide.value - 1 > 0 ? slide.value - 1 : groupedData.value.length - 1;
  }
};

const prevSlideManual = () => {
  prevSlide();
  if (intervalId.value) {
    clearInterval(intervalId.value);
    intervalId.value = null;
  }
};

const toggleSlide = (n) => {
  slide.value = n;
  if (intervalId.value) {
    clearInterval(intervalId.value);
    intervalId.value = null;
  }
};

const intervalId = ref(null);

onMounted(() => {
  intervalId.value = setInterval(nextSlide, 5000);
});

onBeforeUnmount(() => {
  if (intervalId.value) {
    clearInterval(intervalId.value);
  }
});
</script>

<template>
  <VCard :loading="isLoading">
    <VCardItem>
      <VCardTitle> Unfinished {{ props.title }}</VCardTitle>
    </VCardItem>
    <VCardText>
      <VWindow v-if="!isLoading && !isError" v-model="slide" :show-arrows="false" continuous touch>
        <VWindowItem v-for="(group, index) in groupedData" :key="index">
          <VRow class="d-flex justify-center">
            <VCol v-for="item in group" :key="item.slug">
              <VImg height="250px" width="250px" cover :src="item.image" class="ma-auto">
                <template #placeholder>
                  <div class="d-flex align-center justify-center fill-height">
                    <VProgressCircular color="grey-lighten-4" indeterminate></VProgressCircular>
                  </div>
                </template>
                <VCard class="image-overlay d-flex flex-column justify-space-between">
                  <VCardText class="text-white pt-2">{{ item.title }}</VCardText>
                  <div>
                    <VCardText class="text-white text-sm pa-0 pl-4 pr-4">{{ item?.lastFinishedDate }}</VCardText>
                    <VCardText class="text-white pa-0 pl-4 pr-4">{{ item?.stats }}</VCardText>
                    <VCardActions v-if="item?.linkUrl" class="pt-4">
                      <VBtn variant="outlined" color="info" :to="item.linkUrl"> {{ item.linkText }}</VBtn>
                    </VCardActions>
                  </div>
                </VCard>
              </VImg>
            </VCol>
          </VRow>
        </VWindowItem>
      </VWindow>
    </VCardText>
    <VCardActions v-if="!isLoading && !isError && groupedData.length > 1" class="justify-space-between">
      <VBtn variant="plain" icon="fasl:chevron-left" @click="prevSlideManual" />
      <VItemGroup v-model="slide" class="text-center" mandatory>
        <VItem v-for="n in groupedData.length" :key="`btn-${n}`" v-slot="{ isSelected }" :value="n - 1">
          <VBtn
            variant="plain"
            :color="isSelected ? 'primary' : 'secondary'"
            icon="mdi-record"
            size="x-small"
            class="pa-0"
            density="compact"
            @click="toggleSlide(n - 1)"></VBtn>
        </VItem>
      </VItemGroup>
      <VBtn variant="plain" icon="fasl:chevron-right" @click="nextSlideManual" />
    </VCardActions>
  </VCard>
</template>

<style scoped>
.image-overlay {
  background: #00000060;
  height: 100%;
}
</style>
