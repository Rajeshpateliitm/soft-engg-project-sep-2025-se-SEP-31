<template>
  <div class="recycler-container">
    <!-- Find Local Recyclers Section -->
    <div class="card shadow-sm mb-4">
      <div class="card-header bg-info text-white">
        <h3 class="card-title mb-0">Find Local Recyclers</h3>
      </div>
      <div class="card-body">
        <div class="search-section">
          <div class="row g-3 align-items-end">
            <div class="col-md-8">
              <label for="pincode" class="form-label fw-semibold">Enter Pincode</label>
              <input 
                type="text" 
                class="form-control form-control-lg" 
                id="pincode" 
                v-model="searchPincode"
                placeholder="Enter PINCODE...."
                @keyup.enter="searchRecyclers"
              >
            </div>
            <div class="col-md-4">
              <button 
                class="btn btn-danger btn-lg w-100 fw-semibold" 
                @click="searchRecyclers"
                :disabled="!searchPincode.trim()"
              >
                SEARCH
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Results Section -->
    <div v-if="searchPerformed" class="results-section">
      <h4 class="mb-4 fw-bold">Recyclers Near to Your Location</h4>
      
      <div class="row">
        <!-- Recycler Cards Column -->
        <div class="col-lg-6">
          <div v-if="filteredRecyclers.length === 0" class="alert alert-info" role="alert">
            <i class="bi bi-info-circle me-2"></i>
            No recyclers found for pincode {{ searchPincode }}. Please try another pincode.
          </div>
          
          <div v-else class="recycler-cards">
            <div 
              v-for="recycler in filteredRecyclers" 
              :key="recycler.id"
              class="card recycler-card mb-3 shadow-sm"
            >
              <div class="card-body">
                <h5 class="card-title text-primary fw-bold">{{ recycler.name }}</h5>
                <p class="card-text text-muted mb-2">
                  <i class="bi bi-geo-alt me-2"></i>{{ recycler.address }}
                </p>
                <p class="card-text text-muted mb-2">
                  <i class="bi bi-pin-map me-2"></i>{{ recycler.city }}, {{ recycler.state }} - {{ recycler.pincode }}
                </p>
                <p class="card-text mb-3">
                  <small class="text-secondary">{{ recycler.description }}</small>
                </p>
                
                <div class="button-group d-flex gap-2 flex-wrap">
                  <button 
                    class="btn btn-sm btn-outline-primary fw-semibold"
                    @click="showContactInfo(recycler)"
                  >
                    <i class="bi bi-telephone me-1"></i>CONTACTS
                  </button>
                  <button 
                    class="btn btn-sm btn-outline-success fw-semibold"
                    @click="showWebsite(recycler)"
                  >
                    <i class="bi bi-globe me-1"></i>WEBSITE
                  </button>
                  <button 
                    class="btn btn-sm btn-outline-info fw-semibold"
                    @click="showMapDirection(recycler)"
                  >
                    <i class="bi bi-map me-1"></i>MAP DIRECTION
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Map Section -->
        <div class="col-lg-6">
          <div class="map-container">
            <div class="map-header mb-3">
              <h5 class="fw-bold">Recycler Locations near {{ searchPincode }}</h5>
            </div>
            <div class="map-image-wrapper">
              <img 
                src="@/assets/map-placeholder.svg" 
                alt="Map showing recycler locations" 
                class="map-image"
                @error="handleMapImageError"
              >
              <!-- Fallback map display -->
              <div v-if="mapImageError" class="map-fallback">
                <div class="map-placeholder">
                  <i class="bi bi-map"></i>
                  <p>Map showing recycler locations near {{ searchPincode }}</p>
                  <div class="recycler-markers">
                    <div 
                      v-for="(recycler, index) in filteredRecyclers" 
                      :key="recycler.id"
                      class="marker"
                    >
                      <span class="marker-number">{{ index + 1 }}</span>
                      <span class="marker-name">{{ recycler.name }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Contact Modal -->
    <div 
      v-if="showContactModal" 
      class="modal-overlay"
      @click.self="showContactModal = false"
    >
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Contact Information</h5>
          <button 
            type="button" 
            class="btn-close" 
            @click="showContactModal = false"
          ></button>
        </div>
        <div class="modal-body">
          <div v-if="selectedRecycler">
            <h6 class="fw-bold mb-3">{{ selectedRecycler.name }}</h6>
            <p class="mb-2">
              <strong>Phone:</strong> 
              <a :href="`tel:${selectedRecycler.phone}`" class="text-decoration-none">
                {{ selectedRecycler.phone }}
              </a>
            </p>
            <p class="mb-2">
              <strong>Email:</strong> 
              <a :href="`mailto:${selectedRecycler.email}`" class="text-decoration-none">
                {{ selectedRecycler.email }}
              </a>
            </p>
            <p class="mb-0">
              <strong>Address:</strong> {{ selectedRecycler.address }}, {{ selectedRecycler.city }}, {{ selectedRecycler.state }} - {{ selectedRecycler.pincode }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Website Modal -->
    <div 
      v-if="showWebsiteModal" 
      class="modal-overlay"
      @click.self="showWebsiteModal = false"
    >
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Website Information</h5>
          <button 
            type="button" 
            class="btn-close" 
            @click="showWebsiteModal = false"
          ></button>
        </div>
        <div class="modal-body">
          <div v-if="selectedRecycler">
            <h6 class="fw-bold mb-3">{{ selectedRecycler.name }}</h6>
            <p class="mb-2">
              <strong>Website:</strong> 
              <a 
                :href="selectedRecycler.website" 
                target="_blank" 
                rel="noopener noreferrer"
                class="text-decoration-none"
              >
                {{ selectedRecycler.website }}
              </a>
            </p>
            <p class="mb-0">
              <strong>Description:</strong> {{ selectedRecycler.description }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Map Direction Modal -->
    <div 
      v-if="showMapModal" 
      class="modal-overlay"
      @click.self="showMapModal = false"
    >
      <div class="modal-content modal-lg">
        <div class="modal-header">
          <h5 class="modal-title">Map Direction</h5>
          <button 
            type="button" 
            class="btn-close" 
            @click="showMapModal = false"
          ></button>
        </div>
        <div class="modal-body">
          <div v-if="selectedRecycler">
            <h6 class="fw-bold mb-3">{{ selectedRecycler.name }}</h6>
            <div class="map-modal-content">
              <img 
                src="@/assets/map-placeholder.svg" 
                alt="Direction map" 
                class="map-modal-image"
                @error="handleMapImageError"
              >
              <div v-if="mapImageError" class="map-fallback-modal">
                <div class="map-placeholder-modal">
                  <i class="bi bi-map"></i>
                  <p>Map showing directions to {{ selectedRecycler.name }}</p>
                  <p class="text-muted">{{ selectedRecycler.address }}, {{ selectedRecycler.city }}, {{ selectedRecycler.state }} - {{ selectedRecycler.pincode }}</p>
                </div>
              </div>
            </div>
            <div class="mt-3">
              <p class="mb-2">
                <strong>Address:</strong> {{ selectedRecycler.address }}, {{ selectedRecycler.city }}, {{ selectedRecycler.state }} - {{ selectedRecycler.pincode }}
              </p>
              <a 
                :href="`https://www.google.com/maps/search/${selectedRecycler.address}+${selectedRecycler.city}+${selectedRecycler.pincode}`"
                target="_blank"
                rel="noopener noreferrer"
                class="btn btn-sm btn-primary"
              >
                <i class="bi bi-arrow-up-right me-1"></i>Open in Google Maps
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const searchPincode = ref('');
const searchPerformed = ref(false);
const showContactModal = ref(false);
const showWebsiteModal = ref(false);
const showMapModal = ref(false);
const selectedRecycler = ref(null);
const mapImageError = ref(false);

// Static recycler data for different pincodes
const recyclerDatabase = {
  '700001': [
    {
      id: 1,
      name: 'EcoRecycle Solutions',
      address: '45 Park Street',
      city: 'Kolkata',
      state: 'West Bengal',
      pincode: '700001',
      phone: '+91-9876543210',
      email: 'info@ecorecycle.com',
      website: 'https://www.ecorecycle.com',
      description: 'Leading recycling facility specializing in plastic, paper, and metal waste. We provide pickup services and ensure proper waste segregation.'
    },
    {
      id: 2,
      name: 'Green Earth Recyclers',
      address: '123 AJC Bose Road',
      city: 'Kolkata',
      state: 'West Bengal',
      pincode: '700001',
      phone: '+91-9876543211',
      email: 'contact@greenearthrecyclers.com',
      website: 'https://www.greenearthrecyclers.com',
      description: 'Comprehensive waste management and recycling services. We handle organic, inorganic, and hazardous waste with certified processes.'
    },
    {
      id: 3,
      name: 'Waste Warriors',
      address: '78 Chowringhee Lane',
      city: 'Kolkata',
      state: 'West Bengal',
      pincode: '700001',
      phone: '+91-9876543212',
      email: 'support@wastewarriors.com',
      website: 'https://www.wastewarriors.com',
      description: 'Community-focused recycling initiative promoting sustainable waste management practices in urban areas.'
    }
  ],
  '700020': [
    {
      id: 4,
      name: 'Urban Waste Solutions',
      address: '56 Ballygunge Circular Road',
      city: 'Kolkata',
      state: 'West Bengal',
      pincode: '700020',
      phone: '+91-9876543213',
      email: 'info@urbanwaste.com',
      website: 'https://www.urbanwaste.com',
      description: 'Professional waste segregation and recycling center with modern equipment and trained staff.'
    },
    {
      id: 5,
      name: 'Eco Friendly Disposal',
      address: '89 Rash Behari Avenue',
      city: 'Kolkata',
      state: 'West Bengal',
      pincode: '700020',
      phone: '+91-9876543214',
      email: 'contact@ecofriendly.com',
      website: 'https://www.ecofriendly.com',
      description: 'Dedicated to reducing landfill waste through innovative recycling and composting methods.'
    }
  ],
  '700040': [
    {
      id: 6,
      name: 'Sustainable Recycling Hub',
      address: '34 Gariahat Road',
      city: 'Kolkata',
      state: 'West Bengal',
      pincode: '700040',
      phone: '+91-9876543215',
      email: 'info@sustainablerecycling.com',
      website: 'https://www.sustainablerecycling.com',
      description: 'State-of-the-art recycling facility with focus on environmental sustainability and community engagement.'
    }
  ],
  '110001': [
    {
      id: 7,
      name: 'Delhi Waste Management',
      address: '12 Chandni Chowk',
      city: 'Delhi',
      state: 'Delhi',
      pincode: '110001',
      phone: '+91-9876543216',
      email: 'info@delhiwaste.com',
      website: 'https://www.delhiwaste.com',
      description: 'Comprehensive waste management services for residential and commercial areas in Delhi.'
    }
  ],
  '560001': [
    {
      id: 8,
      name: 'Bangalore Recyclers',
      address: '78 MG Road',
      city: 'Bangalore',
      state: 'Karnataka',
      pincode: '560001',
      phone: '+91-9876543217',
      email: 'info@bangalorerecyclers.com',
      website: 'https://www.bangalorerecyclers.com',
      description: 'Leading recycling center in Bangalore with expertise in e-waste and plastic recycling.'
    }
  ]
};

const filteredRecyclers = computed(() => {
  return recyclerDatabase[searchPincode.value] || [];
});

const searchRecyclers = () => {
  if (searchPincode.value.trim()) {
    searchPerformed.value = true;
    mapImageError.value = false;
  }
};

const showContactInfo = (recycler) => {
  selectedRecycler.value = recycler;
  showContactModal.value = true;
};

const showWebsite = (recycler) => {
  selectedRecycler.value = recycler;
  showWebsiteModal.value = true;
};

const showMapDirection = (recycler) => {
  selectedRecycler.value = recycler;
  showMapModal.value = true;
};

const handleMapImageError = () => {
  mapImageError.value = true;
};
</script>

<style scoped>
.recycler-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 0;
}

.search-section {
  padding: 20px 0;
}

.results-section {
  margin-top: 40px;
}

.recycler-cards {
  max-height: 800px;
  overflow-y: auto;
  padding-right: 10px;
}

.recycler-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.recycler-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  transform: translateY(-2px);
}

.recycler-card .card-title {
  font-size: 1.1rem;
  margin-bottom: 10px;
}

.recycler-card .card-text {
  font-size: 0.95rem;
  line-height: 1.5;
}

.button-group {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}

.button-group .btn {
  flex: 1;
  min-width: 100px;
  font-size: 0.85rem;
  padding: 6px 10px;
}

.map-container {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: fit-content;
  position: sticky;
  top: 100px;
}

.map-header {
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 15px;
}

.map-image-wrapper {
  position: relative;
  width: 100%;
  height: 400px;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
}

.map-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.map-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-placeholder {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.map-placeholder i {
  font-size: 3rem;
  margin-bottom: 10px;
  opacity: 0.8;
}

.map-placeholder p {
  margin: 10px 0;
  font-size: 0.95rem;
}

.recycler-markers {
  margin-top: 15px;
  text-align: left;
  font-size: 0.85rem;
}

.marker {
  display: flex;
  align-items: center;
  margin: 5px 0;
  padding: 5px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.marker-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: white;
  color: #667eea;
  border-radius: 50%;
  font-weight: bold;
  margin-right: 8px;
  flex-shrink: 0;
}

.marker-name {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-content.modal-lg {
  max-width: 700px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.modal-title {
  margin: 0;
  font-weight: 600;
  color: #333;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.modal-body p {
  margin-bottom: 12px;
  line-height: 1.6;
}

.modal-body strong {
  color: #333;
}

.modal-body a {
  color: #667eea;
  text-decoration: none;
}

.modal-body a:hover {
  text-decoration: underline;
}

.map-modal-content {
  position: relative;
  width: 100%;
  height: 300px;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

.map-modal-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.map-fallback-modal {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-placeholder-modal {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.map-placeholder-modal i {
  font-size: 2.5rem;
  margin-bottom: 10px;
  opacity: 0.8;
}

.map-placeholder-modal p {
  margin: 5px 0;
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 991.98px) {
  .recycler-container {
    padding: 10px;
  }

  .map-container {
    position: static;
    margin-top: 30px;
  }

  .recycler-cards {
    max-height: none;
  }

  .button-group .btn {
    font-size: 0.8rem;
    padding: 5px 8px;
  }

  .modal-content {
    max-width: 90%;
  }
}

@media (max-width: 576px) {
  .search-section .row {
    flex-direction: column;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group .btn {
    width: 100%;
  }

  .map-image-wrapper {
    height: 250px;
  }

  .modal-content {
    max-width: 95%;
    border-radius: 4px;
  }

  .modal-header {
    padding: 15px;
  }

  .modal-body {
    padding: 15px;
  }
}
</style>
