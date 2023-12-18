<script setup>
const route = useRoute()

definePageMeta({
  navActiveLink: 'story-arcs',
})
</script>

<template>
  <section>{{ route }}</section>
</template>
