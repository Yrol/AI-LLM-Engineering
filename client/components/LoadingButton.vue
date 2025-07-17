<template>
  <button :type="type" :disabled="loading || disabled" :class="[
    'mt-4 px-4 py-2 rounded bg-blue-600 text-white font-semibold flex items-center justify-center transition',
    loading ? 'opacity-70 cursor-not-allowed' : 'hover:bg-blue-700',
    customClass
  ]">
    <span v-if="loading" class="flex items-center">
      <svg class="animate-spin h-5 w-5 mr-2 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
        viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
      </svg>
      <slot name="loading">Submitting...</slot>
    </span>
    <span v-else>
      <slot>Submit</slot>
    </span>
  </button>
</template>

<script setup>
defineProps({
  loading: { type: Boolean, default: false },
  type: { type: String, default: 'button' },
  disabled: { type: Boolean, default: false },
  customClass: { type: String, default: '' }
})
</script>
