<template>
  <div class="secondary-pickup-details">
    <div class="container">
      <div class="row mb-4">
        <div class="col-12">
          <h2 class="text-white fw-bold mb-3">DAILY WASTE COLLECTION LOG</h2>
          <p class="text-white-50">View daily waste logs from households in your RWA area</p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="row mb-4">
        <div class="col-md-4 mb-3">
          <button class="btn btn-info btn-lg w-100" @click="navigateToPickupSummary">
            <i class="bi bi-graph-up me-2"></i>Pickup Summary
          </button>
        </div>
        <div class="col-md-4 mb-3">
          <button class="btn btn-warning btn-lg w-100" @click="navigateToDailyDetails">
            <i class="bi bi-calendar-day me-2"></i>Daily Pickup Requests
          </button>
        </div>
        <div class="col-md-4 mb-3">
          <button class="btn btn-secondary btn-lg w-100" @click="navigateToDashboard">
            <i class="bi bi-house me-2"></i>Back to Dashboard
          </button>
        </div>
      </div>

      <!-- Date Selector -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card shadow-lg">
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-md-6">
                  <label for="wasteLogDate" class="form-label fw-semibold">Select Date to View Waste Logs</label>
                  <input 
                    type="date" 
                    id="wasteLogDate" 
                    v-model="selectedDate"
                    class="form-control"
                    :max="new Date().toISOString().split('T')[0]"
                  >
                </div>
                <div class="col-md-6 d-flex align-items-end">
                  <button class="btn btn-primary w-100" @click="filterWasteLogs" :disabled="loading">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    <i v-else class="bi bi-search me-2"></i>SEARCH
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Summary Statistics Cards -->
      <div class="row mb-4" v-if="!loading && wasteSummary">
        <div class="col-md-3 mb-3">
          <div class="card shadow-lg h-100 border-primary">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Total Households</h6>
              <h3 class="card-text fw-bold text-primary">{{ wasteSummary.total_households }}</h3>
              <small class="text-muted">{{ wasteSummary.households_logged }} logged today</small>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card shadow-lg h-100 border-success">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Total Waste</h6>
              <h3 class="card-text fw-bold text-success">{{ wasteSummary.total_waste }} KG</h3>
              <small class="text-muted">Collected today</small>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card shadow-lg h-100 border-info">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Separated</h6>
              <h3 class="card-text fw-bold text-info">{{ wasteSummary.households_separated }}</h3>
              <small class="text-muted">Households</small>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card shadow-lg h-100 border-warning">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Recycled</h6>
              <h3 class="card-text fw-bold text-warning">{{ wasteSummary.households_recycled }}</h3>
              <small class="text-muted">Households</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Waste Category Summary -->
      <div class="row mb-4" v-if="!loading && wasteSummary">
        <div class="col-md-4 mb-3">
          <div class="card shadow-lg border-success">
            <div class="card-body">
              <h6 class="card-title text-muted">Wet Waste</h6>
              <h4 class="card-text fw-bold text-success">{{ wasteSummary.total_wet_waste }} KG</h4>
            </div>
          </div>
        </div>
        <div class="col-md-4 mb-3">
          <div class="card shadow-lg border-info">
            <div class="card-body">
              <h6 class="card-title text-muted">Dry Waste</h6>
              <h4 class="card-text fw-bold text-info">{{ wasteSummary.total_dry_waste }} KG</h4>
            </div>
          </div>
        </div>
        <div class="col-md-4 mb-3">
          <div class="card shadow-lg border-danger">
            <div class="card-body">
              <h6 class="card-title text-muted">Hazardous Waste</h6>
              <h4 class="card-text fw-bold text-danger">{{ wasteSummary.total_hazardous_waste }} KG</h4>
            </div>
          </div>
        </div>
      </div>

      <!-- Household Waste Logs Table -->
      <div class="row mt-4">
        <div class="col-12">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">HOUSEHOLD WASTE LOGS FOR {{ formattedDate }}</h5>
              <button class="btn btn-sm btn-light" @click="fetchWasteLogs">
                <i class="bi bi-arrow-clockwise me-1"></i>Refresh
              </button>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>
              <div v-else-if="errorMessage" class="alert alert-danger" role="alert">
                {{ errorMessage }}
              </div>
              <div v-else-if="householdWaste.length === 0" class="text-center py-5">
                <i class="bi bi-inbox" style="font-size: 3rem; color: #6c757d;"></i>
                <p class="text-muted mt-3">No households found in your area.</p>
              </div>
              <div v-else class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th>House No.</th>
                      <th>Household Name</th>
                      <th>Family Members</th>
                      <th>Wet Waste (KG)</th>
                      <th>Dry Waste (KG)</th>
                      <th>Hazardous (KG)</th>
                      <th>Total (KG)</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="household in householdWaste" :key="household.user_id" :class="{ 'table-warning': !household.has_logged }">
                      <td><strong>{{ household.house_number || 'N/A' }}</strong></td>
                      <td>{{ household.user_name }}</td>
                      <td>{{ household.family_members }}</td>
                      <td>
                        <span v-if="household.has_logged" class="badge bg-success">{{ household.wet_waste.toFixed(2) }}</span>
                        <span v-else class="text-muted">-</span>
                      </td>
                      <td>
                        <span v-if="household.has_logged" class="badge bg-info text-dark">{{ household.dry_waste.toFixed(2) }}</span>
                        <span v-else class="text-muted">-</span>
                      </td>
                      <td>
                        <span v-if="household.has_logged" class="badge bg-danger">{{ household.hazardous_waste.toFixed(2) }}</span>
                        <span v-else class="text-muted">-</span>
                      </td>
                      <td>
                        <strong v-if="household.has_logged">{{ household.total_waste.toFixed(2) }}</strong>
                        <span v-else class="text-muted">Not logged</span>
                      </td>
                      <td>
                        <span v-if="household.has_logged" class="badge bg-success">
                          <i class="bi bi-check-circle me-1"></i>Logged
                        </span>
                        <span v-else class="badge bg-warning text-dark">
                          <i class="bi bi-clock me-1"></i>Pending
                        </span>
                        <span v-if="household.separated" class="badge bg-info ms-1" title="Waste was properly separated">
                          <i class="bi bi-check2"></i>Separated
                        </span>
                        <span v-if="household.recycled" class="badge bg-success ms-1" title="Waste was recycled/reused">
                          <i class="bi bi-recycle"></i>Recycled
                        </span>
                      </td>
                      <td>
                        <button 
                          v-if="household.has_logged"
                          class="btn btn-sm btn-info" 
                          @click="viewHouseholdDetails(household)"
                          title="View details"
                        >
                          <i class="bi bi-eye"></i>
                        </button>
                        <span v-else class="text-muted">-</span>
                      </td>
                    </tr>
                  </tbody>
                  <tfoot v-if="householdWaste.length > 0" class="table-active">
                    <tr>
                      <td colspan="3" class="fw-bold">TOTAL</td>
                      <td class="fw-bold">{{ totalWetWaste.toFixed(2) }} KG</td>
                      <td class="fw-bold">{{ totalDryWaste.toFixed(2) }} KG</td>
                      <td class="fw-bold">{{ totalHazardousWaste.toFixed(2) }} KG</td>
                      <td class="fw-bold">{{ totalWaste.toFixed(2) }} KG</td>
                      <td colspan="2"></td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const router = useRouter();
const selectedDate = ref(new Date().toISOString().split('T')[0]);
const loading = ref(false);
const errorMessage = ref('');
const householdWaste = ref([]);
const wasteSummary = ref(null);

const formattedDate = computed(() => {
  if (!selectedDate.value) return '';
  const date = new Date(selectedDate.value);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}-${month}-${year}`;
});

const totalWetWaste = computed(() => {
  return householdWaste.value.reduce((sum, h) => sum + (h.wet_waste || 0), 0);
});

const totalDryWaste = computed(() => {
  return householdWaste.value.reduce((sum, h) => sum + (h.dry_waste || 0), 0);
});

const totalHazardousWaste = computed(() => {
  return householdWaste.value.reduce((sum, h) => sum + (h.hazardous_waste || 0), 0);
});

const totalWaste = computed(() => {
  return totalWetWaste.value + totalDryWaste.value + totalHazardousWaste.value;
});

const fetchWasteLogs = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';
    const response = await api.get('/secondary/waste-logs', {
      params: { date: selectedDate.value }
    });
    
    wasteSummary.value = response.data.summary;
    householdWaste.value = response.data.household_waste || [];
  } catch (error) {
    console.error('Error fetching waste logs:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to load waste logs. Please try again.';
    householdWaste.value = [];
    wasteSummary.value = null;
  } finally {
    loading.value = false;
  }
};

const viewHouseholdDetails = (household) => {
  let details = `Household Waste Details:\n\n`;
  details += `House Number: ${household.house_number || 'N/A'}\n`;
  details += `Household: ${household.user_name}\n`;
  details += `Family Members: ${household.family_members}\n`;
  details += `Pincode: ${household.pincode || 'N/A'}\n\n`;
  details += `Waste Categories:\n`;
  details += `- Wet Waste: ${household.wet_waste.toFixed(2)} KG\n`;
  details += `- Dry Waste: ${household.dry_waste.toFixed(2)} KG\n`;
  details += `- Hazardous Waste: ${household.hazardous_waste.toFixed(2)} KG\n`;
  details += `- Total: ${household.total_waste.toFixed(2)} KG\n\n`;
  details += `Status:\n`;
  details += `- Separated: ${household.separated ? 'Yes' : 'No'}\n`;
  details += `- Recycled: ${household.recycled ? 'Yes' : 'No'}\n`;
  
  if (household.questions_doubts) {
    details += `\nQuestions/Doubts: ${household.questions_doubts}\n`;
  }
  
  if (household.feedback) {
    details += `\nFeedback: ${household.feedback}\n`;
  }
  
  alert(details);
};

const filterWasteLogs = () => {
  fetchWasteLogs();
};

const navigateToPickupSummary = () => {
  router.push('/secondary-dashboard/pickup-summary');
};

const navigateToDailyDetails = () => {
  router.push('/secondary-dashboard/daily-pickup-details');
};

const navigateToDashboard = () => {
  router.push('/secondary-dashboard');
};

// Watch for date changes
watch(selectedDate, () => {
  fetchWasteLogs();
});

onMounted(() => {
  fetchWasteLogs();
});
</script>

<style scoped>
.secondary-pickup-details {
  padding: 1.5rem;
}

.card {
  border: none;
  border-radius: 0.5rem;
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

.card-header {
  border-bottom: none;
  border-radius: 0.5rem 0.5rem 0 0 !important;
}

.table {
  margin-bottom: 0;
}

.table-hover tbody tr:hover {
  background-color: #f5f5f5;
}

.table-active {
  background-color: #e7f3ff !important;
}

.badge {
  padding: 0.5rem 0.75rem;
  font-size: 0.85rem;
}

.form-control {
  border-radius: 0.5rem;
  border: 1px solid #ddd;
}

.form-control:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}
</style>
