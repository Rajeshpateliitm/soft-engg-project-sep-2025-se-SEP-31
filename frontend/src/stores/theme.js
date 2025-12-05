/**
 * Theme Store - Manages application theme (light/dark mode)
 *
 * Features:
 * - Persists theme preference to localStorage
 * - Respects system color scheme preference
 * - Applies theme to document and body elements
 */

import { defineStore } from "pinia";

export const useThemeStore = defineStore("theme", {
  state: () => ({
    isDarkMode: false,
  }),

  getters: {
    /**
     * Get current theme name
     * @returns {string} "dark" or "light"
     */
    currentTheme: (state) => (state.isDarkMode ? "dark" : "light"),
  },

  actions: {
    /**
     * Initialize theme from localStorage or system preference
     * Priority: localStorage > system preference > default (light)
     */
    initTheme() {
      const savedTheme = localStorage.getItem("theme");

      if (savedTheme) {
        // Use saved preference
        this.isDarkMode = savedTheme === "dark";
      } else {
        // Check system preference
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        this.isDarkMode = prefersDark;
      }

      this.applyTheme();
    },

    /**
     * Toggle between light and dark theme
     */
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
      this.applyTheme();
      this.persistTheme();
    },

    /**
     * Set theme explicitly
     * @param {string} theme - "dark" or "light"
     */
    setTheme(theme) {
      this.isDarkMode = theme === "dark";
      this.applyTheme();
      this.persistTheme();
    },

    /**
     * Apply theme to DOM elements
     * Adds/removes "dark-mode" class from html and body
     */
    applyTheme() {
      const darkModeClass = "dark-mode";

      if (this.isDarkMode) {
        document.documentElement.classList.add(darkModeClass);
        document.body.classList.add(darkModeClass);
      } else {
        document.documentElement.classList.remove(darkModeClass);
        document.body.classList.remove(darkModeClass);
      }
    },

    /**
     * Persist theme preference to localStorage
     */
    persistTheme() {
      localStorage.setItem("theme", this.currentTheme);
    },
  },

  persist: true,
});