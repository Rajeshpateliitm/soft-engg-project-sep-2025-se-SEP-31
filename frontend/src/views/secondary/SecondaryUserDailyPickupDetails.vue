<template>
  <div class="daily-pickup-container">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex align-items-center mb-3">
            <button class="btn btn-link text-white p-0 me-2" @click="goBack">
              <i class="bi bi-arrow-left" style="font-size: 1.5rem;"></i>
            </button>
            <h2 class="text-white fw-bold mb-0">PICKUP DETAILS OF {{ selectedDateFormatted }}</h2>
          </div>
          <p class="text-white-50">{{ isCollector ? 'View and manage pickup requests for the selected date' : 'View all pickup requests and their status for the selected date (Read-only)' }}</p>
        </div>
      </div>

      <!-- Date Selector -->
      <div class="row mb-4">
        <div class="col-md-6 mb-3">
          <div class="card shadow-lg">
            <div class="card-body">
              <label class="form-label fw-semibold">Select Date</label>
              <input 
                type="date" 
                v-model="selectedDate"
                class="form-control form-control-lg"
                :max="new Date().toISOString().split('T')[0]"
                @change="updatePickupDetails"
              >
            </div>
          </div>
        </div>
        <div class="col-md-6 mb-3">
          <div class="card shadow-lg">
            <div class="card-body">
              <label class="form-label fw-semibold">Filter by Status</label>
              <select v-model="statusFilter" class="form-select form-select-lg" @change="updatePickupDetails">
                <option value="">All Status</option>
                <option value="accepted">Accepted</option>
                <option value="rejected">Rejected</option>
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Summary Cards -->
      <div class="row mb-4">
        <div class="col-md-3 mb-3">
          <div class="summary-card accepted">
            <div class="summary-icon">
              <i class="bi bi-check-circle"></i>
            </div>
            <div class="summary-content">
              <div class="summary-label">Accepted</div>
              <div class="summary-value">{{ acceptedCount }}</div>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="summary-card rejected">
            <div class="summary-icon">
              <i class="bi bi-x-circle"></i>
            </div>
            <div class="summary-content">
              <div class="summary-label">Rejected</div>
              <div class="summary-value">{{ rejectedCount }}</div>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="summary-card pending">
            <div class="summary-icon">
              <i class="bi bi-clock-history"></i>
            </div>
            <div class="summary-content">
              <div class="summary-label">Pending</div>
              <div class="summary-value">{{ pendingCount }}</div>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="summary-card total">
            <div class="summary-icon">
              <i class="bi bi-list-check"></i>
            </div>
            <div class="summary-content">
              <div class="summary-label">Total</div>
              <div class="summary-value">{{ filteredPickups.length }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pickup Details Table -->
      <div class="row">
        <div class="col-12">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white">
              <h5 class="card-title mb-0">Pickup Requests for {{ selectedDateFormatted }}</h5>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-hover mb-0">
                  <thead class="table-light">
                    <tr>
                      <th>Request No.</th>
                      <th>Household Name</th>
                      <th>House Number</th>
                      <th>Pick Up Location</th>
                      <th>Date of Pickup</th>
                      <th>Time of Pickup</th>
                      <th>Disposal Quantity (KG)</th>
                      <th>Status</th>
                      <th>{{ isCollector ? 'Actions' : 'Status Details' }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="loading">
                      <td colspan="9" class="text-center py-4">
                        <div class="spinner-border text-primary" role="status">
                          <span class="visually-hidden">Loading...</span>
                        </div>
                      </td>
                    </tr>
                    <tr v-else-if="errorMessage">
                      <td colspan="9" class="text-center py-4">
                        <div class="alert alert-danger mb-0">{{ errorMessage }}</div>
                      </td>
                    </tr>
                    <tr v-else-if="!loading && filteredPickups.length === 0 && pickupRequests.length === 0">
                      <td colspan="9" class="text-center py-4 text-muted">
                        <i class="bi bi-inbox" style="font-size: 2rem; color: #6c757d;"></i>
                        <p class="mt-3 mb-0">No pickup requests found for the selected date.</p>
                        <p class="text-muted small">Pickup requests are created when primary users log waste.</p>
                      </td>
                    </tr>
                    <tr v-else-if="!loading && filteredPickups.length === 0 && pickupRequests.length > 0">
                      <td colspan="9" class="text-center py-4 text-muted">
                        <i class="bi bi-funnel" style="font-size: 2rem; color: #6c757d;"></i>
                        <p class="mt-3 mb-0">No pickup requests match the selected status filter.</p>
                        <p class="text-muted small">Try changing the status filter or select a different date.</p>
                      </td>
                    </tr>
                    <tr v-else v-for="pickup in filteredPickups" :key="pickup.id">
                      <td><strong>{{ pickup.requestNo }}</strong></td>
                      <td>{{ pickup.userName || 'Unknown' }}</td>
                      <td>{{ pickup.houseNumber || 'N/A' }}</td>
                      <td>{{ pickup.location }}</td>
                      <td>{{ pickup.date }}</td>
                      <td>{{ pickup.time }}</td>
                      <td><strong>{{ pickup.quantity }}</strong></td>
                      <td>
                        <span :class="getStatusBadgeClass(pickup.status)">
                          {{ getStatusDisplay(pickup.status) }}
                        </span>
                      </td>
                      <td>
                        <div class="btn-group btn-group-sm" role="group" v-if="isCollector">
                          <button 
                            v-if="pickup.status === 'pending'"
                            class="btn btn-success" 
                            @click="acceptPickup(pickup.requestNo)"
                            title="Accept pickup"
                          >
                            <i class="bi bi-check-lg"></i> Accept
                          </button>
                          <button 
                            v-if="pickup.status === 'pending'"
                            class="btn btn-danger" 
                            @click="rejectPickup(pickup.requestNo)"
                            title="Reject pickup"
                          >
                            <i class="bi bi-x-lg"></i> Reject
                          </button>
                          <button 
                            class="btn btn-info" 
                            @click="viewDetails(pickup.requestNo)"
                            title="View details"
                          >
                            <i class="bi bi-eye"></i>
                          </button>
                        </div>
                        <div v-else class="text-muted">
                          <small>View Only</small>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-if="filteredPickups.length === 0" class="text-center py-5">
                <i class="bi bi-inbox" style="font-size: 3rem; color: #6c757d;"></i>
                <p class="text-muted mt-3">No pickup requests found for the selected date and status.</p>
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
import { useAuthStore } from '@/stores/auth';
import api from '@/services/api';

const router = useRouter();
const authStore = useAuthStore();
const selectedDate = ref(new Date().toISOString().split('T')[0]);
const statusFilter = ref('');
const loading = ref(false);
const errorMessage = ref('');
const pickupRequests = ref([]);

// Check if user is a collector (not RWA manager)
const isCollector = computed(() => {
  return authStore.rwaRole === 'collector';
});

const selectedDateFormatted = computed(() => {
  if (!selectedDate.value) return '';
  const date = new Date(selectedDate.value);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}-${month}-${year}`;
});

const filteredPickups = computed(() => {
  return pickupRequests.value.filter(pickup => {
    const matchesStatus = !statusFilter.value || pickup.status === statusFilter.value;
    return matchesStatus;
  });
});

const acceptedCount = computed(() => {
  return pickupRequests.value.filter(p => p.status === 'accepted').length;
});

const rejectedCount = computed(() => {
  return pickupRequests.value.filter(p => p.status === 'rejected').length;
});

const pendingCount = computed(() => {
  return pickupRequests.value.filter(p => p.status === 'pending').length;
});

const getStatusBadgeClass = (status) => {
  const classes = {
    'accepted': 'badge bg-success',
    'rejected': 'badge bg-danger',
    'pending': 'badge bg-warning text-dark',
    'completed': 'badge bg-info'
  };
  return classes[status] || 'badge bg-secondary';
};

const getStatusDisplay = (status) => {
  const display = {
    'accepted': 'Accepted',
    'rejected': 'Rejected',
    'pending': 'Pending',
    'completed': 'Completed'
  };
  return display[status] || status;
};

const fetchPickupDetails = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';
    
    const response = await api.get('/secondary/pickup-details', {
      params: { date: selectedDate.value }
    });
    
    // Transform backend data to frontend format
    if (response.data && response.data.pickups) {
      pickupRequests.value = response.data.pickups.map(pickup => ({
        pickupId: pickup.pickup_id,
        id: pickup.request_no,
        requestNo: pickup.request_no,
        userId: pickup.user_id,
        userName: pickup.user_name || 'Unknown',
        userEmail: pickup.user_email || 'N/A',
        houseNumber: pickup.house_number || 'N/A',
        location: pickup.pickup_location || 'N/A',
        date: pickup.date_of_pickup ? new Date(pickup.date_of_pickup).toLocaleDateString('en-GB') : 'N/A',
        time: pickup.time_of_pickup || 'N/A',
        quantity: pickup.disposal_quantity ? `${parseFloat(pickup.disposal_quantity).toFixed(2)}` : '0.00',
        status: pickup.status || 'pending'
      }));
    } else {
      pickupRequests.value = [];
    }
  } catch (error) {
    console.error('Error fetching pickup details:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to load pickup details. Please try again.';
    pickupRequests.value = [];
  } finally {
    loading.value = false;
  }
};

const updatePickupDetails = () => {
  fetchPickupDetails();
};

const acceptPickup = async (requestNo) => {
  try {
    // Find the pickup by request_no
    const pickup = pickupRequests.value.find(p => p.requestNo === requestNo);
    if (!pickup) {
      alert('Pickup request not found');
      return;
    }
    
    // Use the pickup ID from the backend response
    const pickupId = pickup.pickupId;
    
    if (!pickupId) {
      alert('Unable to identify pickup request');
      return;
    }
    
    await api.post(`/secondary/pickup/${pickupId}/accept`);
    
    // Refresh the list
    await fetchPickupDetails();
    
    alert(`Pickup ${requestNo} accepted successfully!`);
  } catch (error) {
    console.error('Error accepting pickup:', error);
    alert(error.response?.data?.error || 'Failed to accept pickup. Please try again.');
  }
};

const rejectPickup = async (requestNo) => {
  try {
    // Find the pickup by request_no
    const pickup = pickupRequests.value.find(p => p.requestNo === requestNo);
    if (!pickup) {
      alert('Pickup request not found');
      return;
    }
    
    // Use the pickup ID from the backend response
    const pickupId = pickup.pickupId;
    
    if (!pickupId) {
      alert('Unable to identify pickup request');
      return;
    }
    
    await api.post(`/secondary/pickup/${pickupId}/reject`);
    
    // Refresh the list
    await fetchPickupDetails();
    
    alert(`Pickup ${requestNo} rejected successfully!`);
  } catch (error) {
    console.error('Error rejecting pickup:', error);
    alert(error.response?.data?.error || 'Failed to reject pickup. Please try again.');
  }
};

const viewDetails = (requestNo) => {
  const pickup = pickupRequests.value.find(p => p.requestNo === requestNo);
  if (pickup) {
    let details = `Pickup Request Details:\n\n`;
    details += `Request No: ${pickup.requestNo}\n`;
    details += `Household: ${pickup.userName}\n`;
    details += `House Number: ${pickup.houseNumber || 'N/A'}\n`;
    details += `Email: ${pickup.userEmail || 'N/A'}\n`;
    details += `Location: ${pickup.location}\n`;
    details += `Date: ${pickup.date}\n`;
    details += `Time: ${pickup.time}\n`;
    details += `Quantity: ${pickup.quantity}\n`;
    details += `Status: ${getStatusDisplay(pickup.status)}\n`;
    alert(details);
  }
};

const goBack = () => {
  router.push('/secondary-dashboard/pickup-details');
};

// Watch for date changes
watch(selectedDate, (newDate) => {
  if (newDate) {
    fetchPickupDetails();
  }
});

onMounted(() => {
  // Set default date to today if not set
  if (!selectedDate.value) {
    selectedDate.value = new Date().toISOString().split('T')[0];
  }
  fetchPickupDetails();
});
</script>

<style scoped>
.daily-pickup-container {
  padding: 1.5rem;
  min-height: 100vh;
}

.summary-card {
  padding: 1.5rem;
  border-radius: 0.75rem;
  color: white;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.summary-card:hover {
  transform: translateY(-5px);
}

.summary-card.accepted {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.summary-card.rejected {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.summary-card.pending {
  background: linear-gradient(135deg, #ffa751 0%, #ffe259 100%);
}

.summary-card.total {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.summary-icon {
  font-size: 2.5rem;
  opacity: 0.8;
}

.summary-content {
  flex: 1;
}

.summary-label {
  font-size: 0.85rem;
  font-weight: 600;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.summary-value {
  font-size: 2rem;
  font-weight: 700;
}

.card {
  border: none;
  border-radius: 0.75rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.card-header {
  border-bottom: 1px solid #dee2e6;
  border-radius: 0.75rem 0.75rem 0 0 !important;
}

.table {
  margin-bottom: 0;
}

.table-hover tbody tr:hover {
  background-color: #f8f9fa;
}

.table thead th {
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #dee2e6;
}

.badge {
  padding: 0.5rem 0.75rem;
  font-size: 0.85rem;
  font-weight: 600;
}

.btn-group-sm .btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.85rem;
}

.btn-group-sm .btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-control,
.form-select {
  border-radius: 0.5rem;
  border: 1px solid #dee2e6;
}

.form-control:focus,
.form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .daily-pickup-container {
    padding: 1rem;
  }

  .summary-card {
    flex-direction: column;
    text-align: center;
  }

  .summary-icon {
    font-size: 2rem;
  }

  .summary-value {
    font-size: 1.5rem;
  }

  .table {
    font-size: 0.9rem;
  }

  .btn-group-sm .btn {
    padding: 0.2rem 0.4rem;
    font-size: 0.75rem;
  }
}
</style>
