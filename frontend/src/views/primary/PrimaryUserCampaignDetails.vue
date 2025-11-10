<template>
  <div class="campaign-details">
    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Loading campaign details...</p>
    </div>

    <!-- Campaign Details Content -->
    <template v-else-if="campaign">
      <!-- Back Button -->
      <div class="mb-4">
        <router-link to="/primary-dashboard/campaigns" class="btn btn-outline-secondary">
          <i class="bi bi-arrow-left me-2"></i>Back to Campaigns
        </router-link>
      </div>

      <!-- Campaign Header -->
      <div class="row mb-4">
        <div class="col-lg-8">
          <div class="card border-0 shadow-sm overflow-hidden">
            <!-- Campaign Image -->
            <div class="position-relative">
              <img 
                :src="campaign.image" 
                class="card-img-top" 
                :alt="campaign.title"
                style="height: 400px; object-fit: cover;"
              >
              <span class="badge position-absolute top-0 end-0 m-3" :class="getStatusBadgeClass(campaign.status)">
                {{ formatStatus(campaign.status) }}
              </span>
            </div>

            <!-- Campaign Title and Basic Info -->
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <h2 class="card-title mb-2">{{ campaign.title }}</h2>
                  <div class="d-flex gap-2 flex-wrap">
                    <span class="badge" :class="getCategoryBadgeClass(campaign.category)">
                      {{ campaign.category }}
                    </span>
                    <span class="badge bg-light text-dark">
                      <i class="bi bi-calendar-event me-1"></i>{{ formatDate(campaign.startDate) }}
                    </span>
                    <span v-if="campaign.location" class="badge bg-light text-dark">
                      <i class="bi bi-geo-alt me-1"></i>{{ campaign.location }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Campaign Description -->
              <div class="mb-4">
                <h5 class="mb-3">About This Campaign</h5>
                <p class="text-muted" style="line-height: 1.8;">
                  {{ campaign.description || 'No description available' }}
                </p>
              </div>

              <!-- Campaign Details Grid -->
              <div class="row g-3 mb-4">
                <div class="col-md-6">
                  <div class="detail-box">
                    <h6 class="text-muted mb-2">
                      <i class="bi bi-people me-2 text-primary"></i>Participants
                    </h6>
                    <h4 class="mb-0">{{ campaign.participants || 0 }}</h4>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="detail-box">
                    <h6 class="text-muted mb-2">
                      <i class="bi bi-target me-2 text-success"></i>Goal
                    </h6>
                    <h4 class="mb-0">{{ campaign.goal || 'N/A' }}</h4>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="detail-box">
                    <h6 class="text-muted mb-2">
                      <i class="bi bi-calendar-range me-2 text-warning"></i>Duration
                    </h6>
                    <p class="mb-0">
                      {{ formatDate(campaign.startDate) }}
                      <span v-if="campaign.endDate"> to {{ formatDate(campaign.endDate) }}</span>
                    </p>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="detail-box">
                    <h6 class="text-muted mb-2">
                      <i class="bi bi-info-circle me-2 text-info"></i>Status
                    </h6>
                    <p class="mb-0">{{ formatStatus(campaign.status) }}</p>
                  </div>
                </div>
              </div>

              <!-- Progress Bar (if applicable) -->
              <div v-if="campaign.goal && campaign.participants" class="mb-4">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <h6 class="mb-0">Campaign Progress</h6>
                  <span class="text-muted">{{ progressPercentage }}%</span>
                </div>
                <div class="progress" style="height: 10px;">
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

              <!-- Additional Details -->
              <div v-if="campaign.event_datetime" class="alert alert-info mb-0">
                <i class="bi bi-calendar-check me-2"></i>
                <strong>Event Date & Time:</strong> {{ formatDateTime(campaign.event_datetime) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="col-lg-4">
          <!-- Registration Card -->
          <div class="card border-0 shadow-sm mb-4">
            <div class="card-body">
              <h5 class="card-title mb-3">Campaign Registration</h5>
              <div v-if="!campaign.is_registered" class="d-grid gap-2">
                <button 
                  class="btn btn-primary btn-lg"
                  @click="registerCampaign"
                  :disabled="isRegistering"
                >
                  <span v-if="isRegistering" class="spinner-border spinner-border-sm me-2" role="status"></span>
                  <i v-else class="bi bi-person-plus me-2"></i>
                  {{ isRegistering ? 'Registering...' : 'Register for Campaign' }}
                </button>
                <small class="text-muted text-center">
                  Join this campaign to participate and earn points
                </small>
              </div>
              <div v-else class="text-center">
                <div class="alert alert-success mb-0">
                  <i class="bi bi-check-circle me-2"></i>
                  <strong>You are registered!</strong>
                  <p class="mb-0 mt-2 small">Thank you for joining this campaign.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Campaign Info Card -->
          <div class="card border-0 shadow-sm">
            <div class="card-body">
              <h5 class="card-title mb-3">Campaign Information</h5>
              <div class="info-item mb-3">
                <h6 class="text-muted mb-1">Category</h6>
                <p class="mb-0">
                  <span class="badge" :class="getCategoryBadgeClass(campaign.category)">
                    {{ campaign.category }}
                  </span>
                </p>
              </div>
              <div class="info-item mb-3">
                <h6 class="text-muted mb-1">Status</h6>
                <p class="mb-0">
                  <span class="badge" :class="getStatusBadgeClass(campaign.status)">
                    {{ formatStatus(campaign.status) }}
                  </span>
                </p>
              </div>
              <div v-if="campaign.location" class="info-item">
                <h6 class="text-muted mb-1">Location</h6>
                <p class="mb-0">
                  <i class="bi bi-geo-alt me-1"></i>{{ campaign.location }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Success/Error Messages -->
      <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
        <i class="bi bi-check-circle me-2"></i>{{ successMessage }}
        <button type="button" class="btn-close" @click="successMessage = ''"></button>
      </div>
      <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
        <i class="bi bi-exclamation-circle me-2"></i>{{ errorMessage }}
        <button type="button" class="btn-close" @click="errorMessage = ''"></button>
      </div>
    </template>

    <!-- Campaign Not Found -->
    <div v-else class="text-center py-5">
      <div class="mb-3">
        <i class="bi bi-calendar-x" style="font-size: 3rem; color: #6c757d;"></i>
      </div>
      <h5>Campaign Not Found</h5>
      <p class="text-muted">The campaign you're looking for doesn't exist or has been removed.</p>
      <router-link to="/primary-dashboard/campaigns" class="btn btn-outline-primary">
        Back to Campaigns
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../../services/api';

const route = useRoute();
const router = useRouter();

// Data
const campaign = ref(null);
const isLoading = ref(true);
const isRegistering = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

// Default image for campaigns without image_url
const defaultImage = 'https://images.unsplash.com/photo-1466611653911-95081537e5b7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80';

// Computed property for progress percentage
const progressPercentage = computed(() => {
  if (!campaign.value || !campaign.value.goal || !campaign.value.participants) {
    return 0;
  }
  return Math.min(100, Math.round((campaign.value.participants / campaign.value.goal) * 100));
});

// Fetch campaign details
const fetchCampaignDetails = async () => {
  try {
    isLoading.value = true;
    const campaignId = route.params.id;
    
    const response = await api.get(`/primary/campaigns/${campaignId}`);
    const data = response.data;
    
    // Transform backend data to frontend format
    const campaignData = data.campaign || data;
    const eventDate = campaignData.event_datetime ? new Date(campaignData.event_datetime) : null;
    const now = new Date();
    
    // Determine status based on event_datetime
    let status = 'upcoming';
    if (eventDate) {
      if (eventDate < now) {
        status = 'completed';
      } else if (eventDate <= new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)) {
        status = 'active';
      }
    }
    
    // Derive category from description
    let category = 'education';
    const desc = (campaignData.description || '').toLowerCase();
    if (desc.includes('recycl') || desc.includes('plastic') || desc.includes('e-waste')) {
      category = 'recycling';
    } else if (desc.includes('compost')) {
      category = 'composting';
    } else if (desc.includes('cleanup') || desc.includes('clean up')) {
      category = 'cleanup';
    } else if (desc.includes('workshop') || desc.includes('seminar') || desc.includes('learn')) {
      category = 'education';
    }
    
    campaign.value = {
      id: campaignData.id,
      title: campaignData.name,
      description: campaignData.description || '',
      category: category,
      status: status,
      startDate: eventDate ? eventDate.toISOString().split('T')[0] : null,
      endDate: eventDate ? eventDate.toISOString().split('T')[0] : null,
      event_datetime: campaignData.event_datetime,
      location: campaignData.location,
      participants: campaignData.participants || 0,
      goal: campaignData.goal || 100,
      image: campaignData.image_url || defaultImage,
      is_registered: campaignData.is_registered || false
    };
  } catch (error) {
    console.error('Error fetching campaign details:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to load campaign details. Please try again.';
    campaign.value = null;
  } finally {
    isLoading.value = false;
  }
};

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

// Register for campaign
const registerCampaign = async () => {
  try {
    isRegistering.value = true;
    errorMessage.value = '';
    successMessage.value = '';
    
    await api.post(`/primary/campaigns/${campaign.value.id}/register`);
    
    campaign.value.is_registered = true;
    successMessage.value = 'Successfully registered for the campaign!';
  } catch (error) {
    console.error('Error registering for campaign:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to register for campaign. Please try again.';
  } finally {
    isRegistering.value = false;
  }
};

// Lifecycle hook
onMounted(() => {
  fetchCampaignDetails();
});
</script>

<style scoped>
.campaign-details {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

.card {
  border: none;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
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

.detail-box {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  border-left: 4px solid #4e73df;
}

.detail-box h6 {
  font-weight: 600;
  font-size: 0.875rem;
}

.detail-box h4 {
  font-weight: 700;
  color: #2c3e50;
}

.info-item {
  padding-bottom: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.info-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.info-item h6 {
  font-weight: 600;
  font-size: 0.875rem;
}

.progress {
  border-radius: 10px;
  background-color: #e9ecef;
}

.progress-bar {
  border-radius: 10px;
  transition: width 0.3s ease;
}

.btn-lg {
  padding: 0.75rem 1.5rem;
  font-weight: 500;
}

.alert {
  border: none;
  border-radius: 0.5rem;
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .campaign-details {
    padding: 1rem;
  }
  
  .card-img-top {
    height: 300px !important;
  }
}

@media (max-width: 768px) {
  .campaign-details {
    padding: 0.5rem;
  }
  
  .card-img-top {
    height: 250px !important;
  }
  
  .card-title {
    font-size: 1.5rem;
  }
  
  .detail-box {
    padding: 0.75rem;
  }
}

/* Animation for badges */
.badge {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
