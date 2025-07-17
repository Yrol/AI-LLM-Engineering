<template>
    <div v-if="message" :class="['mt-4', colorClass, 'font-mono']">
        <p>
            {{ displayedText }}
            <span v-if="showCursor" class="animate-pulse">|</span>
        </p>
    </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
    message: {
        type: String,
        default: ''
    },
    colorClass: {
        type: String,
        default: 'text-green-600'
    },
    speed: { // Typing speed in ms per char
        type: Number,
        default: 30
    }
})

const displayedText = ref('')
const showCursor = computed(
    () => displayedText.value.length !== props.message.length
)

watch(
    () => props.message,
    async (newMsg, oldMsg) => {
        displayedText.value = ''
        if (!newMsg) return
        for (let i = 0; i <= newMsg.length; i++) {
            displayedText.value = newMsg.slice(0, i)
            await new Promise(res => setTimeout(res, props.speed))
        }
    }
)
</script>
