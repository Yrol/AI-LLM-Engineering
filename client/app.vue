<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <header class="bg-blue-600 text-white py-4 px-6 shadow">
      <NuxtLink to="/" class="text-2xl font-bol">LLM Engineering</NuxtLink>
    </header>

    <main class="flex-1 flex flex-row items-start justify-center">
      <!-- Navigation -->
      <nav class="w-64 min-h-screen bg-blue-50 flex flex-col gap-3 px-6 py-10">
        <!-- OpenAI section with sub-items -->
        <div>
          <NuxtLink to="/openai/openai" class="text-lg text-blue-700 font-semibold hover:underline text-left">OpenAI</NuxtLink>
          <div class="pl-4 flex flex-col gap-1 mt-1">
            <NuxtLink to="/openai/askanything" class="text-base text-blue-600 hover:underline text-left">Ask anything</NuxtLink>
            <NuxtLink to="/openai/websummeriser" class="text-base text-blue-600 hover:underline text-left">Web summerizer</NuxtLink>
            <NuxtLink to="/openai/brochure" class="text-base text-blue-600 hover:underline text-left">Brochure</NuxtLink>
          </div>
        </div>
        <NuxtLink to="/ollama/ollama" class="text-lg text-blue-700 hover:underline font-medium text-left mt-2">Ollama</NuxtLink>
      </nav>
      <!-- Page Content -->
      <NuxtPage />
    </main>
  </div>
</template>

