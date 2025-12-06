<template>
  <div class="secondary-rwa-leaderboard">
    <div class="container">
      <div class="row mb-4">
        <div class="col-12">
          <h2 class="text-success fw-bold mb-3">RWA LEADERBOARD</h2>
          <p class="text-secondary-emphasis">
            View RWA rankings based on waste management performance
          </p>
        </div>
      </div>

      <!-- Leaderboard Stats -->
      <div class="row mb-4">
        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Total RWAs</h6>
              <h3 class="card-text fw-bold text-primary">{{ totalRwas }}</h3>
              <p class="card-text text-muted small">Participating</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Your Rank</h6>
              <h3 class="card-text fw-bold text-success">{{ userRwaRank || '-' }}</h3>
              <p class="card-text text-muted small" v-if="totalRwas > 0">Out of {{ totalRwas }}</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Your Points</h6>
              <h3 class="card-text fw-bold text-info">{{ userRwaPoints }}</h3>
              <p class="card-text text-muted small">Total score</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Diversion Rate</h6>
              <h3 class="card-text fw-bold text-warning">72%</h3>
              <p class="card-text text-muted small">Waste diverted</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Leaderboard Table -->
      <div class="row">
        <div class="col-12">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white">
              <h5 class="card-title mb-0">TOP RWA PERFORMERS</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th>Rank</th>
                      <th>RWA Name</th>
                      <th>Points</th>
                      <th>Waste Diverted (KG)</th>
                      <th>Diversion Rate</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="loading">
                      <td colspan="6" class="text-center py-4">
                        <div class="spinner-border text-primary" role="status">
                          <span class="visually-hidden">Loading...</span>
                        </div>
                      </td>
                    </tr>
                    <tr v-else-if="errorMessage">
                      <td colspan="6" class="text-center py-4">
                        <div class="alert alert-danger mb-0">{{ errorMessage }}</div>
                      </td>
                    </tr>
                    <tr v-else-if="leaderboardData.length === 0">
                      <td colspan="6" class="text-center py-4 text-muted">
                        No RWA data available
                      </td>
                    </tr>
                    <tr v-else v-for="rwa in leaderboardData" :key="rwa.rwa_id">
                      <td><span :class="getRankBadgeClass(rwa.rank)">{{ rwa.rank }}</span></td>
                      <td><strong>{{ rwa.rwa_name }}</strong></td>
                      <td>{{ rwa.points }}</td>
                      <td>{{ Math.round(rwa.points / 20) }} KG</td>
                      <td>{{ Math.round((rwa.points / 20) / (rwa.points / 20 + 10) * 100) }}%</td>
                      <td><span :class="`badge ${getStatusBadge(rwa.rank).class}`">{{ rwa.remarks || getStatusBadge(rwa.rank).text }}</span></td>
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
import { useAuthStore } from '@/stores/auth';
import api from '@/services/api';

const authStore = useAuthStore();
const loading = ref(true);
const errorMessage = ref('');
const leaderboardData = ref([]);
const userRwaRank = ref(null);
const userRwaPoints = ref(0);

const totalRwas = computed(() => leaderboardData.value.length);

const fetchRwaLeaderboard = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';
    const response = await api.get('/secondary/rwa-leaderboard');
    leaderboardData.value = response.data.leaderboard || [];
    
    // Find user's RWA rank (if they have an RWA membership)
    // This would require additional backend endpoint or data
    // For now, we'll use the first RWA as placeholder
    if (leaderboardData.value.length > 0) {
      userRwaRank.value = leaderboardData.value[0].rank || 1;
      userRwaPoints.value = leaderboardData.value[0].points || 0;
    }
  } catch (error) {
    console.error('Error fetching RWA leaderboard:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to load RWA leaderboard. Please try again.';
    leaderboardData.value = [];
  } finally {
    loading.value = false;
  }
};

const getRankBadgeClass = (rank) => {
  if (rank === 1) return 'badge bg-warning text-dark';
  if (rank <= 3) return 'badge bg-secondary';
  return 'badge bg-secondary';
};

const getStatusBadge = (rank) => {
  if (rank === 1) return { class: 'bg-success', text: 'Leader' };
  if (rank <= 3) return { class: 'bg-info', text: 'Top Performer' };
  if (rank <= 10) return { class: 'bg-info', text: 'Active' };
  return { class: 'bg-info', text: 'Active' };
};

onMounted(() => {
  fetchRwaLeaderboard();
});
</script>

<style scoped>
.secondary-rwa-leaderboard {
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
</style>
