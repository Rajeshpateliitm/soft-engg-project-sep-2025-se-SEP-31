<template>
  <div class="max-w-2xl mx-auto p-6">
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Create Campaign</h1>
    
    <form @submit.prevent="createCampaign" class="bg-white rounded-lg shadow-md p-6 space-y-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">CAMPAIGN IMAGE</label>
        <input 
          type="file" 
          @change="handleImageUpload"
          accept="image/*"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">CAMPAIGN NAME</label>
        <input 
          type="text" 
          v-model="form.name"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">CAMPAIGN DETAILS</label>
        <textarea 
          v-model="form.details"
          required
          rows="4"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">CAMPAIGN LOCATION</label>
        <input 
          type="text" 
          v-model="form.location"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">CAMPAIGN DATE/TIME</label>
        <input 
          type="datetime-local" 
          v-model="form.datetime"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
      </div>

      <div class="text-center">
        <button 
          type="submit"
          class="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700"
        >
          CREATE
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'RWACreateCampaign',
  data() {
    return {
      form: {
        name: '',
        details: '',
        location: '',
        datetime: '',
        image: null
      }
    }
  },
  methods: {
    handleImageUpload(event) {
      this.form.image = event.target.files[0]
    },
    createCampaign() {
      console.log('Creating campaign:', this.form)
      this.$router.push('/rwa-dashboard/campaigns')
    }
  }
}
</script>