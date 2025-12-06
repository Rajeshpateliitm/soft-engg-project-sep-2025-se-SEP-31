<template>
  <div class="create-campaign-container">
    <div class="container">
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex align-items-center mb-3">
            <button class="btn btn-link text-white p-0 me-2" @click="goBack">
              <i class="bi bi-arrow-left" style="font-size: 1.5rem;"></i>
            </button>
            <h2 class="text-white fw-bold mb-0">{{ isEditMode ? 'EDIT CAMPAIGN' : 'CREATE CAMPAIGN' }}</h2>
          </div>
          <p class="text-white-50">{{ isEditMode ? 'Update your waste management campaign' : 'Create a new waste management campaign for your RWA community' }}</p>
        </div>
      </div>

      <!-- Create Campaign Form -->
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="card shadow-lg">
            <div class="card-body p-4">
              <form @submit.prevent="submitForm">
                <!-- Campaign Image -->
                <div class="mb-4">
                  <label class="form-label fw-bold">Campaign Image</label>
                  <div class="image-upload-area">
                    <div v-if="formData.imagePreview" class="image-preview">
                      <img :src="formData.imagePreview" :alt="formData.campaignName" class="img-fluid">
                      <button type="button" class="btn btn-sm btn-danger position-absolute top-0 end-0 m-2" @click="removeImage">
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                    <div v-else class="upload-placeholder">
                      <input 
                        type="file" 
                        class="form-control" 
                        accept="image/*"
                        @change="handleImageUpload"
                        ref="imageInput"
                      >
                      <small class="text-muted d-block mt-2">Or paste image URL below</small>
                    </div>
                  </div>
                  <input 
                    type="url" 
                    class="form-control mt-2" 
                    placeholder="Image URL (e.g., https://example.com/image.jpg)"
                    v-model="formData.imageUrl"
                    @change="updateImagePreview"
                  >
                </div>

                <!-- Campaign Name -->
                <div class="mb-4">
                  <label class="form-label fw-bold">Campaign Name</label>
                  <input 
                    type="text" 
                    class="form-control form-control-lg" 
                    placeholder="Enter campaign name"
                    v-model="formData.campaignName"
                    required
                  >
                  <small class="text-muted">Give your campaign a clear, descriptive name</small>
                </div>

                <!-- Campaign Details -->
                <div class="mb-4">
                  <label class="form-label fw-bold">Campaign Details</label>
                  <textarea 
                    class="form-control" 
                    rows="4" 
                    placeholder="Describe your campaign objectives, activities, and expected outcomes..."
                    v-model="formData.campaignDetails"
                    required
                  ></textarea>
                  <small class="text-muted">Provide comprehensive details about the campaign</small>
                </div>

                <!-- Campaign Location -->
                <div class="mb-4">
                  <label class="form-label fw-bold">Campaign Location</label>
                  <input 
                    type="text" 
                    class="form-control form-control-lg" 
                    placeholder="Enter location (e.g., RWA Community Center, Park, etc.)"
                    v-model="formData.campaignLocation"
                    required
                  >
                  <small class="text-muted">Specify where the campaign will take place</small>
                </div>

                <!-- Campaign Date and Time -->
                <div class="row">
                  <div class="col-md-6 mb-4">
                    <label class="form-label fw-bold">Event Date</label>
                    <input 
                      type="date" 
                      class="form-control form-control-lg"
                      v-model="formData.startDate"
                      :min="minDate"
                      required
                    >
                    <small class="text-muted">Only current and future dates are allowed</small>
                  </div>
                  <div class="col-md-6 mb-4">
                    <label class="form-label fw-bold">Event Time</label>
                    <input 
                      type="time" 
                      class="form-control form-control-lg"
                      v-model="formData.startTime"
                      required
                    >
                  </div>
                </div>

                <!-- Additional Fields -->
                <div class="row">
                  <div class="col-md-6 mb-4">
                    <label class="form-label fw-bold">Category <span class="text-muted">(Optional - auto-detected)</span></label>
                    <select class="form-select form-select-lg" v-model="formData.category">
                      <option value="">Auto-detect from description</option>
                      <option value="recycling">Recycling</option>
                      <option value="composting">Composting</option>
                      <option value="cleanup">Cleanup</option>
                      <option value="education">Education</option>
                      <option value="other">Other</option>
                    </select>
                    <small class="text-muted">Category helps organize campaigns. It will be auto-detected from your description if not specified.</small>
                  </div>
                  <div class="col-md-6 mb-4">
                    <label class="form-label fw-bold">Pincode <span class="text-muted">(Optional)</span></label>
                    <input 
                      type="text" 
                      class="form-control form-control-lg"
                      placeholder="Campaign area pincode"
                      v-model="formData.pincode"
                      maxlength="12"
                    >
                    <small class="text-muted">Leave empty to use your RWA's pincode</small>
                  </div>
                </div>

                <!-- Form Actions -->
                <div class="d-flex gap-2 justify-content-end mt-5">
                  <button type="button" class="btn btn-outline-secondary btn-lg" @click="goBack">
                    Cancel
                  </button>
                  <button type="submit" class="btn btn-primary btn-lg" :disabled="isSubmitting">
                    <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status"></span>
                    <i v-else class="bi bi-check-lg me-2"></i>
                    {{ isSubmitting ? (isEditMode ? 'Updating...' : 'Creating...') : (isEditMode ? 'Update' : 'Create') }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '@/services/api';

const router = useRouter();
const route = useRoute();
const imageInput = ref(null);
const isSubmitting = ref(false);
const isEditMode = ref(false);
const campaignId = ref(null);

// Compute minimum date (today) for date input
const minDate = computed(() => {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const day = String(today.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
});

const formData = ref({
  campaignName: '',
  campaignDetails: '',
  campaignLocation: '',
  startDate: '',
  startTime: '',
  category: '',
  pincode: '',
  imageUrl: '',
  imagePreview: ''
});

// Check if we're in edit mode
onMounted(() => {
  const editId = route.query.edit;
  if (editId) {
    isEditMode.value = true;
    campaignId.value = parseInt(editId);
    loadCampaignForEdit();
  }
});

// Load campaign data for editing
const loadCampaignForEdit = () => {
  const campaignData = sessionStorage.getItem('campaignToEdit');
  if (campaignData) {
    try {
      const campaign = JSON.parse(campaignData);
      formData.value.campaignName = campaign.title || '';
      formData.value.campaignDetails = campaign.description || '';
      formData.value.campaignLocation = campaign.location || '';
      
      if (campaign.event_datetime) {
        const eventDate = new Date(campaign.event_datetime);
        formData.value.startDate = eventDate.toISOString().split('T')[0];
        formData.value.startTime = eventDate.toTimeString().slice(0, 5);
      }
      
      formData.value.category = campaign.category || '';
      formData.value.pincode = campaign.pincode || '';
      formData.value.imageUrl = campaign.image || '';
      formData.value.imagePreview = campaign.image || '';
    } catch (error) {
      console.error('Error loading campaign data:', error);
    }
  }
};

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      formData.value.imagePreview = e.target.result;
      formData.value.imageUrl = e.target.result; // Use base64 or URL
    };
    reader.readAsDataURL(file);
  }
};

const updateImagePreview = () => {
  if (formData.value.imageUrl) {
    formData.value.imagePreview = formData.value.imageUrl;
  }
};

const removeImage = () => {
  formData.value.imagePreview = '';
  formData.value.imageUrl = '';
  if (imageInput.value) {
    imageInput.value.value = '';
  }
};

const submitForm = async () => {
  // Validate form - only check required fields
  if (!formData.value.campaignName || !formData.value.campaignDetails || 
      !formData.value.campaignLocation || !formData.value.startDate || 
      !formData.value.startTime) {
    alert('Please fill in all required fields (Name, Description, Location, Date, and Time)');
    return;
  }

  // Validate that the date is not in the past
  const selectedDate = new Date(formData.value.startDate);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  selectedDate.setHours(0, 0, 0, 0);
  
  if (selectedDate < today) {
    alert('Event date cannot be in the past. Please select a current or future date.');
    return;
  }

  // Validate that the combined date and time is not in the past
  const eventDateTimeStr = `${formData.value.startDate} ${formData.value.startTime}`;
  const eventDateTime = new Date(eventDateTimeStr);
  const now = new Date();
  
  if (eventDateTime < now) {
    alert('Event date and time cannot be in the past. Please select a current or future date and time.');
    return;
  }

  try {
    isSubmitting.value = true;
    
    // Combine date and time into format: "YYYY-MM-DD HH:MM"
    const eventDateTime = `${formData.value.startDate} ${formData.value.startTime}`;
    
    const campaignData = {
      name: formData.value.campaignName,
      description: formData.value.campaignDetails,
      location: formData.value.campaignLocation,
      event_datetime: eventDateTime,
      image_url: formData.value.imageUrl || null,
      pincode: formData.value.pincode || null
    };
    
    if (isEditMode.value && campaignId.value) {
      // Update existing campaign
      await api.put(`/secondary/campaigns/${campaignId.value}`, campaignData);
      alert('Campaign updated successfully!');
    } else {
      // Create new campaign
      await api.post('/secondary/campaigns/create', campaignData);
      alert('Campaign created successfully!');
    }
    
    // Clear session storage
    sessionStorage.removeItem('campaignToEdit');
    
    // Redirect to campaigns page
    router.push('/secondary-dashboard/campaigns');
  } catch (error) {
    console.error('Error saving campaign:', error);
    alert(error.response?.data?.error || 'Failed to save campaign. Please try again.');
  } finally {
    isSubmitting.value = false;
  }
};

const goBack = () => {
  sessionStorage.removeItem('campaignToEdit');
  router.push('/secondary-dashboard/campaigns');
};
</script>

<style scoped>
.create-campaign-container {
  padding: 1.5rem;
  min-height: 100vh;
}

.card {
  border: none;
  border-radius: 0.75rem;
  background: #ffffff;
}

.form-label {
  color: #2c3e50;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.form-control,
.form-select {
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-control:focus,
.form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.form-control-lg,
.form-select-lg {
  padding: 0.875rem 1rem;
  font-size: 1.1rem;
}

.image-upload-area {
  border: 2px dashed #dee2e6;
  border-radius: 0.5rem;
  padding: 2rem;
  text-align: center;
  background: #f8f9fa;
  transition: border-color 0.3s;
}

.image-upload-area:hover {
  border-color: #0d6efd;
}

.image-preview {
  position: relative;
  display: inline-block;
  max-width: 100%;
}

.image-preview img {
  max-height: 300px;
  border-radius: 0.5rem;
}

.upload-placeholder {
  padding: 1rem;
}

.upload-placeholder .form-control {
  cursor: pointer;
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
  padding: 0.75rem 2rem;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(13, 110, 253, 0.3);
}

.btn-outline-secondary {
  padding: 0.75rem 2rem;
  font-weight: 600;
}

.btn-lg {
  padding: 0.875rem 2rem;
  font-size: 1.1rem;
}

small {
  display: block;
  margin-top: 0.25rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .create-campaign-container {
    padding: 1rem;
  }

  .card-body {
    padding: 1.5rem !important;
  }

  .form-label {
    font-size: 0.95rem;
  }

  .btn-lg {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
  }
}
</style>
