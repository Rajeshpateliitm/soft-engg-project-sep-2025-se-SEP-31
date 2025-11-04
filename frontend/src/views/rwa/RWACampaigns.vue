<template>
  <div class="max-w-7xl mx-auto p-6">
    <!-- Campaign Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div v-for="campaign in campaigns" :key="campaign.id" class="bg-white rounded-lg shadow-md overflow-hidden">
        <img :src="campaign.image" :alt="campaign.name" class="w-full h-48 object-cover bg-gray-200">
        <div class="p-4">
          <h3 class="font-semibold text-gray-800 mb-2">{{ campaign.name }}</h3>
          <p class="text-sm text-gray-600 mb-4">{{ campaign.details }}</p>
          <div class="flex space-x-2">
            <button 
              @click="updateCampaign(campaign.id)"
              class="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
            >
              UPDATE
            </button>
            <button 
              @click="deleteCampaign(campaign.id)"
              class="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700"
            >
              DELETE
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Campaign Button -->
    <div class="text-center">
      <button 
        @click="$router.push('/rwa-dashboard/create-campaign')"
        class="bg-green-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-green-700"
      >
        CREATE CAMPAIGNS
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RWACampaigns',
  data() {
    return {
      campaigns: [
        {
          id: 1,
          name: 'Event A',
          image: '/api/placeholder/300/200',
          details: 'SPHIRA Community Cleanup Drive – 01/11/2025 – 9:00 AM – Near pool area'
        },
        {
          id: 2,
          name: 'Event B',
          image: '/api/placeholder/300/200',
          details: 'Recycling Awareness Workshop – 05/11/2025 – 2:00 PM – Community Hall'
        },
        {
          id: 3,
          name: 'Event C',
          image: '/api/placeholder/300/200',
          details: 'Waste Segregation Training – 10/11/2025 – 10:00 AM – Main Gate'
        }
      ]
    }
  },
  methods: {
    updateCampaign(id) {
      console.log('Update campaign:', id)
    },
    deleteCampaign(id) {
      this.campaigns = this.campaigns.filter(c => c.id !== id)
    }
  }
}
</script>