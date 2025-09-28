<script setup>
import ChatComponent from '~/components/ChatComponent.vue';
import BaseTextarea from '~/components/BaseTextarea.vue'
import { ref } from 'vue';

const userPromptErrorGeneric = ref('')
const userPromptAiAssistantGeneric = ref('You are a helpful assistant')
const userPromptAiAssistantSpecific = ref(`You are a helpful assistant in a clothes store. You should try to gently encourage
the customer to try items that are on sale. Hats are 60% off, and most other items are 50% off.
For example, if the customer says 'I'm looking to buy a hat', 
you could reply something like, 'Wonderful - we have lots of hats - including several that are part of our sales event.'
Encourage the customer to buy hats if they are unsure what to get.`);



var messagesAiAssistantGeneric = ref([
  // { text: 'Testing 123!', sender: 'assistant', created_at: 1669900800000 }
]);

var messagesAiAssistantSpecific = ref([]);

const currentUser = {
  id: 'user',
  name: 'user'
};

const loading = ref(false)

function updateAiAssistantMessageGeneric(message) {
  messagesAiAssistantGeneric.value.push({ text: message, sender: 'assistant', created_at: new Date() });
}

function updateAiAssistantMessageSpecific(message) {
  messagesAiAssistantSpecific.value.push({ text: message, sender: 'assistant', created_at: new Date() });
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

  fetch("http://localhost:8000/api/open_ai_assistant/", {
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
      updateAiAssistantMessageGeneric(data.reply)
    })
    .catch(error => {
      console.error("Error:", error);
  }).finally(() => {
    loading.value = false;
  });
}

async function handleAiAssistantSendMessageSpecific(message) {

  let valid = true

  if (!userPromptAiAssistantSpecific.value.trim()) {
    userPromptErrorGeneric.value = 'User Prompt is required.'
    valid = false
  }

  if (!valid) return

  messagesAiAssistantSpecific.value.push(message);
  // console.log('All messages:', messages.value);

  const formattedMessages = messagesAiAssistantSpecific.value.map(msg => ({
    role: msg.sender,
    content: msg.text
  }));

  loading.value = true

  fetch("http://localhost:8000/api/open_ai_assistant/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      messages: formattedMessages,
      prompt: userPromptAiAssistantSpecific.value
    })
  })
    .then(response => response.json())
    .then(data => {
      updateAiAssistantMessageSpecific(data.reply)
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
      <h4 class="text-lg font-bold">OpenAI Assistant - Generic</h4>

      <BaseTextarea id="user-prompt-textarea" :disabled="true" label="User Prompt generic"
          v-model="userPromptAiAssistantGeneric" :rows="1"
          help="Max 500 characters" class="mb-1" />

      <div v-if="userPromptErrorGeneric" class="text-red-600 text-sm mb-3">{{ userPromptErrorGeneric }}</div>

      <ChatComponent
        :messages="messagesAiAssistantGeneric"
        :currentUser="currentUser"
        @send-message="handleAiAssistantSendMessageGeneric"
        :loading="loading"
      />
    </section>

    <section class="mt-8 mb-8">
      <h4 class="text-lg font-bold">OpenAI Assistant - Specific</h4>
      <BaseTextarea id="user-prompt-textarea" :disabled="false" label="User Prompt specific"
          v-model="userPromptAiAssistantSpecific" :rows="5"
          help="Max 500 characters" class="mb-1" />

      <div v-if="userPromptErrorSpecific" class="text-red-600 text-sm mb-3">{{ userPromptErrorSpecific }}</div> 
         
      <ChatComponent
        :messages="messagesAiAssistantSpecific"
        :currentUser="currentUser"
        @send-message="handleAiAssistantSendMessageSpecific"
        :loading="loading"
      />
    </section>
  </div>
</template>
