<template>
  <button type="button" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
    @click="$emit('click')">
    <slot>Submit</slot>
  </button>
</template>

<script setup>
defineEmits(['click']);
</script>
