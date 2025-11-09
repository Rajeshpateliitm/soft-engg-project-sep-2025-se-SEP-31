import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '../services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userCategory: (state) => state.user?.user_category || null,
    userName: (state) => state.user?.username || state.user?.email || 'User',
    rwaRole: (state) => state.user?.rwa_role || null, // "admin", "collector", or null
  },

  actions: {
    // Initialize auth from localStorage
    initAuth() {
      const token = localStorage.getItem('access_token');
      const userStr = localStorage.getItem('user');
      
      if (token && userStr) {
        this.token = token;
        this.user = JSON.parse(userStr);
      }
    },

    // Set auth data
    setAuth(token, user) {
      this.token = token;
      this.user = user;
      localStorage.setItem('access_token', token);
      localStorage.setItem('user', JSON.stringify(user));
    },

    // Clear auth data
    clearAuth() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    },

    // Register user
    async register(userData) {
      try {
        // Only PRIMARY users can register through public sign-up
        // SECONDARY and TERTIARY users are provisioned by administrators

        const response = await api.post('/auth/register', {
          email: userData.email,
          password: userData.password,
          username: userData.fullName || userData.email.split('@')[0],
          house_number: userData.house_number || '',
          ward_number: userData.ward_number || '',
          family_members: userData.family_members || 1,
          pincode: userData.pincode || '',
          user_category: 'PRIMARY' // Always PRIMARY for public registration
        });

        if (response.data.access_token) {
          this.setAuth(response.data.access_token, response.data.user);
          return {
            success: true,
            user: response.data.user,
            token: response.data.access_token
          };
        }
        throw new Error('Registration failed');
      } catch (error) {
        console.error('Registration error:', error);
        return {
          success: false,
          error: error.response?.data?.error || error.message || 'Registration failed'
        };
      }
    },

    // Login user
    async login(email, password) {
      try {
        const response = await api.post('/auth/login', {
          email,
          password
        });

        if (response.data.access_token) {
          this.setAuth(response.data.access_token, response.data.user);
          return {
            success: true,
            user: response.data.user,
            token: response.data.access_token
          };
        }
        throw new Error('Login failed');
      } catch (error) {
        console.error('Login error:', error);
        return {
          success: false,
          error: error.response?.data?.error || error.message || 'Login failed'
        };
      }
    },

    // Logout
    logout() {
      this.clearAuth();
    },

    // Get current user info
    async getCurrentUser() {
      try {
        const response = await api.get('/auth/me');
        this.user = response.data;
        localStorage.setItem('user', JSON.stringify(response.data));
        return response.data;
      } catch (error) {
        console.error('Get user error:', error);
        this.clearAuth();
        throw error;
      }
    },

    // Get dashboard route based on user category and role
    getDashboardRoute() {
      const category = this.userCategory;
      if (!category) return '/';

      // For secondary users, check RWA role
      if (category === 'SECONDARY') {
        const rwaRole = this.rwaRole;
        if (rwaRole === 'collector') {
          return '/collector-dashboard';
        } else if (rwaRole === 'admin') {
          return '/secondary-dashboard';
        }
        // Default to secondary dashboard if role is unknown
        return '/secondary-dashboard';
      }

      const routeMap = {
        'PRIMARY': '/primary-dashboard',
        'SECONDARY': '/secondary-dashboard',
        'TERTIARY': '/tertiary-dashboard'
      };

      return routeMap[category] || '/';
    }
  },

  persist: true
});

