<template>
  <div>
    <h4 class="text-white">{{ $props.title }}</h4>
    <span class="text-white">{{ $props.message }}</span>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  message: String,
});
</script>
