<script setup>
import { ref } from 'vue'
import BaseInput from '~/components/BaseInput.vue'
import LoadingButton from '~/components/LoadingButton.vue'
import MarkdownRenderer from '~/components/MarkdownRenderer.vue'


const companyName = ref('Drive')
const companyWebsite = ref('https://www.drive.com.au/')
const companyNameError = ref('')
const companyWebsiteError = ref('')
const companyBrochureLoading = ref(false)
const companyBrochureResponseMessage = ref('')
const companyBrochureErrorMessage = ref('')

async function handleSubmitCompanyBrochure() {
  
  // Reset errors
  companyNameError.value = ''
  companyWebsiteError.value = ''
  companyBrochureErrorMessage.value = ''

  // Reset content
  companyBrochureResponseMessage.value = ''

  let valid = true

  if (!companyName.value.trim()) {
    companyNameError.value = 'Company name is required'
    valid = false
  }

  if (!companyWebsite.value.trim()) {
    companyWebsiteError.value = 'Company website is required'
    valid = false
  }

  if (!valid) return

  companyBrochureLoading.value = true

  try {
    const res = await fetch('http://localhost:8000/api/open_ai_createbrochure/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        companyName: companyName.value,
        websiteUrl: companyWebsite.value
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
    companyBrochureResponseMessage.value = data
    // companyName.value = ''
  } catch (err) {
    companyBrochureErrorMessage.value = err.message || String(err)
  } finally {
    companyBrochureLoading.value = false
  }

}
</script>

<template>
  <div class="w-full max-w-2xl mx-auto">

    <section class="mt-8">
      <h3 class="text-lg font-bold mb-4 border-b pb-2">OpenAI Brochure</h3>
      <form @submit.prevent="handleSubmitCompanyBrochure" class="w-full max-w-2xl mx-auto p-6 bg-white rounded shadow">

        <BaseInput id="company-name" label="Company name" v-model="companyName" placeholder="Define company name" class="mb-3" />
        <div v-if="companyNameError" class="text-red-600 text-sm mb-3">{{ companyNameError }}</div>

        <BaseInput id="company-website" label="Company website" v-model="companyWebsite" placeholder="Define company website" class="mb-3" />
        <div v-if="companyWebsiteError" class="text-red-600 text-sm mb-3">{{ companyWebsiteError }}</div>

        <LoadingButton type="submit" :loading="companyBrochureLoading">
          <template #loading>
            Sending...
          </template>
          Send
        </LoadingButton>
        <MarkdownRenderer :content="companyBrochureResponseMessage" />
        <div v-if="companyBrochureErrorMessage" class="mt-4 text-red-600">
          {{ companyBrochureErrorMessage }}
        </div>
      </form>
    </section>
  </div>
</template>
