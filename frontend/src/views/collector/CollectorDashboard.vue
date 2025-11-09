<template>
  <div class="collector-dashboard">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    
    <div v-else class="row">
      <!-- Pickup Summary Card -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-primary text-white">
            <h5 class="card-title mb-0">
              <i class="bi bi-calendar-check me-2"></i>PICKUP SUMMARY
            </h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5" v-if="dashboardData.pickup_summary">
              Today: {{ dashboardData.pickup_summary.total_pickups }} Pickups
            </p>
            <p class="card-text text-muted" v-if="dashboardData.pickup_summary">
              Completed: {{ dashboardData.pickup_summary.completed }} | 
              Pending: {{ dashboardData.pickup_summary.pending }}
            </p>
            <p class="card-text text-muted" v-else>
              View today's pickup schedule
            </p>
            <div class="mt-auto">
              <router-link to="/collector-dashboard/daily-pickup-details" class="btn btn-primary w-100">
                VIEW DETAILS
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Pickup Requests Card -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-warning text-dark">
            <h5 class="card-title mb-0">
              <i class="bi bi-inbox me-2"></i>PICKUP REQUESTS
            </h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5" v-if="dashboardData.pickup_summary">
              Pending: {{ dashboardData.pickup_summary.pending }} Requests
            </p>
            <p class="card-text text-muted" v-if="dashboardData.pickup_summary">
              Accept or reject pickup requests
            </p>
            <p class="card-text text-muted" v-else>
              Manage daily pickup requests
            </p>
            <div class="mt-auto">
              <router-link to="/collector-dashboard/daily-pickup-details" class="btn btn-warning w-100">
                MANAGE REQUESTS
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Pickup Summary (Monthly) Card -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-info text-white">
            <h5 class="card-title mb-0">
              <i class="bi bi-bar-chart me-2"></i>PICKUP SUMMARY
            </h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5">MONTHLY OVERVIEW</p>
            <p class="card-text text-muted">View detailed pickup statistics and trends</p>
            <div class="mt-auto">
              <router-link to="/collector-dashboard/pickup-summary" class="btn btn-info w-100 text-white">
                VIEW SUMMARY
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Ward Information Card -->
      <div class="col-md-12 mb-4" v-if="dashboardData.ward">
        <div class="card shadow-lg">
          <div class="card-header bg-success text-white">
            <h5 class="card-title mb-0">
              <i class="bi bi-geo-alt me-2"></i>WARD INFORMATION
            </h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-3">
                <p class="mb-1 text-muted">Ward Name</p>
                <h6 class="fw-bold">{{ dashboardData.ward.name || `Ward ${dashboardData.ward.ward_number}` }}</h6>
              </div>
              <div class="col-md-3">
                <p class="mb-1 text-muted">Ward Number</p>
                <h6 class="fw-bold">{{ dashboardData.ward.ward_number }}</h6>
              </div>
              <div class="col-md-3">
                <p class="mb-1 text-muted">Pincode</p>
                <h6 class="fw-bold">{{ dashboardData.ward.pincode }}</h6>
              </div>
              <div class="col-md-3">
                <p class="mb-1 text-muted">Households</p>
                <h6 class="fw-bold">{{ dashboardData.household_count || 0 }}</h6>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../../services/api';

const loading = ref(true);
const errorMessage = ref('');
const dashboardData = ref({
  user_role: null,
  ward: null,
  pickup_summary: null,
  household_count: 0
});

const fetchDashboardData = async () => {
  loading.value = true;
  errorMessage.value = '';
  
  try {
    const response = await api.get('/secondary/collector/dashboard');
    dashboardData.value = response.data;
  } catch (error) {
    console.error('Error fetching collector dashboard data:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to load dashboard data. Please try again.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchDashboardData();
});
</script>

<style scoped>
.collector-dashboard {
  padding: 2rem;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.card {
  border: none;
  border-radius: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15) !important;
}

.card-header {
  border-radius: 1rem 1rem 0 0 !important;
  border: none;
}

.card-body {
  padding: 1.5rem;
}

.btn {
  border-radius: 0.5rem;
  font-weight: 600;
  transition: all 0.3s;
}

.btn:hover {
  transform: scale(1.05);
}
</style>

