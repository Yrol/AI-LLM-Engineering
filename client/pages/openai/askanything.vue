<script setup>
import { ref } from 'vue'
import BaseTextarea from '~/components/BaseTextarea.vue'
import LoadingButton from '~/components/LoadingButton.vue'
import TypingEffect from '~/components/TypingEffect.vue'


const askAnythingPrompt = ref('')
const askAnythingPromptError = ref('')
const askAnythingLoading = ref(false)
const askAnythingResponseMessage = ref('')
const askAnythingErrorMessage = ref('')

async function handleSubmitAskAnything() {
  askAnythingPromptError.value = ''

  let valid = true
  if (!askAnythingPrompt.value.trim()) {
    askAnythingPromptError.value = 'Prompt is required'
    valid = false
  }

  if (!valid) return

  askAnythingLoading.value = true

  try {
    const res = await fetch('http://localhost:8000/api/askanything/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: askAnythingPrompt.value,
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
    askAnythingResponseMessage.value = data.response
    // askAnythingPrompt.value = ''
  } catch (err) {
    askAnythingErrorMessage.value = err.message || String(err)
  } finally {
    askAnythingLoading.value = false
  }

}
</script>

<template>
  <div class="w-full max-w-2xl mx-auto">

    <section class="mt-8">
      <h3 class="text-lg font-bold mb-4 border-b pb-2">OpenAI Ask Anything</h3>
      <form @submit.prevent="handleSubmitAskAnything" class="w-full max-w-2xl mx-auto p-6 bg-white rounded shadow">

        <BaseTextarea id="ask-anything-textarea" label="Ask anything" v-model="askAnythingPrompt"
          placeholder="Type your prompt here..." :rows="6" help="Max 500 characters" class="mb-1" />
        <div v-if="askAnythingPromptError" class="text-red-600 text-sm mb-3">{{ askAnythingPromptError }}</div>

        <LoadingButton type="submit" :loading="askAnythingLoading">
          <template #loading>
            Sending...
          </template>
          Send
        </LoadingButton>
        <TypingEffect :message="askAnythingResponseMessage" color-class="text-blue-600" :speed="5" />
        <div v-if="askAnythingErrorMessage" class="mt-4 text-red-600">
          {{ askAnythingErrorMessage }}
        </div>
      </form>
    </section>
  </div>
</template>