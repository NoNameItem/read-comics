<script setup>
const route = useRoute()

definePageMeta({
  navActiveLink: 'publishers',
})
</script>

<template>
  <section>{{ route }}</section>
</template>
