<script setup>
import ChatComponent from '~/components/ChatComponent.vue';
import BaseTextarea from '~/components/BaseTextarea.vue'
import { ref } from 'vue';

const userPromptErrorGeneric = ref('')
const userPromptAiAssistantGeneric = ref(`You are a helpful assistant for an Airline called FlightAI. 
Give short, courteous answers, no more than 1 sentence. 
Always be accurate. If you don't know the answer, say so.`)

var messagesAiAssistantGeneric = ref([
  // { text: 'Testing 123!', sender: 'assistant', created_at: 1669900800000 }
]);

const currentUser = {
  id: 'user',
  name: 'user'
};

const loading = ref(false)

function updateAiAssistantMessageGeneric(message, image) {
  messagesAiAssistantGeneric.value.push({ text: message, image_base64: image, sender: 'assistant', created_at: new Date() });
}

async function handleAiAssistantSendMessageGeneric(message) {
  let valid = true

  if (!userPromptAiAssistantGeneric.value.trim()) {
    userPromptErrorGenericGeneric.value = 'User Prompt is required.'
    valid = false
  }

  if (!valid) return

  messagesAiAssistantGeneric.value.push(message);
  // console.log('All messages:', messages.value);

  const formattedMessages = messagesAiAssistantGeneric.value.map(msg => ({
    role: msg.sender,
    content: msg.text
  }));

  loading.value = true

  fetch("http://localhost:8000/api/open_ai_ticketing_assistant/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      messages: formattedMessages,
      prompt: userPromptAiAssistantGeneric.value
    })
  })
    .then(response => response.json())
    .then(data => {
      updateAiAssistantMessageGeneric(data.reply.message, data.reply.image_base64 || null)
    })
    .catch(error => {
      console.error("Error:", error);
  }).finally(() => {
    loading.value = false;
  });
}

</script>

<template>
  <div class="w-full max-w-4xl mx-auto">
    <section class="mt-8">
      <h3 class="text-lg font-bold mb-4 border-b pb-2">OpenAI Assistant Experiment</h3>
      <h4 class="text-lg font-bold">Ticketing AI Assistant - Using tools</h4>

      <BaseTextarea id="user-prompt-textarea" :disabled="true" label="User Prompt generic"
          v-model="userPromptAiAssistantGeneric" :rows="3"
          help="Max 500 characters" class="mb-1" />

      <div v-if="userPromptErrorGeneric" class="text-red-600 text-sm mb-3">{{ userPromptErrorGeneric }}</div>

      <ChatComponent
        :messages="messagesAiAssistantGeneric"
        :currentUser="currentUser"
        @send-message="handleAiAssistantSendMessageGeneric"
        :loading="loading"
      />
    </section>
  </div>
</template>
