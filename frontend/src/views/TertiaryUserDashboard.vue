<template>
  <div class="tertiary-dashboard">
    <!-- Header with Tertiary Label -->
    <!-- <div class="tertiary-header mb-4">
      <div class="tertiary-badge">Tertiary</div>
    </div> -->

    <div class="container-fluid">
      <!-- Navigation Bar -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="navbar-section">
  <div class="nav-left">
    <router-link 
      to="/tertiary-dashboard" 
      class="navbar-brand d-flex align-items-center brand-container"
    >
      <img 
        src="@/assets/waste-wise-seeklogo.png"
        alt="WasteWise Logo"
        class="logo-img"
      />  
      <span class="brand-text">WASTEWISE</span>
    </router-link>
  </div>

  <div class="nav-right">
    <span class="nav-item logout" @click="handleLogout">LOGOUT</span>
  </div>
</div>

        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="row">
        <div class="col-12 text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-3 text-muted">Loading dashboard data...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="errorMessage" class="row">
        <div class="col-12">
          <div class="alert alert-danger" role="alert">
            <h4 class="alert-heading">Error</h4>
            <p>{{ errorMessage }}</p>
            <button class="btn btn-primary" @click="fetchDashboardData">Retry</button>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div v-else class="row">
        <div class="col-12">
          <div class="card shadow-lg">
            <div class="card-body p-4">
              <!-- Title -->
              <h3 class="section-title mb-4">WARD WISE PERFORMANCE SUMMARY</h3>

              <!-- Performance Table -->
              <div class="table-responsive">
                <table class="performance-table">
                  <thead>
                    <tr>
                      <th>Ward No.</th>
                      <th>Total Households</th>
                      <th>Avg. Wet Waste (kg/day)</th>
                      <th>Avg. Dry Waste (kg/day)</th>
                      <th>Avg. Hazardous Waste (kg/day)</th>
                      <th>Segregation Compliance (%)</th>
                      <th>Remarks / Action Needed</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="wardData.length === 0">
                      <td colspan="7" class="text-center text-muted py-4">
                        No wards found. Please ensure there are active wards in the system.
                      </td>
                    </tr>
                    <tr v-for="ward in sortedWardData" :key="ward.id" :class="{ 'no-data-row': ward.totalHouseholds === 0 }">
                      <td class="ward-name">
                        <strong>{{ ward.wardNo }}</strong>
                        <span v-if="ward.pincode" class="text-muted small d-block">Pincode: {{ ward.pincode }}</span>
                      </td>
                      <td class="text-center">
                        <span :class="{ 'text-muted': ward.totalHouseholds === 0 }">
                          {{ ward.totalHouseholds }}
                        </span>
                      </td>
                      <td class="text-center">
                        <span :class="{ 'text-muted': ward.totalHouseholds === 0 }">
                          {{ ward.avgWetWaste }}
                        </span>
                      </td>
                      <td class="text-center">
                        <span :class="{ 'text-muted': ward.totalHouseholds === 0 }">
                          {{ ward.avgDryWaste }}
                        </span>
                      </td>
                      <td class="text-center">
                        <span :class="{ 'text-muted': ward.totalHouseholds === 0 }">
                          {{ ward.avgHazardousWaste }}
                        </span>
                      </td>
                      <td class="text-center">
                        <span v-if="ward.totalHouseholds > 0" :class="getComplianceBadgeClass(ward.segregationCompliance)">
                          {{ ward.segregationCompliance }}
                        </span>
                        <span v-else class="text-muted">-</span>
                      </td>
                      <td class="remarks">
                        <span :class="{ 'text-muted font-italic': ward.totalHouseholds === 0 }">
                          {{ ward.remarks }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Summary Statistics -->
              <div class="row mt-5">
                <div class="col-md-6">
                  <div class="summary-card">
                    <h5 class="summary-title">Overall Statistics</h5>
                    <div class="stat-item">
                      <span class="stat-label">Total Wards:</span>
                      <span class="stat-value">{{ totalWards }}</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-label">Total Households:</span>
                      <span class="stat-value">{{ totalHouseholds }}</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-label">Average Segregation Compliance:</span>
                      <span class="stat-value">{{ averageCompliance }}%</span>
                    </div>
                  </div>
                </div>

                <div class="col-md-6">
                  <div class="summary-card">
                    <h5 class="summary-title">Daily Waste Collection</h5>
                    <div class="stat-item">
                      <span class="stat-label">Total Wet Waste:</span>
                      <span class="stat-value">{{ formatNumber(totalWetWaste) }} kg</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-label">Total Dry Waste:</span>
                      <span class="stat-value">{{ formatNumber(totalDryWaste) }} kg</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-label">Total Hazardous Waste:</span>
                      <span class="stat-value">{{ formatNumber(totalHazardousWaste) }} kg</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Performance Indicators -->
              <div class="row mt-4">
                <div class="col-12">
                  <h5 class="section-subtitle mb-3">Performance Indicators</h5>
                  <div class="row">
                    <div class="col-md-4 mb-3">
                      <div class="indicator-card excellent">
                        <div class="indicator-icon">
                          <i class="bi bi-star-fill"></i>
                        </div>
                        <div class="indicator-content">
                          <div class="indicator-label">Excellent Performance</div>
                          <div class="indicator-count">{{ dashboardData.excellentCount || 0 }} Wards</div>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-4 mb-3">
                      <div class="indicator-card good">
                        <div class="indicator-icon">
                          <i class="bi bi-hand-thumbs-up"></i>
                        </div>
                        <div class="indicator-content">
                          <div class="indicator-label">Good Performance</div>
                          <div class="indicator-count">{{ dashboardData.goodCount || 0 }} Wards</div>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-4 mb-3">
                      <div class="indicator-card needsImprovement">
                        <div class="indicator-icon">
                          <i class="bi bi-exclamation-triangle"></i>
                        </div>
                        <div class="indicator-content">
                          <div class="indicator-label">Needs Improvement</div>
                          <div class="indicator-count">{{ dashboardData.needsImprovementCount || 0 }} Wards</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Action Items -->
              <div class="row mt-4">
                <div class="col-12">
                  <h5 class="section-subtitle mb-3">Priority Action Items</h5>
                  <div class="action-items" v-if="dashboardData.priorityActions && dashboardData.priorityActions.length > 0">
                    <div v-for="(action, index) in dashboardData.priorityActions" :key="index" class="action-item">
                      <div class="action-number">{{ index + 1 }}</div>
                      <div class="action-content">
                        <div class="action-ward">{{ action.ward }}</div>
                        <div class="action-description">{{ action.description }}</div>
                      </div>
                      <div class="action-priority" :class="action.priority.toLowerCase()">
                        {{ action.priority }}
                      </div>
                    </div>
                  </div>
                  <div v-else class="text-muted py-3">
                    No priority actions at this time.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';

const router = useRouter();
const authStore = useAuthStore();

// Dashboard data
const loading = ref(true);
const errorMessage = ref('');
const dashboardData = ref({
  wardData: [],
  totalWards: 0,
  totalHouseholds: 0,
  averageCompliance: 0,
  totalWetWaste: 0,
  totalDryWaste: 0,
  totalHazardousWaste: 0,
  excellentCount: 0,
  goodCount: 0,
  needsImprovementCount: 0,
  priorityActions: []
});

// Computed properties
const wardData = computed(() => dashboardData.value.wardData || []);
const totalWards = computed(() => dashboardData.value.totalWards || 0);
const totalHouseholds = computed(() => dashboardData.value.totalHouseholds || 0);
const averageCompliance = computed(() => dashboardData.value.averageCompliance || 0);
const totalWetWaste = computed(() => dashboardData.value.totalWetWaste || 0);
const totalDryWaste = computed(() => dashboardData.value.totalDryWaste || 0);
const totalHazardousWaste = computed(() => dashboardData.value.totalHazardousWaste || 0);

// Sort wards by ward number (extract numeric part for proper sorting)
const sortedWardData = computed(() => {
  const sorted = [...wardData.value].sort((a, b) => {
    // Extract ward number from wardNo (e.g., "Ward 1" -> 1)
    const getWardNumber = (ward) => {
      const match = ward.wardNumber ? ward.wardNumber.match(/\d+/) : ward.wardNo.match(/\d+/);
      return match ? parseInt(match[0], 10) : 0;
    };
    return getWardNumber(a) - getWardNumber(b);
  });
  return sorted;
});

// Fetch dashboard data
const fetchDashboardData = async () => {
  loading.value = true;
  errorMessage.value = '';
  
  try {
    const response = await api.get('/tertiary/dashboard');
    dashboardData.value = response.data;
    console.log('Dashboard data received:', response.data);
    console.log('Ward data:', response.data.wardData);
    if (response.data.wardData && response.data.wardData.length > 0) {
      console.log('First ward sample:', response.data.wardData[0]);
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to load dashboard data. Please try again.';
  } finally {
    loading.value = false;
  }
};

// Handle logout
const handleLogout = () => {
  authStore.logout();
  router.push('/signin');
};

// Format number with commas
const formatNumber = (num) => {
  return num.toLocaleString('en-US');
};

// Get compliance badge class
const getComplianceBadgeClass = (compliance) => {
  // Extract numeric value from percentage string (e.g., "88%" -> 88)
  const value = typeof compliance === 'string' 
    ? parseInt(compliance.replace('%', '')) 
    : compliance;
  
  if (value >= 85) return 'compliance-badge excellent';
  if (value >= 70) return 'compliance-badge good';
  return 'compliance-badge needsImprovement';
};

// Fetch data on component mount
onMounted(() => {
  fetchDashboardData();
});
</script>

<style scoped>


.navbar-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Brand container */
.brand-container {
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 14px;          /* spacing between logo & text */
}

/* Logo */
.logo-img {
  height: 46px;
  width: auto;
  object-fit: contain;
  border-radius: 6px;
}

/* Brand text */
.brand-text {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  letter-spacing: 1px;
}

/* Right nav section */
.nav-right .nav-item.logout {
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 6px;
  transition: 0.2s ease;
  background: #f5f5f5;
}

.nav-right .nav-item.logout:hover {
  background: #ff4d4d;
  color: #fff;
}

/* ---------------- DASHBOARD ---------------- */

.tertiary-dashboard {
  padding: 1.5rem;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.tertiary-header {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.tertiary-badge {
  border: 2px solid #0d6efd;
  border-radius: 2rem;
  padding: 0.5rem 1.5rem;
  font-weight: 600;
  color: #0d6efd;
  background-color: white;
  font-size: 1rem;
}

/* Generic nav items */
.nav-left,
.nav-right {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-item {
  font-size: 0.9rem;
  font-weight: 500;
  color: #0d6efd;
  cursor: pointer;
  transition: color 0.3s;
}

.nav-item:hover {
  color: #0b5ed7;
}

.nav-item.logout {
  color: #dc3545;
}

.nav-item.logout:hover {
  color: #bb2d3b;
}

.card {
  border: none;
  border-radius: 0.75rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.section-title {
  color: #dc3545;
  font-weight: 700;
  text-align: center;
  letter-spacing: 1px;
  margin-bottom: 2rem;
}

.section-subtitle {
  color: #2c3e50;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.table-responsive {
  border-radius: 0.5rem;
  overflow: hidden;
}


.table-responsive {
  border-radius: 0.5rem;
  overflow: hidden;
}

.performance-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
}

.performance-table thead {
  background-color: #4a4a4a;
  color: white;
}

.performance-table thead th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.9rem;
  border: 1px solid #3a3a3a;
}

.performance-table tbody tr {
  border-bottom: 1px solid #e9ecef;
  transition: background-color 0.2s;
}

.performance-table tbody tr:hover {
  background-color: #f8f9fa;
}

.performance-table tbody tr.no-data-row {
  opacity: 0.7;
}

.performance-table tbody tr.no-data-row:hover {
  background-color: #f0f0f0;
}

.performance-table tbody td {
  padding: 1rem;
  font-size: 0.95rem;
  border: 1px solid #e9ecef;
}

.ward-name {
  font-weight: 600;
  color: #2c3e50;
}

.remarks {
  font-size: 0.85rem;
  color: #6c757d;
  max-width: 300px;
}

.text-center {
  text-align: center;
}

.compliance-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 0.25rem;
  font-weight: 600;
  font-size: 0.85rem;
}

.compliance-badge.excellent {
  background-color: #d4edda;
  color: #155724;
}

.compliance-badge.good {
  background-color: #cfe2ff;
  color: #084298;
}

.compliance-badge.needsImprovement {
  background-color: #f8d7da;
  color: #842029;
}

.summary-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.summary-title {
  font-weight: 700;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  font-weight: 500;
  font-size: 0.95rem;
}

.stat-value {
  font-weight: 700;
  font-size: 1.1rem;
}

.indicator-card {
  padding: 1.5rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.indicator-card:hover {
  transform: translateY(-5px);
}

.indicator-card.excellent {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.indicator-card.good {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.indicator-card.needsImprovement {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: white;
}

.indicator-icon {
  font-size: 2rem;
  opacity: 0.8;
}

.indicator-content {
  flex: 1;
}

.indicator-label {
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}

.indicator-count {
  font-weight: 700;
  font-size: 1.5rem;
}

.action-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-left: 4px solid #0d6efd;
  border-radius: 0.5rem;
  transition: all 0.3s;
}

.action-item:hover {
  background-color: #e7f3ff;
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
}

.action-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  background-color: #0d6efd;
  color: white;
  border-radius: 50%;
  font-weight: 700;
  flex-shrink: 0;
}

.action-content {
  flex: 1;
}

.action-ward {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.action-description {
  font-size: 0.9rem;
  color: #6c757d;
}

.action-priority {
  padding: 0.4rem 0.8rem;
  border-radius: 0.25rem;
  font-weight: 600;
  font-size: 0.85rem;
  flex-shrink: 0;
}

.action-priority.high {
  background-color: #f8d7da;
  color: #842029;
}

.action-priority.medium {
  background-color: #fff3cd;
  color: #664d03;
}

.action-priority.low {
  background-color: #d1ecf1;
  color: #0c5460;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .tertiary-dashboard {
    padding: 1rem;
  }

  .nav-left,
  .nav-right {
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
  }

  .logo-img {
    height: 36px;
  }

  .brand-text {
    font-size: 1.6rem;
    letter-spacing: 0.6px;
  }

  .navbar-section {
    padding: 10px 16px;
  }

  .performance-table thead th,
  .performance-table tbody td {
    padding: 0.75rem 0.5rem;
    font-size: 0.85rem;
  }

  .remarks {
    max-width: 200px;
  }

  .summary-card {
    margin-bottom: 1rem;
  }

  .indicator-card {
    flex-direction: column;
    text-align: center;
  }

  .action-item {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
