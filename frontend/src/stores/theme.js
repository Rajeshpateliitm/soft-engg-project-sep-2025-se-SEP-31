import { defineStore } from 'pinia';

export const useThemeStore = defineStore('theme', {
  state: () => ({
    isDarkMode: false,
  }),

  getters: {
    currentTheme: (state) => state.isDarkMode ? 'dark' : 'light',
  },

  actions: {
    // Initialize theme from localStorage or system preference
    initTheme() {
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme) {
        this.isDarkMode = savedTheme === 'dark';
      } else {
        // Check system preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        this.isDarkMode = prefersDark;
      }
      this.applyTheme();
    },

    // Toggle theme
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
      this.applyTheme();
      localStorage.setItem('theme', this.isDarkMode ? 'dark' : 'light');
    },

    // Apply theme to document
    applyTheme() {
      if (this.isDarkMode) {
        document.documentElement.classList.add('dark-mode');
        document.body.classList.add('dark-mode');
      } else {
        document.documentElement.classList.remove('dark-mode');
        document.body.classList.remove('dark-mode');
      }
    },

    // Set theme explicitly
    setTheme(theme) {
      this.isDarkMode = theme === 'dark';
      this.applyTheme();
      localStorage.setItem('theme', theme);
    },
  },

  persist: true
});

