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
                :disabled="isLoading"
              >
            </div>
            <div class="col-md-4">
              <button 
                class="btn btn-danger btn-lg w-100 fw-semibold" 
                @click="searchRecyclers"
                :disabled="!searchPincode.trim() || isLoading"
              >
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                {{ isLoading ? 'SEARCHING...' : 'SEARCH' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Results Section -->
    <div v-if="searchPerformed" class="results-section">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h4 class="mb-0 fw-bold">RECYCLERS NEAR TO YOUR LOCATION</h4>
      </div>
      
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
                <h5 class="card-title text-danger fw-bold mb-2">{{ recycler.name }}</h5>
                <p class="card-text text-danger mb-2">
                  <i class="bi bi-geo-alt me-2"></i>{{ recycler.address }}
                </p>
                <p class="card-text text-danger mb-2">
                  <i class="bi bi-telephone me-2"></i>Phone No: {{ recycler.phone || 'N/A' }}
                </p>
                <p class="card-text text-danger mb-3">
                  <strong>We Recycle:</strong> {{ recycler.materials && recycler.materials.length > 0 ? recycler.materials.join(', ') : 'General Waste' }}
                </p>
                
                <div class="button-group d-flex gap-2 flex-wrap">
                  <button 
                    class="btn btn-sm btn-outline-primary fw-semibold"
                    @click="showContactInfo(recycler)"
                  >
                    <i class="bi bi-telephone me-1"></i>CONTACTS
                  </button>
                  <button 
                    v-if="recycler.website"
                    class="btn btn-sm btn-outline-success fw-semibold"
                    @click="showWebsite(recycler)"
                  >
                    <i class="bi bi-globe me-1"></i>WEBSITE
                  </button>
                  <button 
                    class="btn btn-sm btn-outline-info fw-semibold"
                    @click="showMapDirection(recycler)"
                  >
                    <i class="bi bi-map me-1"></i>DIRECTION (MAP)
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
            <div v-if="isLoading" class="map-loading">
              <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading map...</span>
                </div>
                <p class="mt-3 text-muted">Loading recycler locations...</p>
              </div>
            </div>
            <div 
              v-else-if="searchPerformed"
              ref="mapContainer" 
              class="map-wrapper"
              style="height: 500px; width: 100%; border-radius: 8px; overflow: hidden;"
            ></div>
            <div v-else class="map-placeholder-empty">
              <div class="text-center py-5">
                <i class="bi bi-map" style="font-size: 3rem; color: #ccc; margin-bottom: 10px;"></i>
                <p class="text-muted">Enter a pincode and click SEARCH to view recycler locations on the map</p>
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
            <h6 class="fw-bold mb-3 text-danger">{{ selectedRecycler.name }}</h6>
            <p class="mb-2">
              <strong>Phone:</strong> 
              <a :href="`tel:${selectedRecycler.phone}`" class="text-decoration-none text-danger">
                {{ selectedRecycler.phone || 'N/A' }}
              </a>
            </p>
            <p class="mb-2" v-if="selectedRecycler.website">
              <strong>Website:</strong> 
              <a :href="selectedRecycler.website" target="_blank" class="text-decoration-none text-danger">
                {{ selectedRecycler.website }}
              </a>
            </p>
            <p class="mb-2">
              <strong>Address:</strong> {{ selectedRecycler.address }} - {{ selectedRecycler.pincode }}
            </p>
            <p class="mb-0" v-if="selectedRecycler.materials && selectedRecycler.materials.length > 0">
              <strong>We Recycle:</strong> {{ selectedRecycler.materials.join(', ') }}
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
            <h6 class="fw-bold mb-3 text-danger">{{ selectedRecycler.name }}</h6>
            <p class="mb-2" v-if="selectedRecycler.website">
              <strong>Website:</strong> 
              <a 
                :href="selectedRecycler.website" 
                target="_blank" 
                rel="noopener noreferrer"
                class="text-decoration-none text-danger"
              >
                {{ selectedRecycler.website }}
              </a>
            </p>
            <p class="mb-2" v-else>
              <strong>Website:</strong> <span class="text-muted">Not available</span>
            </p>
            <p class="mb-2">
              <strong>Address:</strong> {{ selectedRecycler.address }} - {{ selectedRecycler.pincode }}
            </p>
            <p class="mb-0" v-if="selectedRecycler.materials && selectedRecycler.materials.length > 0">
              <strong>We Recycle:</strong> {{ selectedRecycler.materials.join(', ') }}
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
            <h6 class="fw-bold mb-3 text-danger">{{ selectedRecycler.name }}</h6>
            <div class="mt-3">
              <p class="mb-2">
                <strong>Address:</strong> {{ selectedRecycler.address }} - {{ selectedRecycler.pincode }}
              </p>
              <p class="mb-2" v-if="selectedRecycler.materials && selectedRecycler.materials.length > 0">
                <strong>We Recycle:</strong> {{ selectedRecycler.materials.join(', ') }}
              </p>
              <a 
                v-if="selectedRecycler.latitude && selectedRecycler.longitude"
                :href="`https://www.google.com/maps/dir/?api=1&destination=${selectedRecycler.latitude},${selectedRecycler.longitude}`"
                target="_blank"
                rel="noopener noreferrer"
                class="btn btn-sm btn-primary"
              >
                <i class="bi bi-arrow-up-right me-1"></i>Open in Google Maps
              </a>
              <a 
                v-else
                :href="`https://www.google.com/maps/search/${encodeURIComponent(selectedRecycler.address || '')}`"
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
import { ref, computed, onMounted, onBeforeUnmount, nextTick, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import api from '../../services/api';

const searchPincode = ref('');
const searchPerformed = ref(false);
const showContactModal = ref(false);
const showWebsiteModal = ref(false);
const showMapModal = ref(false);
const selectedRecycler = ref(null);
const mapImageError = ref(false);
const isLoading = ref(false);
const mapContainer = ref(null);
let map = null;
let markers = [];

// Fix for default marker icons in Leaflet with Vite
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Recyclers data from backend
const recyclers = ref([]);

const filteredRecyclers = computed(() => {
  return recyclers.value;
});

// Fetch recyclers from backend API
const searchRecyclers = async () => {
  if (!searchPincode.value.trim()) {
    return;
  }
  
  try {
    isLoading.value = true;
    searchPerformed.value = false;
    
    const response = await api.get(`/common/recyclers?pincode=${searchPincode.value.trim()}`);
    const data = response.data;
    
    recyclers.value = data.recyclers || [];
    searchPerformed.value = true;
    
    // Initialize map after data is loaded
    await nextTick();
    setTimeout(() => {
      initMap();
    }, 100);
  } catch (error) {
    console.error('Error fetching recyclers:', error);
    recyclers.value = [];
    searchPerformed.value = true;
    // Still initialize map even if no recyclers found
    await nextTick();
    setTimeout(() => {
      initMap();
    }, 100);
  } finally {
    isLoading.value = false;
  }
};

// Initialize Leaflet map
const initMap = () => {
  // Clear existing map and markers
  if (map) {
    map.remove();
    map = null;
  }
  markers = [];
  
  // Wait for next tick to ensure DOM is ready
  nextTick(() => {
    if (!mapContainer.value) {
      console.warn('Map container not found');
      return;
    }
    
    // Get center coordinates - use recycler locations or default to Kolkata area based on pincode
    // For pincode 700001, use Kolkata coordinates
    let centerLat = 22.5726; // Kolkata default
    let centerLng = 88.3639;
    let zoom = 13;
    
    // Try to determine center based on pincode if no recyclers
    if (searchPincode.value === '700001' || searchPincode.value.startsWith('700')) {
      centerLat = 22.5726;
      centerLng = 88.3639;
      zoom = 13;
    }
    
    if (recyclers.value.length > 0) {
      const validCoords = recyclers.value.filter(r => r.latitude && r.longitude);
      if (validCoords.length > 0) {
        if (validCoords.length === 1) {
          // Single recycler - center on it
          centerLat = validCoords[0].latitude;
          centerLng = validCoords[0].longitude;
          zoom = 15;
        } else {
          // Multiple recyclers - calculate center
          const avgLat = validCoords.reduce((sum, r) => sum + r.latitude, 0) / validCoords.length;
          const avgLng = validCoords.reduce((sum, r) => sum + r.longitude, 0) / validCoords.length;
          centerLat = avgLat;
          centerLng = avgLng;
          zoom = 13;
        }
      }
    }
    
    try {
      // Initialize map
      map = L.map(mapContainer.value, {
        center: [centerLat, centerLng],
        zoom: zoom,
        zoomControl: true
      });
      
      // Add OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
      }).addTo(map);
      
      // Add markers for each recycler
      recyclers.value.forEach((recycler, index) => {
        if (recycler.latitude && recycler.longitude) {
          // Create custom icon with number (red circle with white number)
          const iconHtml = `
            <div style="background-color: #dc3545; color: white; width: 32px; height: 32px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px;
                        border: 3px solid white; box-shadow: 0 2px 6px rgba(0,0,0,0.4); cursor: pointer;">
              ${index + 1}
            </div>
          `;
          
          const customIcon = L.divIcon({
            html: iconHtml,
            className: 'custom-marker',
            iconSize: [32, 32],
            iconAnchor: [16, 32],
            popupAnchor: [0, -32]
          });
          
          const marker = L.marker([recycler.latitude, recycler.longitude], {
            icon: customIcon
          }).addTo(map);
          
          // Create popup content with recycler details
          const materialsText = recycler.materials && recycler.materials.length > 0 
            ? recycler.materials.join(', ') 
            : 'General Waste';
          
          const popupContent = `
            <div style="min-width: 240px; max-width: 320px;">
              <h6 style="margin: 0 0 12px 0; font-weight: bold; color: #dc3545; font-size: 1.15em; border-bottom: 2px solid #eee; padding-bottom: 8px;">${recycler.name}</h6>
              <p style="margin: 8px 0; font-size: 0.9em; color: #333; line-height: 1.6;">
                <strong style="color: #666; display: block; margin-bottom: 4px;">Address:</strong>
                <span style="color: #555;">${recycler.address || 'N/A'}</span>
              </p>
              <p style="margin: 8px 0; font-size: 0.9em; color: #333;">
                <strong style="color: #666; display: block; margin-bottom: 4px;">Phone:</strong> 
                <a href="tel:${recycler.phone || ''}" style="color: #007bff; text-decoration: none; font-weight: 500;">${recycler.phone || 'N/A'}</a>
              </p>
              <p style="margin: 8px 0; font-size: 0.9em; color: #333;">
                <strong style="color: #666; display: block; margin-bottom: 4px;">We Recycle:</strong> 
                <span style="color: #28a745; font-weight: 500;">${materialsText}</span>
              </p>
              ${recycler.website ? `
                <a href="${recycler.website}" target="_blank" 
                   style="display: inline-block; margin-top: 10px; padding: 6px 12px; background-color: #007bff; 
                          color: white; text-decoration: none; border-radius: 4px; font-size: 0.85em; font-weight: 500;">
                  <i class="bi bi-globe" style="margin-right: 4px;"></i>Visit Website
                </a>
              ` : ''}
            </div>
          `;
          
          marker.bindPopup(popupContent);
          markers.push(marker);
        }
      });
      
      // Fit map to show all markers if we have any
      if (markers.length > 0) {
        setTimeout(() => {
          try {
            const group = new L.featureGroup(markers);
            map.fitBounds(group.getBounds().pad(0.15));
          } catch (e) {
            console.error('Error fitting bounds:', e);
          }
        }, 200);
      } else {
        // No recyclers with coordinates - show area around pincode
        map.setView([centerLat, centerLng], zoom);
      }
    } catch (error) {
      console.error('Error initializing map:', error);
    }
  });
};

const showContactInfo = (recycler) => {
  selectedRecycler.value = recycler;
  showContactModal.value = true;
};

const showWebsite = (recycler) => {
  selectedRecycler.value = recycler;
  if (recycler.website) {
    window.open(recycler.website, '_blank');
  } else {
    showWebsiteModal.value = true;
  }
};

const showMapDirection = (recycler) => {
  selectedRecycler.value = recycler;
  if (recycler.latitude && recycler.longitude) {
    // Open Google Maps with directions
    const url = `https://www.google.com/maps/dir/?api=1&destination=${recycler.latitude},${recycler.longitude}`;
    window.open(url, '_blank');
  } else {
    // Fallback to address search
    const address = encodeURIComponent(recycler.address || '');
    const url = `https://www.google.com/maps/search/?api=1&query=${address}`;
    window.open(url, '_blank');
  }
};

const handleMapImageError = () => {
  mapImageError.value = true;
};

// Watch for recyclers changes to update map
watch(() => recyclers.value, () => {
  if (searchPerformed.value) {
    nextTick(() => {
      initMap();
    });
  }
}, { deep: true });

// Cleanup on unmount
onBeforeUnmount(() => {
  if (map) {
    map.remove();
    map = null;
  }
  markers = [];
});
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
  border: 1px solid #d1d1d1;
  border-radius: 8px;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #f0f8f0 0%, #e8f5e9 100%);
}

.recycler-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  transform: translateY(-2px);
  border-color: #28a745;
  background: linear-gradient(135deg, #e8f5e9 0%, #d4edda 100%);
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

.map-wrapper {
  position: relative;
  width: 100%;
  height: 500px;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #e0e0e0;
}

.map-loading {
  height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 8px;
  border: 2px solid #e0e0e0;
}

.map-placeholder-empty {
  height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 8px;
  border: 2px solid #e0e0e0;
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

/* Custom marker styles */
:deep(.custom-marker) {
  background: transparent;
  border: none;
}

/* Leaflet map container styles */
:deep(.leaflet-container) {
  font-family: inherit;
  z-index: 1;
}

:deep(.leaflet-popup-content-wrapper) {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

:deep(.leaflet-popup-tip) {
  background: white;
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

  .map-wrapper {
    height: 400px !important;
  }

  .map-loading,
  .map-placeholder-empty {
    height: 400px !important;
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
