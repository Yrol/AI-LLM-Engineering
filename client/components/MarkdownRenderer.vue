<template>
  <MDC :value="content" tag="div" />
</template>

<script setup>
defineProps({
  content: {
    type: String,
    required: true
  }
})
</script>
