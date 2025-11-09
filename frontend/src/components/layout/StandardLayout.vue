<template>
  <div class="standard-layout">
    <StandardNavbar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import StandardNavbar from './StandardNavbar.vue';
</script>

<style scoped>
.standard-layout {
  min-height: 100vh;
}

.main-content {
  padding-top: 76px; /* Account for fixed navbar */
}
</style>

