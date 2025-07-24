<script setup>
import { ref } from 'vue'
import BaseTextarea from '~/components/BaseTextarea.vue'
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
    const res = await fetch('http://localhost:8000/api/websummarizer/', {
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
    <h2 class="text-xl font-semibold mb-4">OpenAI Experiment</h2>

    <section>
      <h3 class="text-lg font-bold mb-4 border-b pb-2">Ask Anything</h3>
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

    <section class="mt-8">
      <h3 class="text-lg font-bold mb-4 border-b pb-2">Web Summarizer</h3>

      <p class="p-4">A web summariser tool that uses a predefined System Prompt (set in the backend) along with a User
        Prompt. You may modify the User Prompt and experiment with different variations.</p>

      <form @submit.prevent="handleSubmitWebSummerizer" class="w-full max-w-2xl mx-auto p-6 bg-white rounded shadow">

        <BaseInput id="summarizer-title" label="URL" v-model="webSummerizerUrl" placeholder="Enter the URL"
          class="mb-3" />
        <div v-if="webSummerizerUrlError" class="text-red-600 text-sm mb-3">{{ webSummerizerUrlError }}</div>

        <BaseTextarea id="system-prompt-textarea" label="System Prompt" v-model="webSummerizerSystemPrompt"
          placeholder="Type your System Prompt here..." :rows="6" help="Max 500 characters" class="mb-1" />
        <div v-if="systemPromptError" class="text-red-600 text-sm mb-3">{{ systemPromptError }}</div>

        <BaseTextarea id="user-prompt-textarea" :disabled="true" disa label="User Prompt"
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