<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter.js';

const counter = useCounterStore();
const message = ref('Welcome to Windsurf App!');
</script>

<template>
  <div class="text-center">
    <h1 class="text-4xl font-bold text-gray-900 mb-6">{{ message }}</h1>
    <p class="text-lg text-gray-600 mb-8">
      A modern full-stack application built with Vue 3 and FastAPI
    </p>
    
    <div class="bg-white p-6 rounded-lg shadow-md max-w-md mx-auto">
      <h2 class="text-2xl font-semibold mb-4">Counter Example</h2>
      <p class="text-4xl font-bold mb-6">{{ counter.count }}</p>
      <div class="space-x-4">
        <button 
          @click="counter.increment()" 
          class="btn btn-primary"
        >
          Increment
        </button>
        <button 
          @click="counter.count = 0" 
          class="btn btn-outline"
        >
          Reset
        </button>
      </div>
    </div>
  </div>
</template>
