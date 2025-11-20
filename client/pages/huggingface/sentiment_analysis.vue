<script setup>
import { ref } from 'vue'
import BaseTextarea from '~/components/BaseTextarea.vue'
import LoadingButton from '~/components/LoadingButton.vue'
import JsonViewer from '~/components/JsonViewer.vue'


const prompt = ref('I am super excited to learn AI')
const promptError = ref('')
const loading = ref(false)
const responseMessage = ref('')
const errorMessage = ref('')

async function handleSubmit() {
  promptError.value = ''
  responseMessage.value = '';

  let valid = true
  if (!prompt.value.trim()) {
    promptError.value = 'Prompt is required'
    valid = false
  }

  if (!valid) return

  loading.value = true

  try {
const res = await fetch('http://localhost:8000/api/huggingface_sentiment_analysis/', {
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
        <div class="w-full max-w-2xl mx-auto">
        <section class="mt-8">
          <!-- Current capabilities -->
          <div class="bg-white shadow-md rounded-lg p-6">
              <h3 class="text-lg font-bold mb-4 border-b pb-2">Sentiment Analysis</h3>
              <p class="mb-1">
                  Sentiment analysis is the automated process of classifying text based on sentiment—such as positive, 
                  negative, or neutral. It helps organisations analyse large volumes of data, uncover insights, 
                  and automate decision-making.
              </p>
              <p>
                In the past, sentiment analysis was mainly accessible to researchers, machine-learning engineers, 
                or data scientists with NLP expertise. But in recent years, the AI community has created powerful 
                tools that make machine learning far more accessible. Today, you can run sentiment analysis with just a 
                few lines of code and no prior machine-learning experience.
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
        <JsonViewer class="mt-4" :data="responseMessage" />
        <div v-if="errorMessage" class="mt-4 text-red-600">
          {{ errorMessage }}
        </div>
      </form>
    </section>
  </div>
</template>