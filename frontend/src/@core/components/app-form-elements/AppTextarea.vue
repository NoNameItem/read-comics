<script setup>
defineOptions({
  name         : "AppTextarea",
  inheritAttrs : false
});

const label = computed(() => useAttrs().label);
</script>

<template>
  <div class="app-textarea flex-grow-1" :class="$attrs.class">
    <VTextarea
      v-bind="{
        ...$attrs,
        variant: 'underlined',
      }"
    >
      <template v-for="(_, name) in $slots" #[name]="slotProps">
        <slot :name="name" v-bind="slotProps || {}" />
      </template>
    </VTextarea>
  </div>
</template>
