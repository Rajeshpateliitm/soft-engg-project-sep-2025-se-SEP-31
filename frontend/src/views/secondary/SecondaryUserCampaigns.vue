<template>
  <div class="campaigns-container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Waste Management Campaigns</h2>
      <button class="btn btn-primary" @click="navigateToCreateCampaign">
        <i class="bi bi-plus-lg me-2"></i>Create Campaign
      </button>
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

    <!-- Error Message -->
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>

    <!-- Campaigns Grid -->
    <div v-if="!loading" class="row g-4">
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
              <span v-if="campaign.event_datetime" class="ms-2">
                <i class="bi bi-clock me-1"></i>{{ formatTime(campaign.event_datetime) }}
              </span>
            </p>
            <p class="card-text text-muted small mb-2" v-if="campaign.location">
              <i class="bi bi-geo-alt me-1"></i>
              {{ campaign.location }}
            </p>
            <p class="card-text flex-grow-1">
              {{ campaign.description.substring(0, 100) }}{{ campaign.description.length > 100 ? '...' : '' }}
            </p>
            <div class="mt-3">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <div class="progress flex-grow-1 me-2" style="height: 8px;">
                  <div 
                    class="progress-bar" 
                    role="progressbar" 
                    :style="{ width: campaign.progress + '%' }"
                    :aria-valuenow="campaign.progress" 
                    aria-valuemin="0" 
                    aria-valuemax="100"
                  ></div>
                </div>
                <span class="text-muted small">{{ campaign.participants }}/{{ campaign.goal }} participants</span>
              </div>
              <div class="d-grid gap-2">
                <button 
                  class="btn btn-outline-primary"
                  @click="viewCampaign(campaign.id)"
                >
                  View Details
                </button>
              </div>
              <div class="d-flex gap-2 mt-2">
                <button 
                  class="btn btn-outline-warning flex-grow-1"
                  @click="updateCampaign(campaign.id)"
                  title="Update campaign"
                >
                  <i class="bi bi-pencil me-1"></i>Update
                </button>
                <button 
                  class="btn btn-outline-danger flex-grow-1"
                  @click="deleteCampaign(campaign.id)"
                  title="Delete campaign"
                >
                  <i class="bi bi-trash me-1"></i>Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Loading campaigns...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredCampaigns.length === 0 && !errorMessage" class="text-center py-5">
      <div class="mb-3">
        <i class="bi bi-calendar-x" style="font-size: 3rem; color: #6c757d;"></i>
      </div>
      <h5>No campaigns found</h5>
      <p class="text-muted">{{ campaigns.length === 0 ? 'Create your first campaign to get started!' : 'There are no campaigns matching your filters.' }}</p>
      <button v-if="campaigns.length > 0" class="btn btn-outline-primary" @click="resetFilters">
        Clear Filters
      </button>
      <button v-else class="btn btn-primary" @click="navigateToCreateCampaign">
        Create Campaign
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '@/services/api';

const router = useRouter();
const route = useRoute();

const loading = ref(true);
const errorMessage = ref('');
const campaigns = ref([]);
const searchQuery = ref('');
const statusFilter = ref('');
const categoryFilter = ref('');

// Default image for campaigns without images
const defaultImage = 'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80';

// Fetch campaigns from backend
const fetchCampaigns = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';
    const response = await api.get('/secondary/campaigns');
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
        participants: campaign.registration_count || 0,
        goal: 100, // Default goal (can be updated later if needed)
        progress: Math.min(((campaign.registration_count || 0) / 100) * 100, 100),
        image: campaign.image_url || defaultImage
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
    const matchesSearch = campaign.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         campaign.description.toLowerCase().includes(searchQuery.value.toLowerCase());
    
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

// Format time for display
const formatTime = (dateTimeString) => {
  if (!dateTimeString) return '';
  const date = new Date(dateTimeString);
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
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

// View campaign details
const viewCampaign = (id) => {
  // Could navigate to a detailed view page
  const campaign = campaigns.value.find(c => c.id === id);
  if (campaign) {
    alert(`Campaign: ${campaign.title}\n\nDescription: ${campaign.description}\n\nLocation: ${campaign.location}\n\nDate: ${formatDate(campaign.startDate)}\n\nParticipants: ${campaign.participants}`);
  }
};

// Navigate to create campaign page
const navigateToCreateCampaign = () => {
  router.push('/secondary-dashboard/create-campaign');
};

// Reset all filters
const resetFilters = () => {
  searchQuery.value = '';
  statusFilter.value = '';
  categoryFilter.value = '';
};

// Update campaign
const updateCampaign = async (id) => {
  const campaign = campaigns.value.find(c => c.id === id);
  if (campaign) {
    // Store campaign data to edit
    sessionStorage.setItem('campaignToEdit', JSON.stringify(campaign));
    router.push(`/secondary-dashboard/create-campaign?edit=${id}`);
  }
};

// Delete campaign
const deleteCampaign = async (id) => {
  if (confirm('Are you sure you want to delete this campaign? This action cannot be undone.')) {
    try {
      await api.delete(`/secondary/campaigns/${id}`);
      alert('Campaign deleted successfully!');
      // Refresh campaigns list
      await fetchCampaigns();
    } catch (error) {
      console.error('Error deleting campaign:', error);
      alert(error.response?.data?.error || 'Failed to delete campaign. Please try again.');
    }
  }
};

// Refresh campaigns when page becomes visible (e.g., after creating/updating)
const handleVisibilityChange = () => {
  if (document.visibilityState === 'visible') {
    fetchCampaigns();
  }
};

onMounted(() => {
  fetchCampaigns();
  // Listen for visibility changes to refresh when returning from create/edit page
  document.addEventListener('visibilitychange', handleVisibilityChange);
  // Also refresh when window regains focus
  window.addEventListener('focus', fetchCampaigns);
});

onBeforeUnmount(() => {
  document.removeEventListener('visibilitychange', handleVisibilityChange);
  window.removeEventListener('focus', fetchCampaigns);
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

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
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

/* Animation for cards */
.campaign-card {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
