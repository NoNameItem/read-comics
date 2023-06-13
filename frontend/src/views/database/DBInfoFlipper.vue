<script setup>
import { useUserStore } from "@/stores/user";

const props = defineProps({
  info: {
    type: Object,
    required: false,
  },
  infoLoading: {
    type: Boolean,
    required: false,
  },
  technicalInfo: {
    type: Object,
    required: false,
  },
  technicalInfoLoading: {
    type: Boolean,
    required: false,
  },
});

const infoFlipped = ref(false);

const flipInfo = () => {
  infoFlipped.value = !infoFlipped.value;
};

const user = useUserStore();
</script>

<template>
  <div class="flipper-outer-wrapper w-100">
    <div class="flipper-inner-wrapper w-100">
      <FlipCard :flipped="user.isSuperuserOrStaff && infoFlipped">
        <template #front>
          <DBInfoPanel :data="props.info" :loading="props.infoLoading" />
        </template>
        <template v-if="props.technicalInfo" #back>
          <DBTechInfoPanel :data="props.technicalInfo" :loading="props.technicalInfoLoading" />
        </template>
      </FlipCard>
      <VBtn
        v-if="props.technicalInfo"
        ref="resetImageButtonRef"
        elevation="20"
        size="x-small"
        class="flip-btn"
        icon="fasl:refresh"
        @click="flipInfo">
      </VBtn>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.flipper-outer-wrapper {
  display: inline-block;
  line-height: 1;
}

.flipper-inner-wrapper {
  display: flex;
  position: relative;
}

.flip-btn {
  display: inline-flex;
  pointer-events: auto;
  position: absolute;
  border-radius: 0.375rem;
  inset-block-start: 0;
  inset-inline-end: 0;
  transform: translate(0.5rem, -0.5rem);
  background-color: rgb(var(--v-theme-surface)) !important;
  color: rgba(var(--v-theme-on-surface), var(--v-disabled-opacity)) !important;
}
</style>
