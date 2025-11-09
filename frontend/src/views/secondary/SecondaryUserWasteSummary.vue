<template>
  <div class="secondary-waste-summary">
    <div class="container">
      <div class="row mb-4">
        <div class="col-12">
          <h2 class="text-white fw-bold mb-3">WASTE SUMMARY</h2>
          <p class="text-white-50">View comprehensive waste statistics and trends for your RWA</p>
        </div>
      </div>

      <!-- Summary Cards -->
      <div class="row mb-4">
        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Total Waste Collected</h6>
              <h3 class="card-text fw-bold text-primary">{{ totalWaste }} KG</h3>
              <p class="card-text text-muted small">This month</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Waste Diverted</h6>
              <h3 class="card-text fw-bold text-success">{{ totalDiverted }} KG</h3>
              <p class="card-text text-muted small">Recycled/Composted</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Landfill Waste</h6>
              <h3 class="card-text fw-bold text-danger">{{ totalLandfill }} KG</h3>
              <p class="card-text text-muted small">Sent to landfill</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Diversion Rate</h6>
              <h3 class="card-text fw-bold text-info">{{ diversionRate }}%</h3>
              <p class="card-text text-muted small">Waste diverted</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Detailed Table -->
      <div class="row">
        <div class="col-12">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white">
              <h5 class="card-title mb-0">WASTE BREAKDOWN BY CATEGORY</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th>Category</th>
                      <th>Quantity (KG)</th>
                      <th>Percentage</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="loading">
                      <td colspan="4" class="text-center py-4">
                        <div class="spinner-border text-primary" role="status">
                          <span class="visually-hidden">Loading...</span>
                        </div>
                      </td>
                    </tr>
                    <tr v-else-if="errorMessage">
                      <td colspan="4" class="text-center py-4">
                        <div class="alert alert-danger mb-0">{{ errorMessage }}</div>
                      </td>
                    </tr>
                    <tr v-else-if="wasteData.household_details.length === 0">
                      <td colspan="4" class="text-center py-4 text-muted">
                        No waste data available
                      </td>
                    </tr>
                    <tr v-else>
                      <td>Total Households</td>
                      <td>{{ wasteData.total_households }}</td>
                      <td>100%</td>
                      <td><span class="badge bg-info">Active</span></td>
                    </tr>
                    <tr>
                      <td>Segregation Rate</td>
                      <td>{{ wasteData.segregation_rate }}%</td>
                      <td>{{ wasteData.segregation_rate }}%</td>
                      <td><span class="badge bg-success">Good</span></td>
                    </tr>
                    <tr>
                      <td>Recycle/Reuse/Donation Rate</td>
                      <td>{{ wasteData.recycle_reuse_donations_rate }}%</td>
                      <td>{{ wasteData.recycle_reuse_donations_rate }}%</td>
                      <td><span class="badge bg-info">Active</span></td>
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
import { ref, onMounted, computed } from 'vue';
import api from '@/services/api';

const loading = ref(true);
const errorMessage = ref('');
const wasteData = ref({
  total_households: 0,
  segregation_rate: 0,
  recycle_reuse_donations_rate: 0,
  household_details: []
});

const totalWaste = computed(() => {
  return wasteData.value.household_details.reduce((sum, hh) => {
    return sum + hh.per_capita_wet + hh.per_capita_dry + hh.per_capita_hazardous;
  }, 0).toFixed(0);
});

const totalDiverted = computed(() => {
  return wasteData.value.household_details.reduce((sum, hh) => {
    const diverted = (hh.recycle_reuse_donation_percentage / 100) * (hh.per_capita_wet + hh.per_capita_dry + hh.per_capita_hazardous);
    return sum + diverted;
  }, 0).toFixed(0);
});

const totalLandfill = computed(() => {
  return (totalWaste.value - totalDiverted.value).toFixed(0);
});

const diversionRate = computed(() => {
  if (totalWaste.value > 0) {
    return ((totalDiverted.value / totalWaste.value) * 100).toFixed(0);
  }
  return 0;
});

const fetchWasteSummary = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';
    const response = await api.get('/secondary/waste-summary');
    wasteData.value = response.data;
  } catch (error) {
    console.error('Error fetching waste summary:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to load waste summary. Please try again.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchWasteSummary();
});
</script>

<style scoped>
.secondary-waste-summary {
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

.badge {
  padding: 0.5rem 0.75rem;
  font-size: 0.85rem;
}
</style>
