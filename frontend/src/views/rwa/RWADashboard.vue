<template>
  <div class="max-w-7xl mx-auto p-8">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Left Card - RWA Leaderboard -->
      <div class="bg-white rounded-lg shadow-lg p-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">RWA Leaderboard</h2>
        <div class="space-y-4 mb-8">
          <p class="text-lg text-gray-700 font-medium">RWA Rank #7</p>
          <p class="text-lg text-gray-700 font-medium">#Households</p>
        </div>
        <button 
          @click="$router.push('/rwa-dashboard/leaderboard')"
          class="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
        >
          Details &gt;&gt;
        </button>
      </div>

      <!-- Right Card - Pickup List -->
      <div class="bg-white rounded-lg shadow-lg p-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">PICKUP LIST of {{ currentDateMMDD }}</h2>
        <div class="space-y-4 mb-8">
          <p class="text-lg text-gray-800 font-semibold">TOTAL PICKUPS TODAY: 25</p>
          <p class="text-lg text-gray-800 font-semibold">TOTAL PICKUPS LEFT: 12</p>
          <p class="text-lg text-gray-800 font-semibold">PICKUPS COMPLETED: 10</p>
        </div>
        <div class="flex flex-col sm:flex-row gap-4">
          <button 
            @click="$router.push('/rwa-dashboard/monthly-pickup-summary')"
            class="bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
          >
            PICKUP SUMMARY
          </button>
          <button 
            @click="$router.push('/rwa-dashboard/pickup-details')"
            class="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Daily Details &gt;&gt;
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RWADashboard',
  computed: {
    currentDateMMDD() {
      const date = new Date()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const year = date.getFullYear()
      return `${month}-${day}-${year}`
    }
  }
}
</script>