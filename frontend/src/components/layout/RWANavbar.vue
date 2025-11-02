<template>
  <div class="min-h-screen bg-gray-50 relative">
    <!-- Navigation Bar -->
    <nav class="bg-white border border-blue-300 rounded-lg mx-4 mt-4 shadow-sm relative h-14">
      <!-- Left Section -->
      <div class="absolute left-6 space-x-4">
        <router-link 
          to="/rwa-dashboard" 
          class="text-blue-600 hover:text-blue-800 font-medium"
        >
          DASHBOARD
        </router-link>
        <span class="text-gray-400">|</span>
        <router-link 
          to="/rwa-dashboard/waste-summary" 
          class="text-blue-600 hover:text-blue-800 font-medium"
        >
          WASTE SUMMARY
        </router-link>
        <span class="text-gray-400">|</span>
        <router-link 
          to="/rwa-dashboard/campaigns" 
          class="text-blue-600 hover:text-blue-800 font-medium"
        >
          CAMPAIGNS
        </router-link>
      </div>

      <!-- Right Section -->
      <div class="absolute right-6  space-x-4 text-blue-600 font-medium">
        <span>&lt;&lt;{{ formattedTimestamp }}&gt;&gt;</span>
        <span>&lt;&lt;MEMBER&gt;&gt;</span>
        <button 
          @click="logout" 
          class="hover:text-blue-800 transition-colors"
        >
          LOGOUT
        </button>
      </div>
    </nav>

    <!-- Routed View -->
    <router-view class="pt-6" />
  </div>
</template>

<script>
export default {
  name: 'RWANavbar',
  data() {
    return {
      timestamp: new Date()
    }
  },
  computed: {
    formattedTimestamp() {
      // Format: MM-DD-YYYY HH:MM:SS (US format)
      const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      }
      const formatted = new Intl.DateTimeFormat('en-US', options).format(this.timestamp)
      return formatted.replace(/\//g, '-')
    }
  },
  mounted() {
    this.updateTimestamp()
    setInterval(this.updateTimestamp, 1000)
  },
  methods: {
    updateTimestamp() {
      this.timestamp = new Date()
    },
    logout() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
nav {
  font-family: 'Inter', sans-serif;
  position: relative;
}
</style>
