<template>
  <div class="secondary-pickup-details">
    <div class="container">
      <div class="row mb-4">
        <div class="col-12">
          <h2 class="text-white fw-bold mb-3">PICKUP DETAILS</h2>
          <p class="text-white-50">View scheduled waste pickup details for your RWA</p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="row mb-4">
        <div class="col-md-6 mb-3">
          <button class="btn btn-info btn-lg w-100" @click="navigateToPickupSummary">
            <i class="bi bi-graph-up me-2"></i>Pickup Summary
          </button>
        </div>
        <div class="col-md-6 mb-3">
          <button class="btn btn-warning btn-lg w-100" @click="navigateToDailyDetails">
            <i class="bi bi-calendar-day me-2"></i>Daily Details
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
                  <label for="pickupDate" class="form-label fw-semibold">Select Date (DD-MM-YYYY)</label>
                  <input 
                    type="date" 
                    id="pickupDate" 
                    v-model="selectedDate"
                    class="form-control"
                  >
                </div>
                <div class="col-md-6 d-flex align-items-end">
                  <button class="btn btn-primary w-100" @click="filterPickups">
                    <i class="bi bi-search me-2"></i>SEARCH
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pickup Details Cards -->
      <div class="row">
        <div class="col-md-6 col-lg-4 mb-4">
          <div class="card shadow-lg h-100">
            <div class="card-header bg-primary text-white">
              <h5 class="card-title mb-0">ORGANIC WASTE PICKUP</h5>
            </div>
            <div class="card-body d-flex flex-column">
              <p class="card-text"><strong>Date:</strong> {{ formattedDate }}</p>
              <p class="card-text"><strong>Time:</strong> 08:00 AM - 10:00 AM</p>
              <p class="card-text"><strong>Location:</strong> Main Gate</p>
              <p class="card-text"><strong>Quantity Expected:</strong> 50-75 KG</p>
              <p class="card-text"><strong>Status:</strong> <span class="badge bg-success">Scheduled</span></p>
              <p class="card-text text-muted small">Collect organic waste from households</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-4 mb-4">
          <div class="card shadow-lg h-100">
            <div class="card-header bg-info text-white">
              <h5 class="card-title mb-0">RECYCLABLE WASTE PICKUP</h5>
            </div>
            <div class="card-body d-flex flex-column">
              <p class="card-text"><strong>Date:</strong> {{ formattedDate }}</p>
              <p class="card-text"><strong>Time:</strong> 10:30 AM - 12:30 PM</p>
              <p class="card-text"><strong>Location:</strong> Community Center</p>
              <p class="card-text"><strong>Quantity Expected:</strong> 30-50 KG</p>
              <p class="card-text"><strong>Status:</strong> <span class="badge bg-success">Scheduled</span></p>
              <p class="card-text text-muted small">Collect recyclable materials (paper, plastic, metal)</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-4 mb-4">
          <div class="card shadow-lg h-100">
            <div class="card-header bg-warning text-dark">
              <h5 class="card-title mb-0">HAZARDOUS WASTE PICKUP</h5>
            </div>
            <div class="card-body d-flex flex-column">
              <p class="card-text"><strong>Date:</strong> {{ formattedDate }}</p>
              <p class="card-text"><strong>Time:</strong> 02:00 PM - 04:00 PM</p>
              <p class="card-text"><strong>Location:</strong> Storage Area</p>
              <p class="card-text"><strong>Quantity Expected:</strong> 10-20 KG</p>
              <p class="card-text"><strong>Status:</strong> <span class="badge bg-warning">Pending</span></p>
              <p class="card-text text-muted small">Collect hazardous household waste safely</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-4 mb-4">
          <div class="card shadow-lg h-100">
            <div class="card-header bg-success text-white">
              <h5 class="card-title mb-0">BULK WASTE PICKUP</h5>
            </div>
            <div class="card-body d-flex flex-column">
              <p class="card-text"><strong>Date:</strong> {{ formattedDate }}</p>
              <p class="card-text"><strong>Time:</strong> 04:30 PM - 06:30 PM</p>
              <p class="card-text"><strong>Location:</strong> Parking Area</p>
              <p class="card-text"><strong>Quantity Expected:</strong> 100-150 KG</p>
              <p class="card-text"><strong>Status:</strong> <span class="badge bg-success">Scheduled</span></p>
              <p class="card-text text-muted small">Collect large items and bulk waste</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-4 mb-4">
          <div class="card shadow-lg h-100">
            <div class="card-header bg-secondary text-white">
              <h5 class="card-title mb-0">E-WASTE PICKUP</h5>
            </div>
            <div class="card-body d-flex flex-column">
              <p class="card-text"><strong>Date:</strong> {{ formattedDate }}</p>
              <p class="card-text"><strong>Time:</strong> 07:00 PM - 08:30 PM</p>
              <p class="card-text"><strong>Location:</strong> Main Gate</p>
              <p class="card-text"><strong>Quantity Expected:</strong> 5-15 KG</p>
              <p class="card-text"><strong>Status:</strong> <span class="badge bg-secondary">Scheduled</span></p>
              <p class="card-text text-muted small">Collect electronic waste for recycling</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Pickup Summary Table -->
      <div class="row mt-4">
        <div class="col-12">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white">
              <h5 class="card-title mb-0">PICKUP SUMMARY FOR {{ formattedDate }}</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th>Waste Type</th>
                      <th>Time Slot</th>
                      <th>Location</th>
                      <th>Expected Quantity</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Organic Waste</td>
                      <td>08:00 AM - 10:00 AM</td>
                      <td>Main Gate</td>
                      <td>50-75 KG</td>
                      <td><span class="badge bg-success">Scheduled</span></td>
                    </tr>
                    <tr>
                      <td>Recyclable Waste</td>
                      <td>10:30 AM - 12:30 PM</td>
                      <td>Community Center</td>
                      <td>30-50 KG</td>
                      <td><span class="badge bg-success">Scheduled</span></td>
                    </tr>
                    <tr>
                      <td>Hazardous Waste</td>
                      <td>02:00 PM - 04:00 PM</td>
                      <td>Storage Area</td>
                      <td>10-20 KG</td>
                      <td><span class="badge bg-warning">Pending</span></td>
                    </tr>
                    <tr>
                      <td>Bulk Waste</td>
                      <td>04:30 PM - 06:30 PM</td>
                      <td>Parking Area</td>
                      <td>100-150 KG</td>
                      <td><span class="badge bg-success">Scheduled</span></td>
                    </tr>
                    <tr>
                      <td>E-Waste</td>
                      <td>07:00 PM - 08:30 PM</td>
                      <td>Main Gate</td>
                      <td>5-15 KG</td>
                      <td><span class="badge bg-secondary">Scheduled</span></td>
                    </tr>
                    <tr class="table-active fw-bold">
                      <td colspan="3">TOTAL EXPECTED WASTE</td>
                      <td>195-310 KG</td>
                      <td></td>
                    </tr>
                  </tbody>
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
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const selectedDate = ref(new Date().toISOString().split('T')[0]);

const formattedDate = computed(() => {
  if (!selectedDate.value) return '';
  const date = new Date(selectedDate.value);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}-${month}-${year}`;
});

const filterPickups = () => {
  console.log('Filtering pickups for date:', formattedDate.value);
  // Add filtering logic here
};

const navigateToPickupSummary = () => {
  router.push('/secondary-dashboard/pickup-summary');
};

const navigateToDailyDetails = () => {
  router.push('/secondary-dashboard/daily-pickup-details');
};
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
