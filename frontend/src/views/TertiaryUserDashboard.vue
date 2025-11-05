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
              <span class="nav-item active">DASHBOARD</span>
            </div>
            <div class="nav-right">
              <!-- <span class="nav-item">&lt;&lt;&gt;&gt;</span>
              <span class="nav-item">&lt;&lt;&gt;&gt;</span> -->
              <span class="nav-item logout">LOGOUT</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="row">
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
                    <tr v-for="ward in wardData" :key="ward.id">
                      <td class="ward-name"><strong>{{ ward.wardNo }}</strong></td>
                      <td class="text-center">{{ ward.totalHouseholds }}</td>
                      <td class="text-center">{{ ward.avgWetWaste }}</td>
                      <td class="text-center">{{ ward.avgDryWaste }}</td>
                      <td class="text-center">{{ ward.avgHazardousWaste }}</td>
                      <td class="text-center">
                        <span :class="getComplianceBadgeClass(ward.segregationCompliance)">
                          {{ ward.segregationCompliance }}
                        </span>
                      </td>
                      <td class="remarks">{{ ward.remarks }}</td>
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
                      <span class="stat-value">{{ wardData.length }}</span>
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
                      <span class="stat-value">{{ totalWetWaste }} kg</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-label">Total Dry Waste:</span>
                      <span class="stat-value">{{ totalDryWaste }} kg</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-label">Total Hazardous Waste:</span>
                      <span class="stat-value">{{ totalHazardousWaste }} kg</span>
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
                          <div class="indicator-count">{{ excellentCount }} Wards</div>
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
                          <div class="indicator-count">{{ goodCount }} Wards</div>
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
                          <div class="indicator-count">{{ needsImprovementCount }} Wards</div>
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
                  <div class="action-items">
                    <div v-for="(action, index) in priorityActions" :key="index" class="action-item">
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
import { ref, computed } from 'vue';

const wardData = ref([
  {
    id: 1,
    wardNo: 'Ward 1 - Park Street',
    totalHouseholds: 1200,
    avgWetWaste: '1,850 kg',
    avgDryWaste: '940 kg',
    avgHazardousWaste: '60 kg',
    segregationCompliance: '88%',
    remarks: 'Good segregation; increase composting outreach'
  },
  {
    id: 2,
    wardNo: 'Ward 2 - Ballygunge',
    totalHouseholds: 1000,
    avgWetWaste: '2,100 kg',
    avgDryWaste: '710 kg',
    avgHazardousWaste: '110 kg',
    segregationCompliance: '61%',
    remarks: 'Low segregation; run awareness campaign'
  },
  {
    id: 3,
    wardNo: 'Ward 3 - Behala South',
    totalHouseholds: 1500,
    avgWetWaste: '1,970 kg',
    avgDryWaste: '810 kg',
    avgHazardousWaste: '95 kg',
    segregationCompliance: '73%',
    remarks: 'Moderate performance; improve dry waste recovery'
  },
  {
    id: 4,
    wardNo: 'Ward 4 - Gum Dum',
    totalHouseholds: 980,
    avgWetWaste: '2,250 kg',
    avgDryWaste: '600 kg',
    avgHazardousWaste: '140 kg',
    segregationCompliance: '54%',
    remarks: 'High wet load; train collectors on waste segregation'
  },
  {
    id: 5,
    wardNo: 'Ward 5 - New Town',
    totalHouseholds: 1400,
    avgWetWaste: '1,620 kg',
    avgDryWaste: '1,020 kg',
    avgHazardousWaste: '55 kg',
    segregationCompliance: '91%',
    remarks: 'Model ward; showcase composting and recycling'
  }
]);

const totalHouseholds = computed(() => {
  return wardData.value.reduce((sum, ward) => sum + ward.totalHouseholds, 0);
});

const totalWetWaste = computed(() => {
  return wardData.value.reduce((sum, ward) => {
    const value = parseInt(ward.avgWetWaste.replace(/,/g, ''));
    return sum + value;
  }, 0);
});

const totalDryWaste = computed(() => {
  return wardData.value.reduce((sum, ward) => {
    const value = parseInt(ward.avgDryWaste.replace(/,/g, ''));
    return sum + value;
  }, 0);
});

const totalHazardousWaste = computed(() => {
  return wardData.value.reduce((sum, ward) => {
    const value = parseInt(ward.avgHazardousWaste.replace(/,/g, ''));
    return sum + value;
  }, 0);
});

const averageCompliance = computed(() => {
  const total = wardData.value.reduce((sum, ward) => {
    const value = parseInt(ward.segregationCompliance);
    return sum + value;
  }, 0);
  return Math.round(total / wardData.value.length);
});

const excellentCount = computed(() => {
  return wardData.value.filter(ward => {
    const compliance = parseInt(ward.segregationCompliance);
    return compliance >= 85;
  }).length;
});

const goodCount = computed(() => {
  return wardData.value.filter(ward => {
    const compliance = parseInt(ward.segregationCompliance);
    return compliance >= 70 && compliance < 85;
  }).length;
});

const needsImprovementCount = computed(() => {
  return wardData.value.filter(ward => {
    const compliance = parseInt(ward.segregationCompliance);
    return compliance < 70;
  }).length;
});

const priorityActions = ref([
  {
    ward: 'Ward 4 - Gum Dum',
    description: 'High wet load; train collectors on waste segregation',
    priority: 'High'
  },
  {
    ward: 'Ward 2 - Ballygunge',
    description: 'Low segregation; run awareness campaign',
    priority: 'High'
  },
  {
    ward: 'Ward 3 - Behala South',
    description: 'Improve dry waste recovery and recycling initiatives',
    priority: 'Medium'
  },
  {
    ward: 'Ward 1 - Park Street',
    description: 'Increase composting outreach and community engagement',
    priority: 'Medium'
  }
]);

const getComplianceBadgeClass = (compliance) => {
  const value = parseInt(compliance);
  if (value >= 85) return 'compliance-badge excellent';
  if (value >= 70) return 'compliance-badge good';
  return 'compliance-badge needsImprovement';
};
</script>

<style scoped>
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

.navbar-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

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

  .navbar-section {
    flex-direction: column;
    gap: 1rem;
  }

  .nav-left,
  .nav-right {
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
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

  .action-priority {
    align-self: flex-start;
  }
}
</style>
