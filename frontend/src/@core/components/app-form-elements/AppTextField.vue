<script setup>
defineOptions({
  name: "AppTextField",
  inheritAttrs: false,
});


const label = computed(() => useAttrs().label);
</script>

<template>
  <div class="app-text-field flex-grow-1" :class="$attrs.class">
    <VTextField
      v-bind="{
        ...$attrs,
        variant: 'underlined',
      }"
    >
      <template v-for="(_, name) in $slots" #[name]="slotProps">
        <slot :name="name" v-bind="slotProps || {}" />
      </template>
    </VTextField>
  </div>
</template>
