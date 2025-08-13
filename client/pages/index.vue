<template>
  <div class="w-full max-w-2xl mx-auto">

    <section class="mt-8">
      <h3 class="text-lg font-bold mb-4 border-b pb-2 text-gray-900">LLM Engineering</h3>
      <p class="mb-6 text-gray-700">
        An experimental project featuring both backend and frontend functionality to interact with Large Language Models
        (LLMs).
        For details, see the Current capabilities section below.
      </p>

      <!-- Current capabilities -->
      <div class="bg-white shadow-md rounded-lg p-6">
        <h4 class="text-xl font-bold mb-4 border-b border-gray-300 pb-2 text-gray-900">
          Current capabilities
        </h4>
        <ul class="space-y-4">
          <li>
            <strong class="text-lg text-indigo-600">OpenAI</strong>
            <ul class="list-disc list-inside pl-4 mt-1 space-y-1 text-gray-700">
              <li>Web summarizer (supports user and system prompts) – cloud based</li>
              <li>Generic chat capabilities querying via API calls – cloud based</li>
            </ul>
          </li>
          <li>
            <strong class="text-lg text-indigo-600">Ollama (TinyLlama)</strong>
            <ul class="list-disc list-inside pl-4 mt-1 space-y-1 text-gray-700">
              <li>Generic chat capabilities querying via API calls – local LLM</li>
            </ul>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>
