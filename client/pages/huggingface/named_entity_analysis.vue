<script setup>
import { ref } from 'vue'
import BaseTextarea from '~/components/BaseTextarea.vue'
import LoadingButton from '~/components/LoadingButton.vue'
import JsonViewer from '~/components/JsonViewer.vue'


const prompt = ref('Barack Obama was the 44th president of the United States.')
const promptError = ref('')
const loading = ref(false)
const responseMessage = ref('')
const errorMessage = ref('')

async function handleSubmit() {
  promptError.value = ''
  responseMessage.value = ''

  let valid = true
  if (!prompt.value.trim()) {
    promptError.value = 'Prompt is required'
    valid = false
  }

  if (!valid) return

  loading.value = true

  try {
    const res = await fetch('http://localhost:8000/api/huggingface_named_entity_analysis/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: prompt.value,
      })
    })

    if (!res.ok) {
      let apiErrorMsg = 'API error'
      try {
        const errorData = await res.json()
        apiErrorMsg = errorData.error || errorData.message || apiErrorMsg
      } catch (e) {
        // Not JSON or no error message; stick with generic
      }
      throw new Error(apiErrorMsg)
    }
    const data = await res.json()
    responseMessage.value = data.message
    // prompt.value = ''
  } catch (err) {
    errorMessage.value = err.message || String(err)
  } finally {
    loading.value = false
  }

}
</script>

<template>
  <div class="w-full max-w-2xl mx-auto">

    <section class="mt-8">
      <h3 class="text-lg font-bold mb-4 border-b pb-2">Named Entity Analysis</h3>
      <form @submit.prevent="handleSubmit" class="w-full max-w-2xl mx-auto p-6 bg-white rounded shadow">

        <BaseTextarea id="prompt-textarea" label="Prompt" v-model="prompt"
          placeholder="Type your prompt here..." :rows="6" help="Max 500 characters" class="mb-1" />
        <div v-if="promptError" class="text-red-600 text-sm mb-3">{{ promptError }}</div>

        <LoadingButton type="submit" :loading="loading">
          <template #loading>
            Sending...
          </template>
          Send
        </LoadingButton>
        <JsonViewer class="mt-4" :data="responseMessage" />
        <div v-if="errorMessage" class="mt-4 text-red-600">
          {{ errorMessage }}
        </div>
      </form>
    </section>
  </div>
</template>