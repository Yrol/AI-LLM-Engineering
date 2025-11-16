<script setup>
import { ref } from 'vue'
import JSON5 from "json5";
import BaseTextarea from '~/components/BaseTextarea.vue'
import LoadingButton from '~/components/LoadingButton.vue'
import TypingEffect from '~/components/TypingEffect.vue'

const prompt = ref('If there\'s one thing I want you to remember about using HuggingFace pipelines, it\'s')
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
const res = await fetch('http://localhost:8000/api/huggingface_text_generation/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        input_text: prompt.value,
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
    let raw = data.message;
    if (raw.startsWith('["') && raw.endsWith('"]')) {
        raw = raw.slice(1, -1); // remove outer quotes
    }
    const arr = JSON5.parse(raw);
    const generatedText = arr[0].generated_text;
    responseMessage.value = generatedText

  } catch (err) {
    errorMessage.value = err.message || String(err)
  } finally {
    loading.value = false
  }

}
</script>

<template>
  <div class="w-full max-w-2xl mx-auto">

    <div class="w-full max-w-2xl mx-auto">

        <section class="mt-8">
        <!-- Current capabilities -->
        <div class="bg-white shadow-md rounded-lg p-6">
            <h3 class="text-lg font-bold mb-4 border-b pb-2">Text Generation</h3>
            <p>
                Generating text is the task of generating new text given another text. These models can, for example, 
                fill in incomplete text or paraphrase.
            </p>
        </div>
        </section>
    </div>

    <section class="mt-8">
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
        <TypingEffect :message="responseMessage" color-class="text-blue-600" :speed="5" />
        <div v-if="errorMessage" class="mt-4 text-red-600">
          {{ errorMessage }}
        </div>
      </form>
    </section>
  </div>
</template>