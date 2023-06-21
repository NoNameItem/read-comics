<script setup>
defineOptions({
  name         : "AppSelect",
  inheritAttrs : false
});

const label = computed(() => useAttrs().label);
</script>

<template>
  <div class="app-select flex-grow-1" :class="$attrs.class">
    <VSelect
      v-bind="{
        ...$attrs,
        variant: 'underlined',
        menuProps: {
          contentClass: [
            'app-inner-list',
            'app-select__content',
            'v-select__content',
            $attrs.multiple !== undefined ? 'v-list-select-multiple' : '',
          ],
        },
      }"
    >
      <template v-for="(_, name) in $slots" #[name]="slotProps">
        <slot :name="name" v-bind="slotProps || {}" />
      </template>
    </VSelect>
  </div>
</template>
