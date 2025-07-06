<template>
  <div class="min-h-screen flex flex-col">
    <header class="bg-blue-600 text-white py-4 px-6 shadow">
      <h1 class="text-2xl font-bold">LLM Engineering</h1>
    </header>

    <main class="flex-1 flex flex-col items-center justify-center">
      <nav class="flex flex-col gap-6">
        <NuxtLink to="/" class="text-lg text-blue-700 hover:underline text-center">OpenAI</NuxtLink>
        <NuxtLink to="/about" class="text-lg text-blue-700 hover:underline text-center">About</NuxtLink>
        <NuxtLink to="/contact" class="text-lg text-blue-700 hover:underline text-center">Contact</NuxtLink>
      </nav>
    </main>
  </div>
</template>