<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-blue-600 text-white py-4 px-6 shadow w-full">
      <h1 class="text-2xl font-bold">LLM Engineering</h1>
    </header>
    <!-- Main Content Area: Sidebar + Page Content -->
    <div class="flex flex-1">
      <!-- Sidebar -->
      <aside class="w-64 bg-gray-100 border-r h-[calc(100vh-64px)] sticky top-0 flex flex-col">
        <nav class="flex flex-col gap-6 mt-10">
          <NuxtLink to="/openAi" class="text-lg text-blue-700 hover:underline text-center">OpenAI</NuxtLink>
          <NuxtLink to="/about" class="text-lg text-blue-700 hover:underline text-center">About</NuxtLink>
        </nav>
      </aside>
      <!-- Page Content -->
      <main class="flex-1 flex flex-col items-center justify-center p-8">
        <NuxtPage />
      </main>
    </div>
  </div>
</template>
