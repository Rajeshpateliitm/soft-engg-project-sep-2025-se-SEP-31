<template>
  <div class="pickup-summary-container">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex align-items-center mb-3">
            <button class="btn btn-link text-white p-0 me-2" @click="goBack">
              <i class="bi bi-arrow-left" style="font-size: 1.5rem;"></i>
            </button>
            <h2 class="text-white fw-bold mb-0">MONTHLY WASTE PICKUP SUMMARY</h2>
          </div>
          <p class="text-white-50">Comprehensive statistics about waste pickups for the current month</p>
        </div>
      </div>

      <!-- Statistics Cards -->
      <div class="row mb-4">
        <div class="col-md-6 col-lg-3 mb-3">
          <div class="stat-card">
            <div class="stat-label">TOTAL INCOMING PICKUPS</div>
            <div class="stat-value">320</div>
            <div class="stat-icon">
              <i class="bi bi-arrow-down-circle"></i>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3 mb-3">
          <div class="stat-card">
            <div class="stat-label">TOTAL PICKUPS COMPLETED</div>
            <div class="stat-value">260</div>
            <div class="stat-icon">
              <i class="bi bi-check-circle"></i>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3 mb-3">
          <div class="stat-card">
            <div class="stat-label">TOTAL PENDING PICKUPS</div>
            <div class="stat-value">16</div>
            <div class="stat-icon">
              <i class="bi bi-clock-history"></i>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3 mb-3">
          <div class="stat-card">
            <div class="stat-label">TOTAL REJECTED PICKUPS</div>
            <div class="stat-value">44</div>
            <div class="stat-icon">
              <i class="bi bi-x-circle"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- Chart Section -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">Daily Pick-ups by Status (Last 30 Days)</h5>
              <button class="btn btn-sm btn-light" @click="exportData">
                <i class="bi bi-download me-1"></i>Export Data
              </button>
            </div>
            <div class="card-body">
              <div class="chart-container">
                <canvas id="pickupChart"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Waste Type Breakdown -->
      <div class="row mb-4">
        <div class="col-lg-6 mb-3">
          <div class="card shadow-lg">
            <div class="card-header bg-info text-white">
              <h5 class="card-title mb-0">Waste Type Distribution</h5>
            </div>
            <div class="card-body">
              <div class="waste-type-item">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="waste-label">Organic Waste</span>
                  <span class="waste-percentage">35%</span>
                </div>
                <div class="progress" style="height: 8px;">
                  <div class="progress-bar bg-success" style="width: 35%"></div>
                </div>
              </div>
              <div class="waste-type-item">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="waste-label">Recyclable Waste</span>
                  <span class="waste-percentage">28%</span>
                </div>
                <div class="progress" style="height: 8px;">
                  <div class="progress-bar bg-info" style="width: 28%"></div>
                </div>
              </div>
              <div class="waste-type-item">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="waste-label">Hazardous Waste</span>
                  <span class="waste-percentage">12%</span>
                </div>
                <div class="progress" style="height: 8px;">
                  <div class="progress-bar bg-warning" style="width: 12%"></div>
                </div>
              </div>
              <div class="waste-type-item">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="waste-label">Bulk Waste</span>
                  <span class="waste-percentage">18%</span>
                </div>
                <div class="progress" style="height: 8px;">
                  <div class="progress-bar bg-danger" style="width: 18%"></div>
                </div>
              </div>
              <div class="waste-type-item">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="waste-label">E-Waste</span>
                  <span class="waste-percentage">7%</span>
                </div>
                <div class="progress" style="height: 8px;">
                  <div class="progress-bar bg-secondary" style="width: 7%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Monthly Statistics Table -->
        <div class="col-lg-6 mb-3">
          <div class="card shadow-lg">
            <div class="card-header bg-success text-white">
              <h5 class="card-title mb-0">Monthly Statistics</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-sm">
                  <tbody>
                    <tr>
                      <td><strong>Total Waste Collected</strong></td>
                      <td class="text-end"><strong>2,450 KG</strong></td>
                    </tr>
                    <tr>
                      <td>Average Daily Pickup</td>
                      <td class="text-end">81.67 KG</td>
                    </tr>
                    <tr>
                      <td>Peak Pickup Day</td>
                      <td class="text-end">Day 15 (145 KG)</td>
                    </tr>
                    <tr>
                      <td>Lowest Pickup Day</td>
                      <td class="text-end">Day 8 (35 KG)</td>
                    </tr>
                    <tr>
                      <td><strong>Completion Rate</strong></td>
                      <td class="text-end"><strong>81.25%</strong></td>
                    </tr>
                    <tr>
                      <td>Rejection Rate</td>
                      <td class="text-end">13.75%</td>
                    </tr>
                    <tr>
                      <td>Pending Rate</td>
                      <td class="text-end">5%</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Detailed Breakdown Table -->
      <div class="row">
        <div class="col-12">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white">
              <h5 class="card-title mb-0">Detailed Pickup Breakdown by Date</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th>Date</th>
                      <th>Scheduled</th>
                      <th>Completed</th>
                      <th>Pending</th>
                      <th>Rejected</th>
                      <th>Total Waste (KG)</th>
                      <th>Completion %</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(day, index) in dailyBreakdown" :key="index">
                      <td><strong>{{ day.date }}</strong></td>
                      <td>{{ day.scheduled }}</td>
                      <td><span class="badge bg-success">{{ day.completed }}</span></td>
                      <td><span class="badge bg-warning">{{ day.pending }}</span></td>
                      <td><span class="badge bg-danger">{{ day.rejected }}</span></td>
                      <td>{{ day.waste }}</td>
                      <td>
                        <div class="progress" style="height: 20px;">
                          <div class="progress-bar" :style="{ width: day.completion + '%' }">
                            {{ day.completion }}%
                          </div>
                        </div>
                      </td>
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
import { useRouter } from 'vue-router';

const router = useRouter();

const dailyBreakdown = ref([
  { date: 'Day 1', scheduled: 12, completed: 10, pending: 1, rejected: 1, waste: '85 KG', completion: 83 },
  { date: 'Day 2', scheduled: 11, completed: 9, pending: 1, rejected: 1, waste: '72 KG', completion: 82 },
  { date: 'Day 3', scheduled: 13, completed: 11, pending: 1, rejected: 1, waste: '95 KG', completion: 85 },
  { date: 'Day 4', scheduled: 10, completed: 8, pending: 1, rejected: 1, waste: '68 KG', completion: 80 },
  { date: 'Day 5', scheduled: 12, completed: 10, pending: 1, rejected: 1, waste: '88 KG', completion: 83 },
  { date: 'Day 6', scheduled: 11, completed: 9, pending: 1, rejected: 1, waste: '75 KG', completion: 82 },
  { date: 'Day 7', scheduled: 9, completed: 7, pending: 1, rejected: 1, waste: '58 KG', completion: 78 },
  { date: 'Day 8', scheduled: 8, completed: 6, pending: 1, rejected: 1, waste: '35 KG', completion: 75 },
  { date: 'Day 9', scheduled: 12, completed: 10, pending: 1, rejected: 1, waste: '92 KG', completion: 83 },
  { date: 'Day 10', scheduled: 13, completed: 11, pending: 1, rejected: 1, waste: '105 KG', completion: 85 },
]);

const goBack = () => {
  router.push('/secondary-dashboard/pickup-details');
};

const exportData = () => {
  alert('Exporting pickup summary data...');
  // Add export functionality here
};

onMounted(() => {
  // Initialize chart if needed
  console.log('Pickup Summary page loaded');
});
</script>

<style scoped>
.pickup-summary-container {
  padding: 1.5rem;
  min-height: 100vh;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card:nth-child(2) {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-card:nth-child(3) {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-card:nth-child(4) {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-label {
  font-size: 0.85rem;
  font-weight: 600;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.stat-icon {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 2rem;
  opacity: 0.3;
}

.card {
  border: none;
  border-radius: 0.75rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.card-header {
  border-bottom: none;
  border-radius: 0.75rem 0.75rem 0 0 !important;
}

.chart-container {
  position: relative;
  height: 400px;
  margin-bottom: 1rem;
}

.waste-type-item {
  margin-bottom: 1.5rem;
}

.waste-label {
  font-weight: 500;
  color: #2c3e50;
}

.waste-percentage {
  font-weight: 600;
  color: #667eea;
}

.table {
  margin-bottom: 0;
}

.table-hover tbody tr:hover {
  background-color: #f8f9fa;
}

.progress {
  background-color: #e9ecef;
  border-radius: 0.25rem;
}

.progress-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.75rem;
}

.badge {
  padding: 0.4rem 0.6rem;
  font-size: 0.8rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .pickup-summary-container {
    padding: 1rem;
  }

  .stat-value {
    font-size: 2rem;
  }

  .chart-container {
    height: 300px;
  }

  .table {
    font-size: 0.9rem;
  }
}
</style>
