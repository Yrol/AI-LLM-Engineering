<template>
  <div class="mb-4">
    <label :for="id" class="block mb-1 font-medium text-gray-700">{{ label }}</label>
    <input :id="id" :type="type" :placeholder="placeholder" :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
  </div>
</template>

<script setup>
defineProps({
  id: String,
  label: String,
  type: { type: String, default: 'text' },
  placeholder: String,
  modelValue: String
});
defineEmits(['update:modelValue']);
</script>