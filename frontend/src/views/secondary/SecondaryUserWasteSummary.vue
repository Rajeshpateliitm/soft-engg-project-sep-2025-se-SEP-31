<template>
  <div class="household-performance-summary">
    <div class="container-fluid px-4 py-4">
      <!-- Title -->
      <div class="row mb-4">
        <div class="col-12 text-center">
          <h1 class="page-title">MONTHLY HOUSEHOLD PERFORMANCE SUMMARY</h1>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3 text-muted">Loading household performance data...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="errorMessage" class="alert alert-danger" role="alert">
        {{ errorMessage }}
      </div>

      <!-- Content -->
      <div v-else>
        <!-- Summary Cards -->
        <div class="row mb-4">
          <div class="col-md-4 mb-3">
            <div class="summary-card">
              <div class="summary-card-label">TOTAL HOUSEHOLDS</div>
              <div class="summary-card-value">{{ wasteData.total_households }}</div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="summary-card">
              <div class="summary-card-label">OVERALL SEGREGATION RATE %</div>
              <div class="summary-card-value">{{ wasteData.segregation_rate }}%</div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="summary-card">
              <div class="summary-card-label">RECYCLE/REUSE/DONATION %</div>
              <div class="summary-card-value">{{ wasteData.recycle_reuse_donations_rate }}%</div>
            </div>
          </div>
        </div>

        <!-- Detailed Performance Table -->
        <div class="row">
          <div class="col-12">
            <div class="table-wrapper">
              <div class="table-container">
                <table class="performance-table">
                  <thead>
                    <tr>
                      <th class="col-hh-number">HH Number</th>
                      <th class="col-family-size">Family Size</th>
                      <th class="col-segregation">Segregation %</th>
                      <th class="col-wet">Wet (kg/day)</th>
                      <th class="col-dry">Dry (kg/day)</th>
                      <th class="col-hazardous">Hazardous (kg/day)</th>
                      <th class="col-recycle">Recycle/Reuse %</th>
                      <th class="col-engagement">Engagement Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="wasteData.household_details.length === 0">
                      <td colspan="8" class="text-center py-4 text-muted">
                        No household data available
                      </td>
                    </tr>
                    <tr v-else v-for="household in wasteData.household_details" :key="household.user_id">
                      <td class="col-hh-number">{{ household.household_number }}</td>
                      <td class="col-family-size">{{ household.family_size }}</td>
                      <td class="col-segregation">{{ household.segregation_percentage }}%</td>
                      <td class="col-wet">{{ formatDecimal(household.per_capita_wet) }}</td>
                      <td class="col-dry">{{ formatDecimal(household.per_capita_dry) }}</td>
                      <td class="col-hazardous">{{ formatDecimal(household.per_capita_hazardous) }}</td>
                      <td class="col-recycle">{{ household.recycle_reuse_donation_percentage }}%</td>
                      <td class="col-engagement">{{ household.engagement_score }}</td>
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
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const loading = ref(true);
const errorMessage = ref('');
const wasteData = ref({
  total_households: 0,
  segregation_rate: 0,
  recycle_reuse_donations_rate: 0,
  household_details: []
});

const formatDecimal = (value) => {
  if (value === null || value === undefined) return '0.00';
  const num = typeof value === 'number' ? value : parseFloat(value);
  return isNaN(num) ? '0.00' : num.toFixed(2);
};

const fetchWasteSummary = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';
    const response = await api.get('/secondary/waste-summary');
    wasteData.value = response.data;
    console.log('Waste summary data:', wasteData.value);
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
.household-performance-summary {
  min-height: 100vh;
  background: #ffffff;
  padding: 2rem 0;
  position: relative;
  overflow: hidden;
}

/* Decorative curved borders at bottom corners */
.household-performance-summary::before,
.household-performance-summary::after {
  content: '';
  position: absolute;
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border-radius: 50%;
  opacity: 0.3;
  z-index: 0;
}

.household-performance-summary::before {
  bottom: -100px;
  left: -100px;
}

.household-performance-summary::after {
  bottom: -100px;
  right: -100px;
}

.household-performance-summary > .container-fluid {
  position: relative;
  z-index: 1;
  max-width: 100%;
  padding-left: 1rem;
  padding-right: 1rem;
}

/* Title Styling */
.page-title {
  font-size: 2rem;
  font-weight: bold;
  color: #dc3545;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 2rem;
  text-align: center;
}

/* Summary Cards */
.summary-card {
  border: 1px solid #d1d1d1;
  border-radius: 8px;
  padding: 1.5rem;
  background: #ffffff;
  text-align: center;
  min-height: 140px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.2s;
}

.summary-card:hover {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12);
}

.summary-card-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #dc3545;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  line-height: 1.3;
}

.summary-card-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333333;
  line-height: 1.2;
}

/* Table Wrapper - handles horizontal scrolling when needed */
.table-wrapper {
  width: 100%;
  overflow-x: auto;
  overflow-y: visible;
  -webkit-overflow-scrolling: touch;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Hide scrollbar but keep functionality */
.table-wrapper::-webkit-scrollbar {
  height: 8px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Table Container */
.table-container {
  width: 100%;
  background: #ffffff;
}

.performance-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  background: #ffffff;
}

.performance-table thead {
  background: #6c757d;
  color: #ffffff;
}

.performance-table th {
  padding: 0.65rem 0.4rem;
  font-weight: 600;
  font-size: 0.75rem;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  border-bottom: 2px solid #495057;
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  color: #ffffff;
  white-space: normal;
  word-wrap: break-word;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
}

.performance-table th:last-child {
  border-right: none;
}

/* Column-specific widths for optimal fit - percentages for flexible layout */
/* Total equals 100% (12.5% * 8 = 100%) */
.performance-table .col-hh-number {
  width: 12.5%;
}

.performance-table .col-family-size {
  width: 12.5%;
}

.performance-table .col-segregation {
  width: 12.5%;
}

.performance-table .col-wet {
  width: 12.5%;
}

.performance-table .col-dry {
  width: 12.5%;
}

.performance-table .col-hazardous {
  width: 12.5%;
}

.performance-table .col-recycle {
  width: 12.5%;
}

.performance-table .col-engagement {
  width: 12.5%;
}

.performance-table tbody {
  background: #ffffff;
}

.performance-table tbody tr {
  background: #ffffff;
  border-bottom: 1px solid #dee2e6;
  transition: background-color 0.2s;
}

.performance-table tbody tr:hover {
  background: #f8f9fa;
}

.performance-table tbody tr:nth-child(even) {
  background: #f8f9fa;
}

.performance-table tbody tr:nth-child(even):hover {
  background: #e9ecef;
}

.performance-table td {
  padding: 0.65rem 0.4rem;
  font-size: 0.85rem;
  color: #333333;
  border-right: 1px solid #dee2e6;
  background: inherit;
  white-space: normal;
  text-align: center;
  word-wrap: break-word;
  overflow: hidden;
  text-overflow: ellipsis;
}

.performance-table td:last-child {
  border-right: none;
}

/* Responsive Design */
@media (max-width: 1400px) {
  .performance-table th {
    font-size: 0.7rem;
    padding: 0.6rem 0.35rem;
  }
  
  .performance-table td {
    font-size: 0.8rem;
    padding: 0.6rem 0.35rem;
  }
}

@media (max-width: 992px) {
  .performance-table th {
    font-size: 0.65rem;
    padding: 0.55rem 0.3rem;
    line-height: 1.1;
  }
  
  .performance-table td {
    font-size: 0.75rem;
    padding: 0.55rem 0.3rem;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 1.5rem;
  }

  .summary-card {
    min-height: 120px;
    padding: 1rem;
  }

  .summary-card-label {
    font-size: 0.8rem;
  }

  .summary-card-value {
    font-size: 2rem;
  }

  /* On smaller screens, allow horizontal scroll if needed */
  .table-wrapper {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  /* Switch to auto layout on very small screens to prevent breaking */
  .performance-table {
    table-layout: auto;
    min-width: 800px;
  }

  .performance-table th {
    font-size: 0.65rem;
    padding: 0.5rem 0.3rem;
    white-space: nowrap;
  }

  .performance-table td {
    font-size: 0.7rem;
    padding: 0.5rem 0.3rem;
    white-space: nowrap;
  }
}

@media (max-width: 576px) {
  .performance-table th {
    font-size: 0.6rem;
    padding: 0.45rem 0.25rem;
    line-height: 1.1;
  }

  .performance-table td {
    font-size: 0.65rem;
    padding: 0.45rem 0.25rem;
  }
}

/* Loading and Error States */
.alert {
  margin: 2rem 0;
  border-radius: 8px;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>
