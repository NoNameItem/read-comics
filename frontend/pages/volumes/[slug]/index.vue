<script setup>
definePageMeta({
  navActiveLink: "volumes",
})

const route = useRoute()
</script>

<template>
  <section>{{ route }}</section>
</template>
