<template>
  <div class="chat-box">
    <div ref="messagesBox" class="chat-messages">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['chat-message', { 'own-message': message.sender === currentUser.id }]"
      >
        <!-- Render text -->
        <div v-if="message.text">
          <MarkdownRenderer :content="message.text" />
        </div>

        <!-- Render image if present -->
        <div v-if="message.image_base64" class="chat-image">
          <img
            :src="`data:image/png;base64,${message.image_base64}`"
            alt="AI generated"
          />
        </div>

        <span class="timestamp">{{ formatTimestamp(message.created_at) }}</span>
      </div>
    </div>

    <!-- Input area -->
    <div class="chat-input">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        placeholder="Type a message..."
        :disabled="props.loading"
      />
      <button @click="sendMessage" :disabled="props.loading">
        <span v-if="props.loading">Loading...</span>
        <span v-else>Send</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue';
import MarkdownRenderer from '~/components/MarkdownRenderer.vue'

// Props
const props = defineProps({
  currentUser: { type: Object, required: true },
  messages: { type: Array, required: false },
  loading: { type: Boolean, default: false }
});

const emit = defineEmits(['send-message']);

const newMessage = ref('');
const messagesBox = ref(null);

function formatTimestamp(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC'
  });
}

function sendMessage() {
  if (newMessage.value.trim() !== '') {
    emit('send-message', {
      text: newMessage.value,
      sender: props.currentUser.id,
      created_at: Date.now(),
    });
    newMessage.value = '';
  }
}

watch(
  () => props.messages,
  () => {
    nextTick(() => {
      if (messagesBox.value) {
        messagesBox.value.scrollTop = messagesBox.value.scrollHeight;
      }
    });
  },
  { deep: true }
);
</script>

<style scoped>
.chat-box {
  display: flex;
  flex-direction: column;
  border: 1px solid #ccc;
  height: 400px;
  /* width: 300px; */
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}
.chat-input {
  display: flex;
  border-top: 1px solid #eee;
}
.chat-input input {
  flex: 1;
  padding: 10px;
}
.chat-input button {
  padding: 10px;
}
.chat-message {
  margin: 5px 0;
  padding: 6px 12px;
  border-radius: 15px;
  background: #f0f0f0;
  max-width: 75%;
  word-break: break-word;
}
.own-message {
  background: #d1e7ff;
  align-self: flex-end;
  color: #115293;
}
.timestamp {
  font-size: 0.75em;
  color: #999;
  margin-left: 8px;
}

.chat-image {
  margin-top: 8px;
  display: flex;
  justify-content: flex-start; /* align left */
}

.chat-image img {
  max-width: 50%;              /* reduce size to 50% */
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
}
</style>
