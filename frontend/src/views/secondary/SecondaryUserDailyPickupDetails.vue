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
          <p class="text-white-50">View all pickup requests and their status for the selected date</p>
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
                <option value="Accept">Accept</option>
                <option value="Reject">Reject</option>
                <option value="Pending">Pending</option>
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
                      <th>User ID</th>
                      <th>Pick Up Location</th>
                      <th>Date of Pickup</th>
                      <th>Time of Pickup</th>
                      <th>Disposal Quantity</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="pickup in filteredPickups" :key="pickup.id">
                      <td><strong>{{ pickup.requestNo }}</strong></td>
                      <td>{{ pickup.userId }}</td>
                      <td>{{ pickup.location }}</td>
                      <td>{{ pickup.date }}</td>
                      <td>{{ pickup.time }}</td>
                      <td>{{ pickup.quantity }}</td>
                      <td>
                        <span :class="getStatusBadgeClass(pickup.status)">
                          {{ pickup.status }}
                        </span>
                      </td>
                      <td>
                        <div class="btn-group btn-group-sm" role="group">
                          <button 
                            class="btn btn-success" 
                            @click="acceptPickup(pickup.id)"
                            :disabled="pickup.status !== 'Pending'"
                            title="Accept pickup"
                          >
                            <i class="bi bi-check-lg"></i>
                          </button>
                          <button 
                            class="btn btn-danger" 
                            @click="rejectPickup(pickup.id)"
                            :disabled="pickup.status !== 'Pending'"
                            title="Reject pickup"
                          >
                            <i class="bi bi-x-lg"></i>
                          </button>
                          <button 
                            class="btn btn-info" 
                            @click="viewDetails(pickup.id)"
                            title="View details"
                          >
                            <i class="bi bi-eye"></i>
                          </button>
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
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const selectedDate = ref(new Date().toISOString().split('T')[0]);
const statusFilter = ref('');

// Sample pickup data
const pickupRequests = ref([
  { id: 1, requestNo: 'REQ001', userId: 'USER001', location: 'Block A, Apt 101', date: '15-01-2024', time: '09:00 AM', quantity: '5 KG', status: 'Accept' },
  { id: 2, requestNo: 'REQ002', userId: 'USER002', location: 'Block B, Apt 205', date: '15-01-2024', time: '09:15 AM', quantity: '3 KG', status: 'Accept' },
  { id: 3, requestNo: 'REQ003', userId: 'USER003', location: 'Block C, Apt 310', date: '15-01-2024', time: '09:30 AM', quantity: '7 KG', status: 'Reject' },
  { id: 4, requestNo: 'REQ004', userId: 'USER004', location: 'Block A, Apt 102', date: '15-01-2024', time: '09:45 AM', quantity: '4 KG', status: 'Accept' },
  { id: 5, requestNo: 'REQ005', userId: 'USER005', location: 'Block D, Apt 401', date: '15-01-2024', time: '10:00 AM', quantity: '6 KG', status: 'Accept' },
  { id: 6, requestNo: 'REQ006', userId: 'USER006', location: 'Block B, Apt 206', date: '15-01-2024', time: '10:15 AM', quantity: '2 KG', status: 'Reject' },
  { id: 7, requestNo: 'REQ007', userId: 'USER007', location: 'Block E, Apt 501', date: '15-01-2024', time: '10:30 AM', quantity: '8 KG', status: 'Accept' },
  { id: 8, requestNo: 'REQ008', userId: 'USER008', location: 'Block C, Apt 311', date: '15-01-2024', time: '10:45 AM', quantity: '5 KG', status: 'Pending' },
  { id: 9, requestNo: 'REQ009', userId: 'USER009', location: 'Block A, Apt 103', date: '15-01-2024', time: '11:00 AM', quantity: '4 KG', status: 'Accept' },
  { id: 10, requestNo: 'REQ010', userId: 'USER010', location: 'Block D, Apt 402', date: '15-01-2024', time: '11:15 AM', quantity: '6 KG', status: 'Pending' },
]);

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
  return filteredPickups.value.filter(p => p.status === 'Accept').length;
});

const rejectedCount = computed(() => {
  return filteredPickups.value.filter(p => p.status === 'Reject').length;
});

const pendingCount = computed(() => {
  return filteredPickups.value.filter(p => p.status === 'Pending').length;
});

const getStatusBadgeClass = (status) => {
  const classes = {
    'Accept': 'badge bg-success',
    'Reject': 'badge bg-danger',
    'Pending': 'badge bg-warning text-dark'
  };
  return classes[status] || 'badge bg-secondary';
};

const updatePickupDetails = () => {
  console.log('Updated pickup details for:', selectedDateFormatted.value);
};

const acceptPickup = (id) => {
  const pickup = pickupRequests.value.find(p => p.id === id);
  if (pickup && pickup.status === 'Pending') {
    pickup.status = 'Accept';
    alert(`Pickup ${pickup.requestNo} accepted successfully!`);
  }
};

const rejectPickup = (id) => {
  const pickup = pickupRequests.value.find(p => p.id === id);
  if (pickup && pickup.status === 'Pending') {
    pickup.status = 'Reject';
    alert(`Pickup ${pickup.requestNo} rejected successfully!`);
  }
};

const viewDetails = (id) => {
  const pickup = pickupRequests.value.find(p => p.id === id);
  if (pickup) {
    alert(`Viewing details for ${pickup.requestNo}\nLocation: ${pickup.location}\nQuantity: ${pickup.quantity}`);
  }
};

const goBack = () => {
  router.push('/secondary-dashboard/pickup-details');
};
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
