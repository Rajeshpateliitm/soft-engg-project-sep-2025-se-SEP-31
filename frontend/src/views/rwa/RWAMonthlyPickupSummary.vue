<template>
  <div class="max-w-7xl mx-auto p-6">
    <h1 class="text-2xl font-bold text-gray-800 mb-6">MONTHLY WASTE PICKUP SUMMARY</h1>
    
    <!-- KPIs -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow-md p-6 text-center">
        <h3 class="text-lg font-semibold text-gray-800">TOTAL INCOMING PICKUPS</h3>
        <p class="text-3xl font-bold text-blue-600">320</p>
      </div>
      <div class="bg-white rounded-lg shadow-md p-6 text-center">
        <h3 class="text-lg font-semibold text-gray-800">TOTAL PICKUPS COMPLETED</h3>
        <p class="text-3xl font-bold text-green-600">260</p>
      </div>
      <div class="bg-white rounded-lg shadow-md p-6 text-center">
        <h3 class="text-lg font-semibold text-gray-800">TOTAL PENDING PICKUPS</h3>
        <p class="text-3xl font-bold text-yellow-600">16</p>
      </div>
      <div class="bg-white rounded-lg shadow-md p-6 text-center">
        <h3 class="text-lg font-semibold text-gray-800">TOTAL REJECTED PICKUPS</h3>
        <p class="text-3xl font-bold text-red-600">44</p>
      </div>
    </div>

    <!-- Bar Chart -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-bold text-gray-800 mb-4">Daily Pickups by Status (Last 30 Days)</h2>
      <div class="h-96 flex items-end justify-between space-x-1 border-b border-l border-gray-300 p-4">
        <div v-for="day in chartData" :key="day.day" class="flex flex-col items-center space-y-1">
          <div class="flex flex-col items-center space-y-1">
            <div 
              class="w-4 bg-green-500" 
              :style="{ height: (day.completed / maxValue * 200) + 'px' }"
              :title="`Completed: ${day.completed}`"
            ></div>
            <div 
              class="w-4 bg-yellow-500" 
              :style="{ height: (day.pending / maxValue * 200) + 'px' }"
              :title="`Pending: ${day.pending}`"
            ></div>
            <div 
              class="w-4 bg-red-500" 
              :style="{ height: (day.rejected / maxValue * 200) + 'px' }"
              :title="`Rejected: ${day.rejected}`"
            ></div>
          </div>
          <span class="text-xs text-gray-600 transform -rotate-45">{{ day.day }}</span>
        </div>
      </div>
      <div class="mt-4 flex justify-center space-x-6">
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 bg-green-500"></div>
          <span class="text-sm">Completed</span>
        </div>
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 bg-yellow-500"></div>
          <span class="text-sm">Pending</span>
        </div>
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 bg-red-500"></div>
          <span class="text-sm">Rejected</span>
        </div>
      </div>
    </div>

    <div class="mt-6">
      <button class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
        Export Data
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RWAMonthlyPickupSummary',
  data() {
    return {
      chartData: [
        { day: '1', completed: 8, pending: 2, rejected: 1 },
        { day: '2', completed: 12, pending: 1, rejected: 2 },
        { day: '3', completed: 10, pending: 3, rejected: 1 },
        { day: '4', completed: 15, pending: 2, rejected: 3 },
        { day: '5', completed: 9, pending: 4, rejected: 2 },
        { day: '6', completed: 11, pending: 1, rejected: 1 },
        { day: '7', completed: 13, pending: 2, rejected: 2 },
        { day: '8', completed: 14, pending: 3, rejected: 1 },
        { day: '9', completed: 8, pending: 2, rejected: 3 },
        { day: '10', completed: 16, pending: 1, rejected: 2 }
      ]
    }
  },
  computed: {
    maxValue() {
      return Math.max(...this.chartData.map(d => Math.max(d.completed, d.pending, d.rejected)))
    }
  }
}
</script>