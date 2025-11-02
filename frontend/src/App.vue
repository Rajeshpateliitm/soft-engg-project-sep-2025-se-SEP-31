<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm">
      <div class="container mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <div class="text-xl font-semibold text-gray-800">Windsurf App</div>
          <div class="space-x-4">
            <RouterLink to="/" class="text-gray-700 hover:text-blue-600">Home</RouterLink>
            <RouterLink to="/about" class="text-gray-700 hover:text-blue-600">About</RouterLink>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
/* Add any global styles here */
</style>
