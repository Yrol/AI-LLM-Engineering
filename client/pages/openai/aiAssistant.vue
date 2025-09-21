<script setup>
import ChatComponent from '~/components/ChatComponent.vue';
import { ref } from 'vue';

var messages = ref([
  // { text: 'Testing 123!', sender: 'assistant', created_at: 1669900800000 }
]);

const currentUser = {
  id: 'user',
  name: 'user'
};

const loading = ref(false)

function updateMessages(message) {
  messages.value.push({ text: message, sender: 'assistant', created_at: new Date() });
}

async function handleSendMessage(message) {
  messages.value.push(message);
  // console.log('All messages:', messages.value);

  const formattedMessages = messages.value.map(msg => ({
    role: msg.sender,
    content: msg.text
  }));

  loading.value = true

  fetch("http://localhost:8000/api/open_ai_assistant/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(formattedMessages)
  })
    .then(response => response.json())
    .then(data => {
      updateMessages(data.reply)
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
      <h3 class="text-lg font-bold mb-4 border-b pb-2">OpenAI Assistant</h3>
      <ChatComponent
        :messages="messages"
        :currentUser="currentUser"
        @send-message="handleSendMessage"
        :loading="loading"
      />
    </section>
  </div>
</template>
