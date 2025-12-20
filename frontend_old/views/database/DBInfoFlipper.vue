<script setup>
import { useUserStore } from "@/stores/user"

const props = defineProps({
  batchDownload: {
    default:  true,
    required: false,
    type:     Boolean,
  },
  info: {
    required: false,
    type:     Object,
  },
  infoLoading: {
    required: false,
    type:     Boolean,
  },
  showPrevNextButtons: {
    default:  false,
    required: false,
    type:     Boolean,
  },
  technicalInfo: {
    required: false,
    type:     Object,
  },
  technicalInfoLoading: {
    required: false,
    type:     Boolean,
  },
})

const infoFlipped = ref(false)

const flipInfo = () => {
  infoFlipped.value = !infoFlipped.value
}

const user = useUserStore()
</script>

<template>
  <div class="flipper-outer-wrapper w-100">
    <div class="flipper-inner-wrapper w-100">
      <FlipCard :flipped="user.isSuperuserOrStaff && infoFlipped">
        <template #front>
          <DBInfoPanel
            :batch-download="props.batchDownload"
            :data="props.info"
            :loading="props.infoLoading"
            :show-prev-next-buttons="props.showPrevNextButtons"
          />
        </template>
        <template v-if="props.technicalInfo" #back>
          <DBTechInfoPanel :data="props.technicalInfo" :loading="props.technicalInfoLoading" />
        </template>
      </FlipCard>
      <VBtn
        v-if="props.technicalInfo"
        class="flip-btn"
        elevation="20"
        icon="fasl:refresh"
        size="x-small"
        @click="flipInfo"
      />
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
