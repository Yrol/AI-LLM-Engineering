<script setup>
import { ref } from 'vue'
import BaseTextarea from '~/components/BaseTextarea.vue'
import LoadingButton from '~/components/LoadingButton.vue'
import JsonViewer from '~/components/JsonViewer.vue'


const contextPrompt = ref('Pipelines are a high level API for inference of LLMs with common tasks')
const contextError = ref('')
const questionPrompt = ref('What are Hugging Face pipelines?')
const questionError = ref('')
const loading = ref(false)
const responseMessage = ref('')
const errorMessage = ref('')

async function handleSubmit() {
  contextError.value = ''
  questionError.value = ''
  responseMessage.value = ''

  let valid = true

  if (!contextPrompt.value.trim()) {
    contextError.value = 'Context is required'
    valid = false
  }

  if (!questionPrompt.value.trim()) {
    questionError.value = 'Question is required'
    valid = false
  }

  if (!valid) return

  loading.value = true

  try {
      const res = await fetch('http://localhost:8000/api/huggingface_question_answering/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        context: contextPrompt.value,
        question: questionPrompt.value
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
            <h3 class="text-lg font-bold mb-4 border-b pb-2">Question Answering</h3>
            <p>
                Question answering tasks return an answer given a question. 
                If you’ve ever asked a virtual assistant like Alexa, Siri or Google what the weather is, then you’ve used a question answering model before. There are two common types of question answering tasks:
            </p>
            <ul class="space-y-4">
                <li>
                    <ul class="list-disc list-inside pl-4 mt-1 space-y-1 text-gray-700">
                    <li>Extractive: extract the answer from the given context.</li>
                    <li>Abstractive: generate an answer from the context that correctly answers the question.</li>
                    </ul>
                </li>
            </ul>
        </div>
        </section>
    </div>

    <section class="mt-8">
      <form @submit.prevent="handleSubmit" class="w-full max-w-2xl mx-auto p-6 bg-white rounded shadow">

        <BaseTextarea id="context-textarea" label="Context" v-model="contextPrompt"
          placeholder="Type your context here..." :rows="6" help="Max 500 characters" class="mb-1" />
        <div v-if="contextError" class="text-red-600 text-sm mb-3">{{ contextError }}</div>

        <BaseTextarea id="question-textarea" label="Question" v-model="questionPrompt"
          placeholder="Type your question here..." :rows="6" help="Max 500 characters" class="mb-1" />
        <div v-if="questionError" class="text-red-600 text-sm mb-3">{{ questionError }}</div>

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