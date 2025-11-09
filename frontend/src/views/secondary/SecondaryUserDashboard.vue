<template>
  <div class="secondary-user-dashboard">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    
    <div v-else class="row">
      <!-- RWA Leaderboard Card -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-warning text-dark">
            <h5 class="card-title mb-0">
              <i class="bi bi-trophy me-2"></i>RWA LEADERBOARD
            </h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5" v-if="dashboardData.rwa_leaderboard">
              Rank: #{{ dashboardData.rwa_leaderboard.rank }}
            </p>
            <p class="card-text text-muted" v-if="dashboardData.rwa_leaderboard">
              {{ dashboardData.rwa_leaderboard.households }} Households
            </p>
            <p class="card-text text-muted" v-if="dashboardData.rwa_leaderboard && dashboardData.rwa_leaderboard.rwa_name">
              RWA: {{ dashboardData.rwa_leaderboard.rwa_name }}
            </p>
            <p class="card-text text-muted" v-else>
              View RWA rankings and performance metrics
            </p>
            <div class="mt-auto">
              <router-link to="/secondary-dashboard/rwa-leaderboard" class="btn btn-warning w-100">
                VIEW DETAILS
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Waste Summary Card -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-info text-white">
            <h5 class="card-title mb-0">
              <i class="bi bi-trash me-2"></i>WASTE SUMMARY
            </h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5">RWA WASTE OVERVIEW</p>
            <p class="card-text text-muted">View comprehensive waste statistics for your RWA</p>
            <div class="mt-auto">
              <router-link to="/secondary-dashboard/waste-summary" class="btn btn-info w-100 text-white">
                VIEW DETAILS
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Campaigns Card -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-success text-white">
            <h5 class="card-title mb-0">
              <i class="bi bi-megaphone me-2"></i>CAMPAIGNS
            </h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5">MANAGE CAMPAIGNS</p>
            <p class="card-text text-muted">View and manage waste management campaigns</p>
            <div class="mt-auto">
              <router-link to="/secondary-dashboard/campaigns" class="btn btn-success w-100">
                VIEW CAMPAIGNS
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const loading = ref(true);
const errorMessage = ref('');
const dashboardData = ref({
  user_role: null,
  rwa_leaderboard: null
});

const fetchDashboard = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';
    const response = await api.get('/secondary/dashboard');
    dashboardData.value = response.data;
  } catch (error) {
    console.error('Error fetching dashboard:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to load dashboard data. Please try again.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchDashboard();
});
</script>

<style scoped>
.secondary-user-dashboard {
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

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}
</style>
