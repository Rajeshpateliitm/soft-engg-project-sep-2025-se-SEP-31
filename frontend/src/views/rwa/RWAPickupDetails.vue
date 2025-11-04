<template>
  <div class="max-w-7xl mx-auto p-6">
    <h1 class="text-2xl font-bold text-gray-800 mb-6">PICKUP DETAILS OF {{ currentDate }}</h1>
    
    <div class="bg-white rounded-lg shadow-md overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">REQUEST NO.</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">USER ID</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">PICKUP LOCATION</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">DATE OF PICKUP</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">TIME OF PICKUP</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">DISPOSAL</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">QUANTITY</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">STATUS</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ACTIONS</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="pickup in pickupData" :key="pickup.requestNo">
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ pickup.requestNo }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ pickup.userId }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ pickup.location }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ pickup.date }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ pickup.time }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ pickup.disposal }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ pickup.quantity }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ pickup.status }}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm space-x-2">
              <button 
                @click="acceptPickup(pickup.requestNo)"
                class="bg-green-600 text-white px-3 py-1 rounded text-xs hover:bg-green-700"
              >
                Accept
              </button>
              <button 
                @click="rejectPickup(pickup.requestNo)"
                class="bg-red-600 text-white px-3 py-1 rounded text-xs hover:bg-red-700"
              >
                Reject
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RWAPickupDetails',
  data() {
    return {
      pickupData: [
        { requestNo: 'AAAAA', userId: 'BBB', location: 'CCCCC', date: '01_11_24', time: '09:30:00', disposal: 'XY', quantity: '5kg', status: 'Pending' },
        { requestNo: 'BBBBB', userId: 'CCC', location: 'DDDDD', date: '01_11_24', time: '10:15:00', disposal: 'XZ', quantity: '3kg', status: 'Pending' },
        { requestNo: 'CCCCC', userId: 'DDD', location: 'EEEEE', date: '01_11_24', time: '11:00:00', disposal: 'YZ', quantity: '7kg', status: 'Pending' }
      ]
    }
  },
  computed: {
    currentDate() {
      return new Date().toLocaleDateString('en-GB').replace(/\//g, '-')
    }
  },
  methods: {
    acceptPickup(requestNo) {
      const pickup = this.pickupData.find(p => p.requestNo === requestNo)
      if (pickup) pickup.status = 'Accepted'
    },
    rejectPickup(requestNo) {
      const pickup = this.pickupData.find(p => p.requestNo === requestNo)
      if (pickup) pickup.status = 'Rejected'
    }
  }
}
</script>