<template>
  <div class="theme-toggle-container">
    <button 
      class="theme-toggle-btn" 
      @click="toggleTheme"
      :aria-label="isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'"
      type="button"
    >
      <i :class="isDarkMode ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill'"></i>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useThemeStore } from '../stores/theme';

const themeStore = useThemeStore();
const isDarkMode = ref(themeStore.isDarkMode);

const toggleTheme = () => {
  themeStore.toggleTheme();
  isDarkMode.value = themeStore.isDarkMode;
};

onMounted(() => {
  isDarkMode.value = themeStore.isDarkMode;
  themeStore.$subscribe(() => {
    isDarkMode.value = themeStore.isDarkMode;
  });
});
</script>

<style scoped>
.theme-toggle-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 1rem;
}

.theme-toggle-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #2c3e50;
  font-size: 1.2rem;
  padding: 0;
}

.theme-toggle-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.theme-toggle-btn:active {
  transform: scale(0.95);
}

.theme-toggle-btn i {
  display: block;
  transition: transform 0.3s ease;
}

.theme-toggle-btn:hover i {
  transform: rotate(15deg);
}

/* Dark mode adjustments */
.dark-mode .theme-toggle-btn {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: #ffd700;
}

.dark-mode .theme-toggle-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .theme-toggle-btn {
    width: 36px;
    height: 36px;
    font-size: 1.1rem;
  }
}
</style>
