<template>
  <div class="max-w-7xl mx-auto p-6">
    <h1 class="text-2xl font-bold text-gray-800 mb-6">RWA LEADERBOARD</h1>
    
    <!-- Community Rank Section -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <div class="flex items-center space-x-6">
        <div class="flex-shrink-0">
          <div class="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center">
            <span class="text-white text-2xl font-bold">#7</span>
          </div>
        </div>
        <div>
          <p class="text-lg font-semibold text-gray-800">COMMUNITY RANK: 7</p>
          <p class="text-gray-600">YOUR SCORE: 12400 points</p>
          <p class="text-gray-600">REMARKS: RECYCLE LEADERBOARD</p>
        </div>
      </div>
    </div>

    <!-- Leaderboard Table -->
    <div class="bg-white rounded-lg shadow-md overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rank</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">RWA</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Points</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Remarks</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="item in leaderboardData" :key="item.rank" :class="{ 'bg-blue-50': item.rank === 7 }">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.rank }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ item.rwa }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ item.points }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ item.remarks }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-6">
      <button class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
        DETAILS &gt;&gt;
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RWALeaderboard',
  data() {
    return {
      leaderboardData: [
        { rank: 1, rwa: 'XXXXX', points: 1700, remarks: 'RECYCLE CHAMPION' },
        { rank: 2, rwa: 'XXXXX', points: 1500, remarks: 'RECYCLE STAR' },
        { rank: 3, rwa: 'XXXXX', points: 1400, remarks: 'RECYCLE STAR' },
        { rank: 4, rwa: 'XXXXX', points: 1300, remarks: 'RECYCLE MASTER' },
        { rank: 5, rwa: 'XXXXX', points: 1100, remarks: 'RECYCLE MASTER' },
        { rank: 6, rwa: 'XXXXX', points: 950, remarks: 'RECYCLE BOOSTER' },
        { rank: 7, rwa: 'XXXXX', points: 740, remarks: 'RECYCLE BOOSTER' },
        { rank: 8, rwa: 'XXXXX', points: 720, remarks: 'RECYCLE BOOSTER' }
      ]
    }
  }
}
</script>