<script setup>
import { ref } from 'vue'
import BaseTextarea from '~/components/BaseTextarea.vue'
import BaseInput from '~/components/BaseInput.vue'
import LoadingButton from '~/components/LoadingButton.vue'
import TypingEffect from '~/components/TypingEffect.vue'

const webSummerizerSystemPrompt = ref('You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown.')
const webSummerizerUserPrompt = ref('You are looking at a website titled {website.title} \nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n')
const webSummerizerUrl = ref('https://www.bbc.com/')
const webSummerizerResponseMessage = ref('')
const webSummerizerErrorMessage = ref('')
const systemPromptError = ref('')
const userPromptError = ref('')
const webSummerizerUrlError = ref('')
const webSummerizerLoading = ref(false)

async function handleSubmitWebSummerizer() {
  // Reset errors
  systemPromptError.value = ''
  userPromptError.value = ''
  webSummerizerUrlError.value = ''

  webSummerizerResponseMessage.value = ''
  webSummerizerErrorMessage.value = ''

  // Validation
  let valid = true
  if (!webSummerizerSystemPrompt.value.trim()) {
    systemPromptError.value = 'System Prompt is required.'
    valid = false
  }

  if (!webSummerizerUserPrompt.value.trim()) {
    userPromptError.value = 'User Prompt is required.'
    valid = false
  }

  if (!webSummerizerUrl.value.trim()) {
    webSummerizerUrlError.value = 'URL is required.'
    valid = false
  }

  if (!valid) return

  webSummerizerLoading.value = true

  try {
    const res = await fetch('http://localhost:8000/api/ollama_websummarizer/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        systemInput: webSummerizerSystemPrompt.value,
        website: webSummerizerUrl.value
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
    webSummerizerResponseMessage.value = data.message

    // webSummerizerSystemPrompt.value = ''
    // webSummerizerUrl.value = ''

  } catch (err) {
    webSummerizerErrorMessage.value = err.message || String(err)
  } finally {
    webSummerizerLoading.value = false
  }
}
</script>

<template>
  <div class="w-full max-w-2xl mx-auto">

    <section class="mt-8">
      <h3 class="text-lg font-bold mb-4 border-b pb-2">Ollama Web Summarizer</h3>

      <p class="p-4">A web summariser tool that uses a predefined System Prompt (set in the backend) along with a User
        Prompt. You may modify the User Prompt and experiment with different variations.
      </p>

      <p class="p-4">
        Note: Getting a response for this task from the locally running Ollama may take a few minutes, depending on your machine’s speed
      </p>

      <form @submit.prevent="handleSubmitWebSummerizer" class="w-full max-w-2xl mx-auto p-6 bg-white rounded shadow">

        <BaseInput id="summarizer-title" label="URL" v-model="webSummerizerUrl" placeholder="Enter the URL"
          class="mb-3" />
        <div v-if="webSummerizerUrlError" class="text-red-600 text-sm mb-3">{{ webSummerizerUrlError }}</div>

        <BaseTextarea id="system-prompt-textarea" label="System Prompt" v-model="webSummerizerSystemPrompt"
          placeholder="Type your System Prompt here..." :rows="6" help="Max 500 characters" class="mb-1" />
        <div v-if="systemPromptError" class="text-red-600 text-sm mb-3">{{ systemPromptError }}</div>

        <BaseTextarea id="user-prompt-textarea" :disabled="true" label="User Prompt"
          v-model="webSummerizerUserPrompt" placeholder="Type your User Prompt here..." :rows="6"
          help="Max 500 characters" class="mb-1" />
        <div v-if="userPromptError" class="text-red-600 text-sm mb-3">{{ userPromptError }}</div>

        <LoadingButton type="submit" :loading="webSummerizerLoading">
          <template #loading>
            Sending...
          </template>
          Send
        </LoadingButton>
        <TypingEffect :message="webSummerizerResponseMessage" color-class="text-blue-600" :speed="5" />
        <div v-if="webSummerizerErrorMessage" class="mt-4 text-red-600">
          {{ webSummerizerErrorMessage }}
        </div>
      </form>
    </section>
  </div>
</template>