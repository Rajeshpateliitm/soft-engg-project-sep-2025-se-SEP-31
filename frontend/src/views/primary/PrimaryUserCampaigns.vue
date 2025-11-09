<template>
  <div class="campaigns-container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Waste Management Campaigns</h2>
    </div>

    <!-- Search and Filter -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="input-group">
          <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
          <input 
            type="text" 
            class="form-control" 
            placeholder="Search campaigns..." 
            v-model="searchQuery"
          >
        </div>
      </div>
      <div class="col-md-3">
        <select class="form-select" v-model="statusFilter">
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="upcoming">Upcoming</option>
          <option value="completed">Completed</option>
        </select>
      </div>
      <div class="col-md-3">
        <select class="form-select" v-model="categoryFilter">
          <option value="">All Categories</option>
          <option value="recycling">Recycling</option>
          <option value="composting">Composting</option>
          <option value="cleanup">Cleanup</option>
          <option value="education">Education</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Loading campaigns...</p>
    </div>

    <!-- Campaigns Grid -->
    <div v-else class="row g-4">
      <div 
        v-for="campaign in filteredCampaigns" 
        :key="campaign.id" 
        class="col-md-6 col-lg-4"
      >
        <div class="card h-100 campaign-card">
          <div class="position-relative">
            <img 
              :src="campaign.image" 
              class="card-img-top" 
              :alt="campaign.title"
              style="height: 160px; object-fit: cover;"
            >
            <span class="badge position-absolute top-0 end-0 m-2" :class="getStatusBadgeClass(campaign.status)">
              {{ formatStatus(campaign.status) }}
            </span>
          </div>
          <div class="card-body d-flex flex-column">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="card-title mb-1">{{ campaign.title }}</h5>
              <span class="badge" :class="getCategoryBadgeClass(campaign.category)">
                {{ campaign.category }}
              </span>
            </div>
            <p class="card-text text-muted small mb-3">
              <i class="bi bi-calendar-event me-1"></i> 
              {{ formatDate(campaign.startDate) }}
              <span v-if="campaign.location" class="ms-2">
                <i class="bi bi-geo-alt me-1"></i>{{ campaign.location }}
              </span>
            </p>
            <p class="card-text flex-grow-1">
              {{ campaign.description && campaign.description.length > 100 ? campaign.description.substring(0, 100) + '...' : (campaign.description || 'No description available') }}
            </p>
            <div class="mt-3">
              <div class="d-grid gap-2">
                <button 
                  v-if="!campaign.is_registered"
                  class="btn btn-primary"
                  @click="registerCampaign(campaign.id)"
                  :disabled="isRegistering === campaign.id"
                >
                  <span v-if="isRegistering === campaign.id" class="spinner-border spinner-border-sm me-2" role="status"></span>
                  <i v-else class="bi bi-person-plus me-2"></i>
                  {{ isRegistering === campaign.id ? 'Registering...' : 'Register' }}
                </button>
                <button 
                  v-else
                  class="btn btn-success"
                  disabled
                >
                  <i class="bi bi-check-circle me-2"></i>Registered
                </button>
                <button 
                  class="btn btn-outline-secondary"
                  @click="viewCampaign(campaign.id)"
                >
                  View Details
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && filteredCampaigns.length === 0" class="text-center py-5">
      <div class="mb-3">
        <i class="bi bi-calendar-x" style="font-size: 3rem; color: #6c757d;"></i>
      </div>
      <h5>No campaigns found</h5>
      <p class="text-muted">There are no campaigns matching your filters.</p>
      <button class="btn btn-outline-primary" @click="resetFilters">
        Clear Filters
      </button>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
      {{ successMessage }}
      <button type="button" class="btn-close" @click="successMessage = ''"></button>
    </div>
    <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ errorMessage }}
      <button type="button" class="btn-close" @click="errorMessage = ''"></button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../../services/api';

const router = useRouter();

// Data
const campaigns = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const statusFilter = ref('');
const categoryFilter = ref('');
const isRegistering = ref(null);
const successMessage = ref('');
const errorMessage = ref('');

// Default image for campaigns without image_url
const defaultImage = 'https://images.unsplash.com/photo-1466611653911-95081537e5b7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80';

// Fetch campaigns from backend
const fetchCampaigns = async () => {
  try {
    loading.value = true;
    const response = await api.get('/primary/campaigns');
    const data = response.data;
    
    // Transform backend data to frontend format
    campaigns.value = data.campaigns.map(campaign => {
      const eventDate = campaign.event_datetime ? new Date(campaign.event_datetime) : null;
      const now = new Date();
      
      // Determine status based on event_datetime
      let status = 'upcoming';
      if (eventDate) {
        if (eventDate < now) {
          status = 'completed';
        } else if (eventDate <= new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)) {
          // Within 7 days
          status = 'active';
        }
      }
      
      // Derive category from description (simple keyword matching)
      let category = 'education'; // default
      const desc = (campaign.description || '').toLowerCase();
      if (desc.includes('recycl') || desc.includes('plastic') || desc.includes('e-waste')) {
        category = 'recycling';
      } else if (desc.includes('compost')) {
        category = 'composting';
      } else if (desc.includes('cleanup') || desc.includes('clean up')) {
        category = 'cleanup';
      } else if (desc.includes('workshop') || desc.includes('seminar') || desc.includes('learn')) {
        category = 'education';
      }
      
      return {
        id: campaign.id,
        title: campaign.name,
        description: campaign.description || '',
        category: category,
        status: status,
        startDate: eventDate ? eventDate.toISOString().split('T')[0] : null,
        endDate: eventDate ? eventDate.toISOString().split('T')[0] : null,
        event_datetime: campaign.event_datetime,
        location: campaign.location,
        participants: 0, // Will be updated if backend provides this
        goal: 100, // Default goal
        image: campaign.image_url || defaultImage,
        is_registered: campaign.is_registered || false
      };
    });
  } catch (error) {
    console.error('Error fetching campaigns:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to load campaigns. Please try again.';
    campaigns.value = [];
  } finally {
    loading.value = false;
  }
};

// Computed property for filtered campaigns
const filteredCampaigns = computed(() => {
  return campaigns.value.filter(campaign => {
    const matchesSearch = !searchQuery.value || 
      campaign.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (campaign.description && campaign.description.toLowerCase().includes(searchQuery.value.toLowerCase()));
    
    const matchesStatus = !statusFilter.value || campaign.status === statusFilter.value;
    const matchesCategory = !categoryFilter.value || campaign.category === categoryFilter.value;
    
    return matchesSearch && matchesStatus && matchesCategory;
  });
});

// Format date for display
const formatDate = (dateString) => {
  if (!dateString) return 'TBD';
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

// Format status for display
const formatStatus = (status) => {
  return status.charAt(0).toUpperCase() + status.slice(1);
};

// Get badge class based on status
const getStatusBadgeClass = (status) => {
  const classes = {
    active: 'bg-success',
    upcoming: 'bg-primary',
    completed: 'bg-secondary'
  };
  return classes[status] || 'bg-secondary';
};

// Get badge class based on category
const getCategoryBadgeClass = (category) => {
  const classes = {
    recycling: 'bg-info text-dark',
    composting: 'bg-success',
    cleanup: 'bg-warning text-dark',
    education: 'bg-primary'
  };
  return classes[category] || 'bg-secondary';
};

// Register for a campaign
const registerCampaign = async (campaignId) => {
  try {
    isRegistering.value = campaignId;
    errorMessage.value = '';
    successMessage.value = '';
    
    await api.post(`/primary/campaigns/${campaignId}/register`);
    
    // Update the campaign's registered status
    const campaign = campaigns.value.find(c => c.id === campaignId);
    if (campaign) {
      campaign.is_registered = true;
    }
    
    successMessage.value = 'Successfully registered for the campaign!';
  } catch (error) {
    console.error('Error registering for campaign:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to register for campaign. Please try again.';
  } finally {
    isRegistering.value = null;
  }
};

// View campaign details
const viewCampaign = (id) => {
  // For now, just show an alert with campaign details
  const campaign = campaigns.value.find(c => c.id === id);
  if (campaign) {
    alert(`${campaign.title}\n\n${campaign.description}\n\nLocation: ${campaign.location || 'TBD'}\nDate: ${formatDate(campaign.startDate)}`);
  }
};

// Reset all filters
const resetFilters = () => {
  searchQuery.value = '';
  statusFilter.value = '';
  categoryFilter.value = '';
};

// Lifecycle hook
onMounted(() => {
  fetchCampaigns();
});
</script>

<style scoped>
.campaigns-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem;
}

.campaign-card {
  border: none;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.campaign-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
}

.card-img-top {
  object-fit: cover;
  height: 160px;
}

.card-body {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-title {
  font-weight: 600;
  color: #2c3e50;
}

.badge {
  font-weight: 500;
  padding: 0.35em 0.65em;
  font-size: 0.75em;
  letter-spacing: 0.5px;
}

.modal-backdrop {
  opacity: 0.5;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .campaigns-container {
    padding: 0.5rem;
  }
  
  .card-title {
    font-size: 1.1rem;
  }
  
  .btn {
    padding: 0.375rem 0.75rem;
    font-size: 0.9rem;
  }
}

/* Animation for modal */
.modal.fade .modal-dialog {
  transition: transform 0.3s ease-out;
  transform: translateY(-50px);
}

.modal.show .modal-dialog {
  transform: none;
}

/* Custom scrollbar for the modal */
.modal-body {
  max-height: 70vh;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #dee2e6 #f8f9fa;
}

.modal-body::-webkit-scrollbar {
  width: 8px;
}

.modal-body::-webkit-scrollbar-track {
  background: #f8f9fa;
}

.modal-body::-webkit-scrollbar-thumb {
  background-color: #dee2e6;
  border-radius: 20px;
  border: 2px solid #f8f9fa;
}
</style>
