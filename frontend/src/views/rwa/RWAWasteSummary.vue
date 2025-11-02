<template>
  <div class="max-w-7xl mx-auto p-6">
    <h1 class="text-2xl font-bold text-gray-800 mb-6">MONTHLY HOUSEHOLD PERFORMANCE SUMMARY</h1>
    
    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div class="bg-white rounded-lg shadow-md p-6 text-center">
        <h3 class="text-lg font-semibold text-gray-800">Total Households</h3>
        <p class="text-3xl font-bold text-blue-600">320</p>
      </div>
      <div class="bg-white rounded-lg shadow-md p-6 text-center">
        <h3 class="text-lg font-semibold text-gray-800">Overall Segregation Rate</h3>
        <p class="text-3xl font-bold text-green-600">65%</p>
      </div>
      <div class="bg-white rounded-lg shadow-md p-6 text-center">
        <h3 class="text-lg font-semibold text-gray-800">Recycle/Reused Portion</h3>
        <p class="text-3xl font-bold text-purple-600">36%</p>
      </div>
    </div>

    <!-- Performance Table -->
    <div class="bg-white rounded-lg shadow-md overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Household Number</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Family Size</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Segregation Percentage</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Per Capita Dry (kg/day)</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Per Capita Wet (kg/day)</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Per Capita Hazardous (kg/day)</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Recycled/Reused/Donated (kg/week)</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Engagement Score</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="household in householdData" :key="household.number">
            <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ household.number }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ household.familySize }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ household.segregationPercentage }}%</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ household.perCapitaDry }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ household.perCapitaWet }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ household.perCapitaHazardous }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ household.recycled }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ household.engagementScore }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RWAWasteSummary',
  data() {
    return {
      householdData: [
        { number: 101, familySize: 2, segregationPercentage: 85.0, perCapitaDry: 0.85, perCapitaWet: 0.45, perCapitaHazardous: 0.08, recycled: 4.0, engagementScore: 785 },
        { number: 102, familySize: 4, segregationPercentage: 62.0, perCapitaDry: 1.10, perCapitaWet: 0.95, perCapitaHazardous: 0.08, recycled: 2.0, engagementScore: 523 },
        { number: 103, familySize: 6, segregationPercentage: 91.0, perCapitaDry: 0.70, perCapitaWet: 0.60, perCapitaHazardous: 0.04, recycled: 5.5, engagementScore: 882 },
        { number: 104, familySize: 3, segregationPercentage: 78.0, perCapitaDry: 0.65, perCapitaWet: 0.50, perCapitaHazardous: 0.07, recycled: 1.8, engagementScore: 460 },
        { number: 105, familySize: 2, segregationPercentage: 76.0, perCapitaDry: 0.95, perCapitaWet: 0.60, perCapitaHazardous: 0.06, recycled: 3.0, engagementScore: 724 }
      ]
    }
  }
}
</script>