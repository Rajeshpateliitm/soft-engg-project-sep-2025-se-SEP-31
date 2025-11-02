<template>
  <div class="campaigns-container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Waste Management Campaigns</h2>
      <button class="btn btn-primary" @click="showCreateModal = true">
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

    <!-- Create Campaign Modal -->
    <div class="modal fade" :class="{ 'show d-block': showCreateModal }" tabindex="-1" v-if="showCreateModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create New Campaign</h5>
            <button type="button" class="btn-close" @click="showCreateModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="createCampaign">
              <div class="mb-3">
                <label class="form-label">Campaign Title</label>
                <input type="text" class="form-control" v-model="newCampaign.title" required>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Start Date</label>
                  <input type="date" class="form-control" v-model="newCampaign.startDate" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">End Date</label>
                  <input type="date" class="form-control" v-model="newCampaign.endDate" required>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" rows="3" v-model="newCampaign.description" required></textarea>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Category</label>
                  <select class="form-select" v-model="newCampaign.category" required>
                    <option value="recycling">Recycling</option>
                    <option value="composting">Composting</option>
                    <option value="cleanup">Cleanup</option>
                    <option value="education">Education</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Goal (participants)</label>
                  <input type="number" class="form-control" v-model.number="newCampaign.goal" min="1" required>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Cover Image URL</label>
                <input type="url" class="form-control" v-model="newCampaign.image" placeholder="https://example.com/image.jpg">
              </div>
              <div class="d-flex justify-content-end gap-2">
                <button type="button" class="btn btn-outline-secondary" @click="showCreateModal = false">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary">
                  Create Campaign
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="showCreateModal"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// Sample data - in a real app, this would come from an API
const campaigns = ref([
  {
    id: 1,
    title: 'Plastic Free July Challenge',
    description: 'Join us in reducing single-use plastic waste throughout July. Track your plastic consumption and learn sustainable alternatives.',
    category: 'recycling',
    status: 'active',
    startDate: '2023-07-01',
    endDate: '2023-07-31',
    participants: 245,
    goal: 500,
    image: 'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80'
  },
  {
    id: 2,
    title: 'Community Cleanup Day',
    description: 'Help clean up our local park and learn about proper waste segregation. Gloves and bags will be provided.',
    category: 'cleanup',
    status: 'upcoming',
    startDate: '2023-08-15',
    endDate: '2023-08-15',
    participants: 87,
    goal: 200,
    image: 'https://images.unsplash.com/photo-1605000797499-95a51c5269ae?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1471&q=80'
  },
  {
    id: 3,
    title: 'Composting Workshop',
    description: 'Learn how to turn your food scraps into nutrient-rich compost for your garden. Perfect for beginners!',
    category: 'composting',
    status: 'upcoming',
    startDate: '2023-08-22',
    endDate: '2023-08-22',
    participants: 32,
    goal: 50,
    image: 'https://images.unsplash.com/photo-1589924743088-6f0090d3ac1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80'
  },
  {
    id: 4,
    title: 'E-Waste Collection Drive',
    description: 'Safely dispose of your old electronics. We accept computers, phones, and other electronic waste.',
    category: 'recycling',
    status: 'completed',
    startDate: '2023-06-10',
    endDate: '2023-06-12',
    participants: 312,
    goal: 300,
    image: 'https://images.unsplash.com/photo-1603732551681-2e91159b9dc2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80'
  },
  {
    id: 5,
    title: 'Zero Waste Living Seminar',
    description: 'Learn practical tips for reducing waste in your daily life from sustainability experts.',
    category: 'education',
    status: 'active',
    startDate: '2023-07-15',
    endDate: '2023-12-31',
    participants: 178,
    goal: 500,
    image: 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1373&q=80'
  },
  {
    id: 6,
    title: 'Clothing Swap Event',
    description: 'Bring clothes you no longer wear and exchange them for something new-to-you. Leftover items will be donated.',
    category: 'recycling',
    status: 'upcoming',
    startDate: '2023-09-05',
    endDate: '2023-09-05',
    participants: 94,
    goal: 150,
    image: 'https://images.unsplash.com/photo 1467043237213-65f2f417abf2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80'
  }
]);

const showCreateModal = ref(false);
const searchQuery = ref('');
const statusFilter = ref('');
const categoryFilter = ref('');

const newCampaign = ref({
  title: '',
  description: '',
  category: 'recycling',
  startDate: new Date().toISOString().split('T')[0],
  endDate: '',
  goal: 100,
  image: 'https://images.unsplash.com/photo-1466611653911-95081537e5b7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80'
});

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

// Create new campaign
const createCampaign = () => {
  const newId = Math.max(...campaigns.value.map(c => c.id)) + 1;
  
  campaigns.value.unshift({
    id: newId,
    status: 'upcoming',
    participants: 0,
    ...newCampaign.value
  });
  
  // Reset form
  newCampaign.value = {
    title: '',
    description: '',
    category: 'recycling',
    startDate: new Date().toISOString().split('T')[0],
    endDate: '',
    goal: 100,
    image: 'https://images.unsplash.com/photo-1466611653911-95081537e5b7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80'
  };
  
  showCreateModal.value = false;
};

// Reset all filters
const resetFilters = () => {
  searchQuery.value = '';
  statusFilter.value = '';
  categoryFilter.value = '';
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
