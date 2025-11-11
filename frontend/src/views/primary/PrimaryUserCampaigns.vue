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

    <!-- Campaign Details Modal -->
    <div 
      class="modal fade" 
      :class="{ 'show': showModal }" 
      :style="{ display: showModal ? 'block' : 'none' }" 
      tabindex="-1" 
      role="dialog"
      @click.self="closeModal"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document" @click.stop>
        <div class="modal-content">
          <div class="modal-header border-0 pb-2">
            <h5 class="modal-title fw-bold">Campaign Details</h5>
            <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="selectedCampaign">
            <!-- Campaign Image -->
            <div class="position-relative mb-4 rounded overflow-hidden" style="height: 250px;">
              <img 
                :src="selectedCampaign.image" 
                class="w-100 h-100" 
                :alt="selectedCampaign.title"
                style="object-fit: cover;"
              >
              <span class="badge position-absolute top-0 end-0 m-3" :class="getStatusBadgeClass(selectedCampaign.status)">
                {{ formatStatus(selectedCampaign.status) }}
              </span>
            </div>

            <!-- Campaign Title and Basic Info -->
            <div class="mb-4">
              <h3 class="mb-3 fw-bold">{{ selectedCampaign.title }}</h3>
              <div class="d-flex flex-wrap gap-2 mb-3">
                <span class="badge" :class="getCategoryBadgeClass(selectedCampaign.category)">
                  {{ selectedCampaign.category }}
                </span>
                <span class="badge bg-light text-dark">
                  <i class="bi bi-calendar-event me-1"></i>{{ formatDate(selectedCampaign.startDate) }}
                </span>
                <span v-if="selectedCampaign.location" class="badge bg-light text-dark">
                  <i class="bi bi-geo-alt me-1"></i>{{ selectedCampaign.location }}
                </span>
              </div>
            </div>

            <!-- Campaign Description -->
            <div class="mb-4">
              <h5 class="mb-3 fw-semibold">
                <i class="bi bi-info-circle me-2 text-primary"></i>About This Campaign
              </h5>
              <p class="text-muted" style="line-height: 1.8; font-size: 1rem;">
                {{ selectedCampaign.description || 'No description available' }}
              </p>
            </div>

            <!-- Venue Section -->
            <div v-if="selectedCampaign.location" class="mb-4">
              <div class="venue-card p-3 rounded border">
                <h5 class="mb-3 fw-semibold">
                  <i class="bi bi-geo-alt-fill me-2 text-danger"></i>Venue
                </h5>
                <p class="mb-0 fw-medium" style="font-size: 1.1rem; color: #2c3e50;">
                  <i class="bi bi-map me-2 text-primary"></i>{{ selectedCampaign.location }}
                </p>
                <p v-if="selectedCampaign.pincode" class="mt-2 mb-0 text-muted">
                  <i class="bi bi-pin-map me-1"></i>Pincode: {{ selectedCampaign.pincode }}
                </p>
              </div>
            </div>

            <!-- Campaign Details Grid -->
            <div class="row g-3 mb-4">
              <div class="col-md-6">
                <div class="detail-box p-3 rounded">
                  <h6 class="text-muted mb-2 fw-semibold">
                    <i class="bi bi-people me-2 text-primary"></i>Participants
                  </h6>
                  <h4 class="mb-0 fw-bold">{{ selectedCampaign.participants || 0 }}</h4>
                </div>
              </div>
              <div class="col-md-6">
                <div class="detail-box p-3 rounded">
                  <h6 class="text-muted mb-2 fw-semibold">
                    <i class="bi bi-target me-2 text-success"></i>Goal
                  </h6>
                  <h4 class="mb-0 fw-bold">{{ selectedCampaign.goal || 'N/A' }}</h4>
                </div>
              </div>
              <div class="col-md-6">
                <div class="detail-box p-3 rounded">
                  <h6 class="text-muted mb-2 fw-semibold">
                    <i class="bi bi-calendar-range me-2 text-warning"></i>Event Date
                  </h6>
                  <p class="mb-0">
                    {{ formatDate(selectedCampaign.startDate) }}
                    <span v-if="selectedCampaign.endDate && selectedCampaign.endDate !== selectedCampaign.startDate">
                      <br>to {{ formatDate(selectedCampaign.endDate) }}
                    </span>
                  </p>
                </div>
              </div>
              <div class="col-md-6">
                <div class="detail-box p-3 rounded">
                  <h6 class="text-muted mb-2 fw-semibold">
                    <i class="bi bi-clock me-2 text-info"></i>Event Time
                  </h6>
                  <p class="mb-0">{{ formatDateTime(selectedCampaign.event_datetime) }}</p>
                </div>
              </div>
            </div>

            <!-- Progress Bar (if applicable) -->
            <div v-if="selectedCampaign.goal && selectedCampaign.participants !== undefined" class="mb-4">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <h6 class="mb-0 fw-semibold">Campaign Progress</h6>
                <span class="text-muted">{{ progressPercentage }}%</span>
              </div>
              <div class="progress" style="height: 12px; border-radius: 10px;">
                <div 
                  class="progress-bar bg-success" 
                  role="progressbar" 
                  :style="{ width: progressPercentage + '%' }"
                  :aria-valuenow="progressPercentage" 
                  aria-valuemin="0" 
                  aria-valuemax="100"
                ></div>
              </div>
            </div>

            <!-- Event Date & Time Alert -->
            <div v-if="selectedCampaign.event_datetime" class="alert alert-info mb-0">
              <i class="bi bi-calendar-check me-2"></i>
              <strong>Event Date & Time:</strong> {{ formatDateTime(selectedCampaign.event_datetime) }}
            </div>
          </div>
          <div class="modal-footer border-0 pt-3">
            <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
            <button 
              v-if="selectedCampaign && !selectedCampaign.is_registered"
              type="button" 
              class="btn btn-primary"
              @click="registerFromModal"
              :disabled="isRegistering === selectedCampaign?.id"
            >
              <span v-if="isRegistering === selectedCampaign?.id" class="spinner-border spinner-border-sm me-2" role="status"></span>
              <i v-else class="bi bi-person-plus me-2"></i>
              {{ isRegistering === selectedCampaign?.id ? 'Registering...' : 'Register for Campaign' }}
            </button>
            <button 
              v-else-if="selectedCampaign && selectedCampaign.is_registered"
              type="button" 
              class="btn btn-success"
              disabled
            >
              <i class="bi bi-check-circle me-2"></i>Registered
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal Backdrop -->
    <div 
      v-if="showModal" 
      class="modal-backdrop fade show" 
      @click="closeModal"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import api from '../../services/api';

// Data
const campaigns = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const statusFilter = ref('');
const categoryFilter = ref('');
const isRegistering = ref(null);
const successMessage = ref('');
const errorMessage = ref('');
const showModal = ref(false);
const selectedCampaign = ref(null);

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
        pincode: campaign.pincode || null,
        participants: campaign.registration_count || 0,
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

// Format date and time for display
const formatDateTime = (dateTimeString) => {
  if (!dateTimeString) return 'TBD';
  const options = { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };
  return new Date(dateTimeString).toLocaleString(undefined, options);
};

// Computed property for progress percentage
const progressPercentage = computed(() => {
  if (!selectedCampaign.value || !selectedCampaign.value.goal || !selectedCampaign.value.participants) {
    return 0;
  }
  return Math.min(100, Math.round((selectedCampaign.value.participants / selectedCampaign.value.goal) * 100));
});

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
    
    const response = await api.post(`/primary/campaigns/${campaignId}/register`);
    const data = response.data;
    
    // Update the campaign's registered status and participant count
    const campaign = campaigns.value.find(c => c.id === campaignId);
    if (campaign) {
      campaign.is_registered = true;
      campaign.participants = (campaign.participants || 0) + 1;
    }
    
    // Show success message with points information
    if (data.points_awarded) {
      successMessage.value = `Successfully registered for the campaign! You earned +${data.points_awarded} points.`;
    } else {
      successMessage.value = 'Successfully registered for the campaign!';
    }
  } catch (error) {
    console.error('Error registering for campaign:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to register for campaign. Please try again.';
  } finally {
    isRegistering.value = null;
  }
};

// View campaign details - open modal
const viewCampaign = (id) => {
  const campaign = campaigns.value.find(c => c.id === id);
  if (campaign) {
    selectedCampaign.value = { ...campaign };
    showModal.value = true;
    // Prevent body scroll when modal is open
    document.body.style.overflow = 'hidden';
  }
};

// Close modal
const closeModal = () => {
  showModal.value = false;
  selectedCampaign.value = null;
  document.body.style.overflow = '';
};

// Register from modal
const registerFromModal = async () => {
  if (!selectedCampaign.value) return;
  
  try {
    isRegistering.value = selectedCampaign.value.id;
    errorMessage.value = '';
    successMessage.value = '';
    
    const response = await api.post(`/primary/campaigns/${selectedCampaign.value.id}/register`);
    const data = response.data;
    
    // Update the campaign's registered status in both modal and list
    selectedCampaign.value.is_registered = true;
    selectedCampaign.value.participants = (selectedCampaign.value.participants || 0) + 1;
    const campaign = campaigns.value.find(c => c.id === selectedCampaign.value.id);
    if (campaign) {
      campaign.is_registered = true;
      campaign.participants = (campaign.participants || 0) + 1;
    }
    
    // Show success message with points information
    if (data.points_awarded) {
      successMessage.value = `Successfully registered for the campaign! You earned +${data.points_awarded} points.`;
    } else {
      successMessage.value = 'Successfully registered for the campaign!';
    }
    // Close modal after a short delay
    setTimeout(() => {
      closeModal();
    }, 1500);
  } catch (error) {
    console.error('Error registering for campaign:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to register for campaign. Please try again.';
  } finally {
    isRegistering.value = null;
  }
};

// Reset all filters
const resetFilters = () => {
  searchQuery.value = '';
  statusFilter.value = '';
  categoryFilter.value = '';
};

// Handle Escape key to close modal
const handleEscapeKey = (event) => {
  if (event.key === 'Escape' && showModal.value) {
    closeModal();
  }
};

// Lifecycle hooks
onMounted(() => {
  fetchCampaigns();
  // Add event listener for Escape key
  document.addEventListener('keydown', handleEscapeKey);
});

// Cleanup: restore body scroll when component is unmounted
onBeforeUnmount(() => {
  document.body.style.overflow = '';
  document.removeEventListener('keydown', handleEscapeKey);
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

/* Modal Styles */
.modal {
  z-index: 1055;
}

.modal-backdrop {
  opacity: 0.5;
  z-index: 1050;
}

.modal-content {
  border: none;
  border-radius: 0.75rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.modal-header {
  border-bottom: 1px solid #e9ecef;
  padding: 1.5rem 1.5rem 1rem;
}

.modal-body {
  padding: 1.5rem;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}

.modal-footer {
  padding: 1rem 1.5rem 1.5rem;
  border-top: 1px solid #e9ecef;
}

.detail-box {
  background-color: #f8f9fa;
  border-left: 4px solid #4e73df;
  transition: transform 0.2s, box-shadow 0.2s;
}

.detail-box:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
}

.detail-box h6 {
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-box h4 {
  color: #2c3e50;
  font-size: 1.75rem;
}

/* Venue Card Styling */
.venue-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border: 2px solid #e9ecef !important;
  border-left: 4px solid #dc3545 !important;
  transition: all 0.3s ease;
}

.venue-card:hover {
  box-shadow: 0 0.5rem 1rem rgba(220, 53, 69, 0.15);
  transform: translateY(-2px);
  border-left-color: #c82333 !important;
}

.venue-card h5 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.venue-card p {
  line-height: 1.6;
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

  .modal-dialog {
    margin: 0.5rem;
    max-width: calc(100% - 1rem);
  }

  .modal-body {
    padding: 1rem;
    max-height: calc(100vh - 150px);
  }

  .modal-header,
  .modal-footer {
    padding: 1rem;
  }

  .detail-box h4 {
    font-size: 1.5rem;
  }

  .modal-body img {
    height: 200px !important;
  }

  .venue-card {
    padding: 1rem !important;
  }

  .venue-card h5 {
    font-size: 1rem;
    margin-bottom: 0.75rem;
  }

  .venue-card p {
    font-size: 0.95rem;
  }
}

/* Modal Animation */
.modal.fade.show .modal-dialog {
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
  transform: translateY(-50px);
}
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Custom scrollbar for the modal */
.modal-body::-webkit-scrollbar {
  width: 8px;
}

.modal-body::-webkit-scrollbar-track {
  background: #f8f9fa;
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb {
  background-color: #dee2e6;
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background-color: #adb5bd;
}

/* Progress bar styling */
.progress {
  background-color: #e9ecef;
  border-radius: 10px;
}

.progress-bar {
  border-radius: 10px;
  transition: width 0.3s ease;
}

/* Alert styling */
.alert {
  border: none;
  border-radius: 0.5rem;
}

/* Badge styling in modal */
.modal-body .badge {
  font-size: 0.875rem;
  padding: 0.5em 0.75em;
}
</style>
