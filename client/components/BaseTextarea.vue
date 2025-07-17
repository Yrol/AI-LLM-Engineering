<template>
  <div>
    <label v-if="label" :for="id" class="block mb-1 font-medium text-gray-700">
      {{ label }}
    </label>
    <textarea :id="id" :rows="rows" :placeholder="placeholder" :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 transition"></textarea>
    <p v-if="help" class="mt-1 text-sm text-gray-500">{{ help }}</p>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  id: {
    type: String,
    default: () => `textarea-${Math.random().toString(36).substr(2, 9)}`
  },
  placeholder: {
    type: String,
    default: ''
  },
  rows: {
    type: Number,
    default: 4
  },
  help: {
    type: String,
    default: ''
  }
})
defineEmits(['update:modelValue'])
</script>
