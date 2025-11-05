<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm">
      <div class="container mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          
        
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
