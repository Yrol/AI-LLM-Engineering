<script setup>
import { ref } from 'vue'
import BaseTextarea from '~/components/BaseTextarea.vue'
import LoadingButton from '~/components/LoadingButton.vue'
import TypingEffect from '~/components/TypingEffect.vue'

const handleSubmitOllama = ref('')
const model = ref('tinyllama')
const role = ref('user')
const content = ref('Describe some of the business applications of Generative AI')
const ollamaChatResponseMessage = ref('')

const modelError = ref('')
const rolelError = ref('')
const contentError = ref('')
const ollamaChatErrorMessage = ref('')

const ollamaChatLoading = ref(false)

async function handleSubmitOllamaAskAnything() {

  modelError.value = ''
  rolelError.value = ''
  contentError.value = ''
  ollamaChatErrorMessage.value = ''

  let valid = true

  if (!model.value.trim()) {
    modelError.value = 'Model is required.'
    valid = false
  }

  if (!role.value.trim()) {
    rolelError.value = 'Role is required.'
    valid = false
  }

  if (!content.value.trim()) {
    contentError.value = 'Content is required.'
    valid = false
  }

  if (!valid) return

  ollamaChatLoading.value = true

  try {
    const res = await fetch('http://localhost:8000/api/ollamachat/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: model.value,
        messages: [
          {
            role: role.value,
            content: content.value
          }
        ],
        stream: false
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
    ollamaChatResponseMessage.value = data.message.content

  } catch (err) {
    ollamaChatErrorMessage.value = err.message || String(err)
  } finally {
    ollamaChatLoading.value = false
  }

}
</script>

<template>
  <div class="w-full max-w-2xl mx-auto">
    <section class="mt-8">
      <h3 class="text-lg font-bold mb-4 border-b pb-2">Ollama Experiment</h3>

      <form @submit.prevent="handleSubmitOllamaAskAnything"
        class="w-full max-w-2xl mx-auto p-6 bg-white rounded shadow">
        <BaseInput id="model" label="Model" v-model="model" placeholder="Define the model" class="mb-3" />
        <div v-if="modelError" class="text-red-600 text-sm mb-3">{{ modelError }}</div>

        <BaseInput id="role" label="Role" v-model="role" placeholder="Define the role" class="mb-3" />
        <div v-if="rolelError" class="text-red-600 text-sm mb-3">{{ rolelError }}</div>

        <BaseTextarea id="content-textarea" label="Content" v-model="content" placeholder="Type your content here..."
          :rows="6" help="Max 500 characters" class="mb-1" />
        <div v-if="contentError" class="text-red-600 text-sm mb-3">{{ contentError }}</div>

        <LoadingButton type="submit" :loading="ollamaChatLoading">
          <template #loading>
            Sending...
          </template>
          Send
        </LoadingButton>
        <TypingEffect :message="ollamaChatResponseMessage" color-class="text-blue-600" :speed="5" />
        <div v-if="ollamaChatErrorMessage" class="mt-4 text-red-600">
          {{ ollamaChatErrorMessage }}
        </div>
      </form>

    </section>
  </div>
</template>