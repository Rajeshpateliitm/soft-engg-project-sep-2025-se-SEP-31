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

    <!-- Campaigns Grid -->
    <div class="row g-4">
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
              {{ formatDate(campaign.startDate) }} - {{ formatDate(campaign.endDate) }}
            </p>
            <p class="card-text text-muted small mb-2">
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

    <!-- Empty State -->
    <div v-if="filteredCampaigns.length === 0" class="text-center py-5">
      <div class="mb-3">
        <i class="bi bi-calendar-x" style="font-size: 3rem; color: #6c757d;"></i>
      </div>
      <h5>No campaigns found</h5>
      <p class="text-muted">There are no campaigns matching your filters.</p>
      <button class="btn btn-outline-primary" @click="resetFilters">
        Clear Filters
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// Sample data - campaigns for secondary user (RWA)
const campaigns = ref([
  {
    id: 1,
    title: 'Plastic Free July Challenge',
    description: 'Join us in reducing single-use plastic waste throughout July. Track your plastic consumption and learn sustainable alternatives.',
    category: 'recycling',
    status: 'active',
    startDate: '2024-07-01',
    endDate: '2024-07-31',
    location: 'RWA Community Center',
    participants: 245,
    goal: 500,
    progress: 49,
    image: 'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80'
  },
  {
    id: 2,
    title: 'Community Cleanup Day',
    description: 'Help clean up our local park and learn about proper waste segregation. Gloves and bags will be provided.',
    category: 'cleanup',
    status: 'upcoming',
    startDate: '2024-08-15',
    endDate: '2024-08-15',
    location: 'Central Park',
    participants: 87,
    goal: 200,
    progress: 44,
    image: 'https://images.unsplash.com/photo-1605000797499-95a51c5269ae?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1471&q=80'
  },
  {
    id: 3,
    title: 'Composting Initiative',
    description: 'Learn how to turn your food scraps into nutrient-rich compost for your garden. Perfect for beginners!',
    category: 'composting',
    status: 'active',
    startDate: '2024-02-01',
    endDate: '2024-12-31',
    location: 'RWA Garden Area',
    participants: 200,
    goal: 300,
    progress: 67,
    image: 'https://images.unsplash.com/photo-1589924743088-6f0090d3ac1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80'
  },
  {
    id: 4,
    title: 'E-Waste Collection Drive',
    description: 'Safely dispose of your old electronics. We accept computers, phones, and other electronic waste.',
    category: 'recycling',
    status: 'completed',
    startDate: '2024-06-10',
    endDate: '2024-06-12',
    location: 'RWA Main Gate',
    participants: 312,
    goal: 300,
    progress: 100,
    image: 'https://images.unsplash.com/photo-1603732551681-2e91159b9dc2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80'
  },
  {
    id: 5,
    title: 'Zero Waste Living Seminar',
    description: 'Learn practical tips for reducing waste in your daily life from sustainability experts.',
    category: 'education',
    status: 'active',
    startDate: '2024-07-15',
    endDate: '2024-12-31',
    location: 'Community Hall',
    participants: 178,
    goal: 500,
    progress: 36,
    image: 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1373&q=80'
  },
  {
    id: 6,
    title: 'Tree Plantation Drive',
    description: 'Plant trees to offset carbon footprint and create a greener community environment.',
    category: 'education',
    status: 'upcoming',
    startDate: '2024-09-05',
    endDate: '2024-09-05',
    location: 'RWA Green Space',
    participants: 94,
    goal: 150,
    progress: 63,
    image: 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1471&q=80'
  }
]);

const searchQuery = ref('');
const statusFilter = ref('');
const categoryFilter = ref('');

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

// View campaign details
const viewCampaign = (id) => {
  router.push(`/campaigns/${id}`);
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
const updateCampaign = (id) => {
  const campaign = campaigns.value.find(c => c.id === id);
  if (campaign) {
    // Store campaign data in session/local storage or pass via router params
    sessionStorage.setItem('campaignToEdit', JSON.stringify(campaign));
    router.push(`/secondary-dashboard/create-campaign?edit=${id}`);
  }
};

// Delete campaign
const deleteCampaign = (id) => {
  if (confirm('Are you sure you want to delete this campaign? This action cannot be undone.')) {
    const index = campaigns.value.findIndex(c => c.id === id);
    if (index > -1) {
      campaigns.value.splice(index, 1);
      alert('Campaign deleted successfully!');
    }
  }
};
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
