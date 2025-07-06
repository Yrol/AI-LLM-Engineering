<template>
  <form @submit.prevent="handleSubmit" class="max-w-md mx-auto mt-8 p-6 bg-white rounded shadow">
    <BaseInput
      id="my-input"
      label="Enter Text"
      v-model="inputValue"
      placeholder="Type something..."
    />
    <BaseButton @click="handleSubmit">Submit</BaseButton>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import BaseInput from './BaseInput.vue'
import BaseButton from './BaseButton.vue'

const inputValue = ref('')

function handleSubmit() {
  alert('Submitted: ' + inputValue.value)
}
</script>
