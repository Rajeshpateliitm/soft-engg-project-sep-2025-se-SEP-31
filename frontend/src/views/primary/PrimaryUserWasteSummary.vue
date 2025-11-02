<template>
  <div class="waste-summary">
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h2 class="mb-1">Waste Summary</h2>
            <p class="text-muted mb-0">Track your waste reduction progress and impact</p>
          </div>
          <div class="d-flex gap-2">
            <select v-model="timeRange" class="form-select form-select-sm" style="width: auto;">
              <option value="weekly">This Week</option>
              <option value="monthly" selected>This Month</option>
              <option value="yearly">This Year</option>
              <option value="all">All Time</option>
            </select>
            <button class="btn btn-sm btn-outline-primary" @click="exportReport">
              <i class="bi bi-download me-1"></i> Export
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="row">
      <div class="col-md-3 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="bg-primary bg-opacity-10 p-3 rounded-3 me-3">
                <i class="bi bi-trash text-primary" style="font-size: 1.5rem;"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Total Waste Logged</h6>
                <h3 class="mb-0">{{ formatNumber(summary.totalWaste) }}<small class="text-muted">kg</small></h3>
                <small class="text-success" v-if="summary.wasteChange > 0">
                  <i class="bi bi-arrow-up"></i> {{ summary.wasteChange }}% from last period
                </small>
                <small class="text-danger" v-else-if="summary.wasteChange < 0">
                  <i class="bi bi-arrow-down"></i> {{ Math.abs(summary.wasteChange) }}% from last period
                </small>
                <small class="text-muted" v-else>No change from last period</small>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="bg-success bg-opacity-10 p-3 rounded-3 me-3">
                <i class="bi bi-recycle text-success" style="font-size: 1.5rem;"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Recycling Rate</h6>
                <h3 class="mb-0">{{ summary.recyclingRate }}<small>%</small></h3>
                <div class="progress mt-2" style="height: 5px;">
                  <div class="progress-bar bg-success" role="progressbar" :style="{ width: summary.recyclingRate + '%' }" 
                       :aria-valuenow="summary.recyclingRate" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="bg-warning bg-opacity-10 p-3 rounded-3 me-3">
                <i class="bi bi-lightbulb text-warning" style="font-size: 1.5rem;"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Carbon Footprint</h6>
                <h3 class="mb-0">{{ formatNumber(summary.carbonFootprint) }}<small class="text-muted">kg CO₂</small></h3>
                <small class="text-success" v-if="summary.carbonChange < 0">
                  <i class="bi bi-arrow-down"></i> {{ Math.abs(summary.carbonChange) }}% reduction
                </small>
                <small class="text-danger" v-else-if="summary.carbonChange > 0">
                  <i class="bi bi-arrow-up"></i> {{ summary.carbonChange }}% increase
                </small>
                <small class="text-muted" v-else>No change from last period</small>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="bg-info bg-opacity-10 p-3 rounded-3 me-3">
                <i class="bi bi-trophy text-info" style="font-size: 1.5rem;"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Waste Reduction</h6>
                <h3 class="mb-0">{{ summary.wasteReduction }}<small>%</small></h3>
                <div class="progress mt-2" style="height: 5px;">
                  <div class="progress-bar bg-info" role="progressbar" :style="{ width: summary.wasteReduction + '%' }" 
                       :aria-valuenow="summary.wasteReduction" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Waste Composition Chart -->
      <div class="col-lg-8 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Waste Composition</h5>
            <div class="btn-group btn-group-sm" role="group">
              <button 
                v-for="tab in chartTabs" 
                :key="tab.id"
                type="button" 
                class="btn"
                :class="activeChartTab === tab.id ? 'btn-primary' : 'btn-outline-secondary'"
                @click="activeChartTab = tab.id"
              >
                {{ tab.label }}
              </button>
            </div>
          </div>
          <div class="card-body">
            <div class="chart-container" style="position: relative; height: 300px;">
              <canvas ref="wasteChart"></canvas>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Waste Categories -->
      <div class="col-lg-4 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <h5 class="mb-0">Waste by Category</h5>
          </div>
          <div class="card-body p-0">
            <div class="list-group list-group-flush">
              <div 
                v-for="(category, index) in wasteCategories" 
                :key="index"
                class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
              >
                <div class="d-flex align-items-center">
                  <div 
                    class="rounded-circle d-flex align-items-center justify-content-center me-3" 
                    :class="'bg-' + category.variant + '-subtle'"
                    style="width: 40px; height: 40px;"
                  >
                    <i :class="'bi ' + category.icon + ' text-' + category.variant + '" style="font-size: 1.25rem;"></i>
                  </div>
                  <div>
                    <h6 class="mb-0">{{ category.name }}</h6>
                    <small class="text-muted">{{ category.percentage }}% of total</small>
                  </div>
                </div>
                <span class="badge rounded-pill" :class="'bg-' + category.variant">{{ category.amount }} kg</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="row">
      <!-- Waste Trends Over Time -->
      <div class="col-lg-6 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <h5 class="mb-0">Waste Trends Over Time</h5>
          </div>
          <div class="card-body">
            <div class="chart-container" style="position: relative; height: 300px;">
              <canvas ref="trendsChart"></canvas>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Waste Disposal Methods -->
      <div class="col-lg-6 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <h5 class="mb-0">Waste Disposal Methods</h5>
          </div>
          <div class="card-body">
            <div class="chart-container" style="position: relative; height: 300px;">
              <canvas ref="disposalChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Recent Waste Logs -->
    <div class="row">
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Recent Waste Logs</h5>
            <router-link to="/primary-dashboard/waste-log" class="btn btn-sm btn-outline-primary">
              View All Logs
            </router-link>
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>Date</th>
                  <th>Waste Type</th>
                  <th>Amount</th>
                  <th>Disposal Method</th>
                  <th class="text-end">Carbon Impact</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(log, index) in recentLogs" :key="index">
                  <td>
                    <div class="text-nowrap">{{ formatDate(log.date) }}</div>
                    <small class="text-muted">{{ formatTime(log.date) }}</small>
                  </td>
                  <td>
                    <div class="d-flex align-items-center">
                      <div 
                        class="rounded-circle d-flex align-items-center justify-content-center me-2" 
                        :class="'bg-' + getWasteType(log.type).variant + '-subtle'"
                        style="width: 32px; height: 32px;"
                      >
                        <i :class="'bi ' + getWasteType(log.type).icon + ' text-' + getWasteType(log.type).variant" style="font-size: 0.875rem;"></i>
                      </div>
                      <span>{{ log.type }}</span>
                    </div>
                  </td>
                  <td>{{ log.amount }} kg</td>
                  <td>
                    <span class="badge" :class="'bg-' + getDisposalMethod(log.method).variant">
                      {{ log.method }}
                    </span>
                  </td>
                  <td class="text-end">
                    <span class="fw-medium">{{ log.carbonImpact }} kg CO₂</span>
                  </td>
                </tr>
                <tr v-if="recentLogs.length === 0">
                  <td colspan="5" class="text-center py-4">
                    <p class="text-muted mb-0">No waste logs found</p>
                    <router-link to="/primary-dashboard/waste-log" class="btn btn-sm btn-primary mt-2">
                      <i class="bi bi-plus-lg me-1"></i> Add Waste Log
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Waste Reduction Tips -->
    <div class="row mt-4">
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-0">
            <h5 class="mb-0">Waste Reduction Tips</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div v-for="(tip, index) in wasteReductionTips" :key="index" class="col-md-6 col-lg-4 mb-4">
                <div class="card h-100 border-0 shadow-sm">
                  <div class="card-body">
                    <div class="d-flex align-items-start">
                      <div class="bg-primary bg-opacity-10 p-2 rounded-3 me-3">
                        <i :class="'bi ' + tip.icon + ' text-primary'" style="font-size: 1.25rem;"></i>
                      </div>
                      <div>
                        <h6 class="mb-1">{{ tip.title }}</h6>
                        <p class="small text-muted mb-0">{{ tip.description }}</p>
                      </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mt-3">
                      <span class="badge bg-light text-dark">
                        <i class="bi bi-lightning-charge text-warning me-1"></i>
                        Saves ~{{ tip.savings }} kg CO₂/month
                      </span>
                      <button class="btn btn-sm btn-link p-0" @click="viewTipDetails(tip)">
                        Learn more <i class="bi bi-arrow-right"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Tip Details Modal -->
    <div v-if="selectedTip" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedTip.title }}</h5>
            <button type="button" class="btn-close" @click="selectedTip = null"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <img :src="selectedTip.image || 'https://source.unsplash.com/random/600x400/?waste,recycling'" 
                     class="img-fluid rounded mb-3" alt="Waste reduction tip">
                <div class="d-flex align-items-center mb-3">
                  <div class="bg-primary bg-opacity-10 p-2 rounded-3 me-3">
                    <i :class="'bi ' + selectedTip.icon + ' text-primary'" style="font-size: 1.5rem;"></i>
                  </div>
                  <div>
                    <h6 class="mb-0">Potential Impact</h6>
                    <p class="mb-0 text-muted">Saves ~{{ selectedTip.savings }} kg CO₂/month</p>
                  </div>
                </div>
                <div class="d-flex align-items-center">
                  <div class="bg-success bg-opacity-10 p-2 rounded-3 me-3">
                    <i class="bi bi-check2-circle text-success" style="font-size: 1.5rem;"></i>
                  </div>
                  <div>
                    <h6 class="mb-0">Difficulty</h6>
                    <div class="d-flex">
                      <i v-for="i in 5" :key="i" 
                         :class="i <= selectedTip.difficulty ? 'bi bi-star-fill text-warning' : 'bi bi-star text-muted'"
                         style="font-size: 0.875rem;">
                      </i>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <h6>How to implement:</h6>
                <ul class="mb-3">
                  <li v-for="(step, index) in selectedTip.steps" :key="index" class="mb-2">
                    {{ step }}
                  </li>
                </ul>
                
                <h6>Benefits:</h6>
                <ul class="mb-3">
                  <li v-for="(benefit, index) in selectedTip.benefits" :key="'benefit-' + index" class="mb-1">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>{{ benefit }}
                  </li>
                </ul>
                
                <div class="alert alert-info mb-0">
                  <i class="bi bi-lightbulb me-2"></i>
                  <strong>Pro Tip:</strong> {{ selectedTip.proTip || 'Start small and gradually increase your efforts for long-term success.' }}
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" @click="selectedTip = null">Close</button>
            <button type="button" class="btn btn-primary" @click="addToActionPlan(selectedTip)">
              <i class="bi bi-plus-lg me-1"></i> Add to Action Plan
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import Chart from 'chart.js/auto';

// Refs
const timeRange = ref('monthly');
const activeChartTab = ref('weight');
const selectedTip = ref(null);
const wasteChart = ref(null);
const trendsChart = ref(null);
const disposalChart = ref(null);

// Chart instances
let wasteChartInstance = null;
let trendsChartInstance = null;
let disposalChartInstance = null;

// Data
const summary = ref({
  totalWaste: 156.8,
  wasteChange: -12.5,
  recyclingRate: 68,
  carbonFootprint: 342.5,
  carbonChange: -8.2,
  wasteReduction: 24,
  lastUpdated: new Date()
});

const chartTabs = [
  { id: 'weight', label: 'By Weight' },
  { id: 'volume', label: 'By Volume' },
  { id: 'impact', label: 'By Impact' }
];

const wasteCategories = ref([
  { id: 1, name: 'Plastic', amount: 45.2, percentage: 29, icon: 'bi-arrow-repeat', variant: 'primary' },
  { id: 2, name: 'Paper', amount: 38.7, percentage: 25, icon: 'bi-file-text', variant: 'info' },
  { id: 3, name: 'Organic', amount: 32.5, percentage: 21, icon: 'bi-egg-fried', variant: 'success' },
  { id: 4, name: 'Glass', amount: 18.3, percentage: 12, icon: 'bi-cup-straw', variant: 'warning' },
  { id: 5, name: 'Metal', amount: 12.8, percentage: 8, icon: 'bi-cup', variant: 'danger' },
  { id: 6, name: 'E-Waste', amount: 9.3, percentage: 6, icon: 'bi-laptop', variant: 'secondary' }
]);

const recentLogs = ref([
  { 
    id: 1, 
    date: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 hours ago
    type: 'Plastic Bottles', 
    amount: 2.5, 
    method: 'Recycling',
    carbonImpact: 1.2
  },
  { 
    id: 2, 
    date: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 day ago
    type: 'Food Waste', 
    amount: 1.8, 
    method: 'Composting',
    carbonImpact: 0.9
  },
  { 
    id: 3, 
    date: new Date(Date.now() - 1000 * 60 * 60 * 26), // 1 day 2 hours ago
    type: 'Cardboard Boxes', 
    amount: 3.2, 
    method: 'Recycling',
    carbonImpact: 0.8
  },
  { 
    id: 4, 
    date: new Date(Date.now() - 1000 * 60 * 60 * 48), // 2 days ago
    type: 'Batteries', 
    amount: 0.5, 
    method: 'Hazardous',
    carbonImpact: 2.1
  },
  { 
    id: 5, 
    date: new Date(Date.now() - 1000 * 60 * 60 * 72), // 3 days ago
    type: 'Glass Jars', 
    amount: 1.2, 
    method: 'Recycling',
    carbonImpact: 0.3
  }
]);

const wasteReductionTips = ref([
  {
    id: 1,
    title: 'Use Reusable Bags',
    icon: 'bi-bag',
    description: 'Switch to reusable shopping bags to reduce plastic waste.',
    savings: 5.2,
    difficulty: 1,
    steps: [
      'Keep reusable bags in your car or by the door',
      'Opt for cloth or recycled material bags',
      'Politely decline plastic bags at stores'
    ],
    benefits: [
      'Reduces plastic waste in landfills',
      'Saves money on bag fees',
      'More durable than single-use bags'
    ],
    proTip: 'Store a foldable reusable bag in your purse or backpack for unexpected shopping trips.'
  },
  {
    id: 2,
    title: 'Start Composting',
    icon: 'bi-recycle',
    description: 'Turn food scraps into nutrient-rich compost for your garden.',
    savings: 8.7,
    difficulty: 3,
    steps: [
      'Set up a compost bin in your yard or use a countertop composter',
      'Add food scraps like fruit peels and coffee grounds',
      'Turn the compost regularly and keep it moist'
    ],
    benefits: [
      'Reduces methane emissions from landfills',
      'Creates free fertilizer for plants',
      'Lowers your carbon footprint'
    ],
    proTip: 'Start with a small indoor compost bin if you don\'t have outdoor space.'
  },
  {
    id: 3,
    title: 'Switch to a Reusable Water Bottle',
    icon: 'bi-droplet',
    description: 'Ditch single-use plastic bottles for a reusable alternative.',
    savings: 6.5,
    difficulty: 1,
    steps: [
      'Choose a durable, BPA-free water bottle',
      'Fill it up before leaving home',
      'Use water fountains or ask restaurants to refill it'
    ],
    benefits: [
      'Saves money on bottled water',
      'Reduces plastic waste significantly',
      'Keeps drinks at desired temperature longer'
    ],
    proTip: 'Get an insulated bottle to keep water cold for hours.'
  },
  {
    id: 4,
    title: 'Buy in Bulk',
    icon: 'bi-box-seam',
    description: 'Reduce packaging waste by purchasing larger quantities.',
    savings: 4.3,
    difficulty: 2,
    steps: [
      'Bring your own containers to bulk stores',
      'Plan purchases to avoid waste',
      'Store bulk items properly to maintain freshness'
    ],
    benefits: [
      'Reduces packaging waste',
      'Saves money in the long run',
      'Reduces shopping frequency'
    ],
    proTip: 'Team up with friends or family to split bulk purchases.'
  },
  {
    id: 5,
    title: 'Use Cloth Instead of Paper',
    icon: 'bi-bandaid',
    description: 'Replace paper towels with reusable cloth alternatives.',
    savings: 3.8,
    difficulty: 2,
    steps: [
      'Invest in quality cloth napkins and towels',
      'Use rags for cleaning instead of paper towels',
      'Wash and reuse regularly'
    ],
    benefits: [
      'Reduces paper waste',
      'Saves money over time',
      'More absorbent than paper products'
    ],
    proTip: 'Designate specific colors for different cleaning tasks.'
  },
  {
    id: 6,
    title: 'Repair Instead of Replace',
    icon: 'bi-tools',
    description: 'Fix broken items rather than throwing them away.',
    savings: 7.2,
    difficulty: 3,
    steps: [
      'Learn basic repair skills',
      'Find local repair cafes or services',
      'Consider the environmental impact before replacing'
    ],
    benefits: [
      'Reduces waste in landfills',
      'Saves money on replacements',
      'Extends product lifecycles'
    ],
    proTip: 'Check if the manufacturer offers repair services or guides.'
  }
]);

// Methods
const initCharts = () => {
  // Destroy existing charts if they exist
  if (wasteChartInstance) wasteChartInstance.destroy();
  if (trendsChartInstance) trendsChartInstance.destroy();
  if (disposalChartInstance) disposalChartInstance.destroy();
  
  // Waste Composition Chart
  const ctx1 = wasteChart.value.getContext('2d');
  wasteChartInstance = new Chart(ctx1, {
    type: 'doughnut',
    data: {
      labels: wasteCategories.value.map(cat => cat.name),
      datasets: [{
        data: wasteCategories.value.map(cat => cat.amount),
        backgroundColor: [
          'rgba(78, 115, 223, 0.8)',
          'rgba(23, 162, 184, 0.8)',
          'rgba(40, 167, 69, 0.8)',
          'rgba(255, 193, 7, 0.8)',
          'rgba(220, 53, 69, 0.8)',
          'rgba(108, 117, 125, 0.8)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.label || '';
              const value = context.raw || 0;
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const percentage = Math.round((value / total) * 100);
              return `${label}: ${value} kg (${percentage}%)`;
            }
          }
        }
      },
      cutout: '70%'
    }
  });
  
  // Waste Trends Over Time Chart
  const ctx2 = trendsChart.value.getContext('2d');
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const currentMonth = new Date().getMonth();
  const lastSixMonths = [];
  
  for (let i = 5; i >= 0; i--) {
    const monthIndex = (currentMonth - i + 12) % 12;
    lastSixMonths.push(months[monthIndex]);
  }
  
  trendsChartInstance = new Chart(ctx2, {
    type: 'line',
    data: {
      labels: lastSixMonths,
      datasets: [
        {
          label: 'Total Waste (kg)',
          data: [28, 35, 42, 39, 31, 25],
          borderColor: 'rgba(78, 115, 223, 1)',
          backgroundColor: 'rgba(78, 115, 223, 0.1)',
          tension: 0.3,
          fill: true
        },
        {
          label: 'Recycled (kg)',
          data: [15, 20, 25, 24, 18, 15],
          borderColor: 'rgba(40, 167, 69, 1)',
          backgroundColor: 'rgba(40, 167, 69, 0.1)',
          tension: 0.3,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        tooltip: {
          mode: 'index',
          intersect: false,
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  });
  
  // Waste Disposal Methods Chart
  const ctx3 = disposalChart.value.getContext('2d');
  disposalChartInstance = new Chart(ctx3, {
    type: 'bar',
    data: {
      labels: ['Recycling', 'Composting', 'Landfill', 'Hazardous', 'Donation'],
      datasets: [{
        label: 'Waste by Disposal Method (kg)',
        data: [65, 32, 42, 8, 12],
        backgroundColor: [
          'rgba(40, 167, 69, 0.8)',
          'rgba(13, 110, 253, 0.8)',
          'rgba(108, 117, 125, 0.8)',
          'rgba(220, 53, 69, 0.8)',
          'rgba(255, 193, 7, 0.8)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `${context.parsed.y} kg (${Math.round((context.parsed.y / 159) * 100)}%)`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  });
};

const formatNumber = (num) => {
  return num.toLocaleString();
};

const formatDate = (date) => {
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
};

const formatTime = (date) => {
  return date.toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: true
  });
};

const getWasteType = (type) => {
  // In a real app, this would be a more sophisticated lookup
  if (type.toLowerCase().includes('plastic')) return { icon: 'bi-arrow-repeat', variant: 'primary' };
  if (type.toLowerCase().includes('paper') || type.toLowerCase().includes('cardboard')) return { icon: 'bi-file-text', variant: 'info' };
  if (type.toLowerCase().includes('food') || type.toLowerCase().includes('organic')) return { icon: 'bi-egg-fried', variant: 'success' };
  if (type.toLowerCase().includes('glass')) return { icon: 'bi-cup-straw', variant: 'warning' };
  if (type.toLowerCase().includes('metal')) return { icon: 'bi-cup', variant: 'danger' };
  if (type.toLowerCase().includes('e-waste') || type.toLowerCase().includes('batter')) return { icon: 'bi-laptop', variant: 'secondary' };
  return { icon: 'bi-trash', variant: 'dark' };
};

const getDisposalMethod = (method) => {
  // In a real app, this would be a more sophisticated lookup
  switch(method.toLowerCase()) {
    case 'recycling':
      return { variant: 'success' };
    case 'composting':
      return { variant: 'primary' };
    case 'landfill':
      return { variant: 'secondary' };
    case 'hazardous':
      return { variant: 'danger' };
    case 'donation':
      return { variant: 'info' };
    default:
      return { variant: 'dark' };
  }
};

const viewTipDetails = (tip) => {
  selectedTip.value = { ...tip };
};

const addToActionPlan = (tip) => {
  // In a real app, this would add the tip to the user's action plan
  alert(`Added "${tip.title}" to your action plan!`);
  selectedTip.value = null;
};

const exportReport = () => {
  // In a real app, this would generate and download a report
  alert('Exporting waste summary report...');
};

// Watchers
watch(timeRange, () => {
  // In a real app, this would fetch new data based on the selected time range
  console.log('Time range changed to:', timeRange.value);
  // Simulate loading new data
  setTimeout(() => {
    // Update summary data
    summary.value = {
      totalWaste: Math.floor(Math.random() * 200) + 100,
      wasteChange: Math.floor(Math.random() * 40) - 20,
      recyclingRate: Math.floor(Math.random() * 30) + 50,
      carbonFootprint: Math.floor(Math.random() * 200) + 200,
      carbonChange: Math.floor(Math.random() * 40) - 20,
      wasteReduction: Math.floor(Math.random() * 30) + 10,
      lastUpdated: new Date()
    };
    
    // Update charts
    if (wasteChartInstance) wasteChartInstance.update();
    if (trendsChartInstance) trendsChartInstance.update();
    if (disposalChartInstance) disposalChartInstance.update();
  }, 500);
});

watch(activeChartTab, () => {
  // In a real app, this would update the chart based on the selected tab
  console.log('Chart tab changed to:', activeChartTab.value);
  
  // For demo purposes, just update the chart title
  if (wasteChartInstance) {
    wasteChartInstance.destroy();
    nextTick(() => {
      const ctx = wasteChart.value.getContext('2d');
      let title = 'Waste by Weight (kg)';
      let unit = 'kg';
      
      if (activeChartTab.value === 'volume') {
        title = 'Waste by Volume (liters)';
        unit = 'L';
      } else if (activeChartTab.value === 'impact') {
        title = 'Waste by Carbon Impact (kg CO₂)';
        unit = 'kg CO₂';
      }
      
      wasteChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: wasteCategories.value.map(cat => cat.name),
          datasets: [{
            data: wasteCategories.value.map(cat => {
              // Generate some sample data based on the selected tab
              if (activeChartTab.value === 'volume') {
                return Math.floor(cat.amount * (0.8 + Math.random() * 0.4));
              } else if (activeChartTab.value === 'impact') {
                return Math.floor(cat.amount * (1.5 + Math.random() * 2));
              }
              return cat.amount;
            }),
            backgroundColor: [
              'rgba(78, 115, 223, 0.8)',
              'rgba(23, 162, 184, 0.8)',
              'rgba(40, 167, 69, 0.8)',
              'rgba(255, 193, 7, 0.8)',
              'rgba(220, 53, 69, 0.8)',
              'rgba(108, 117, 125, 0.8)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: title,
              font: {
                size: 16
              }
            },
            legend: {
              position: 'right',
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.raw || 0;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = Math.round((value / total) * 100);
                  return `${label}: ${value} ${unit} (${percentage}%)`;
                }
              }
            }
          },
          cutout: '70%'
        }
      });
    });
  }
});

// Lifecycle hooks
onMounted(() => {
  // Initialize charts when component is mounted
  nextTick(() => {
    initCharts();
  });
  
  // Add window resize event listener to handle chart resizing
  window.addEventListener('resize', () => {
    if (wasteChartInstance || trendsChartInstance || disposalChartInstance) {
      initCharts();
    }
  });
});
</script>

<style scoped>
.waste-summary {
  padding: 1.5rem;
}

.card {
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
}

.progress {
  border-radius: 10px;
  height: 10px;
}

.progress-bar {
  border-radius: 10px;
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .waste-summary {
    padding: 1rem;
  }
  
  .chart-container {
    height: 250px !important;
  }
}

/* Custom scrollbar for tables */
.table-responsive {
  max-height: 400px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #dee2e6 #f8f9fa;
}

.table-responsive::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.table-responsive::-webkit-scrollbar-track {
  background: #f8f9fa;
}

.table-responsive::-webkit-scrollbar-thumb {
  background-color: #dee2e6;
  border-radius: 3px;
}

/* Animation for list items */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

tbody tr {
  animation: fadeIn 0.3s ease-out forwards;
  opacity: 0;
}

tbody tr:nth-child(1) { animation-delay: 0.1s; }
tbody tr:nth-child(2) { animation-delay: 0.15s; }
tbody tr:nth-child(3) { animation-delay: 0.2s; }
tbody tr:nth-child(4) { animation-delay: 0.25s; }
tbody tr:nth-child(5) { animation-delay: 0.3s; }
tbody tr:nth-child(n+6) { animation-delay: 0.35s; }

/* Modal styles */
.modal-content {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.modal-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 1.25rem 1.5rem;
}

.modal-footer {
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  padding: 1rem 1.5rem;
}

/* Badge colors */
.bg-warning { background-color: #ffc107 !important; }
.bg-info { background-color: #0dcaf0 !important; }
.bg-success { background-color: #198754 !important; }
.bg-danger { background-color: #dc3545 !important; }
.bg-primary { background-color: #0d6efd !important; }
.bg-secondary { background-color: #6c757d !important; }

/* Background subtle colors */
.bg-warning-subtle { background-color: #fff3cd !important; }
.bg-info-subtle { background-color: #d1ecf1 !important; }
.bg-success-subtle { background-color: #d1e7dd !important; }
.bg-danger-subtle { background-color: #f8d7da !important; }
.bg-primary-subtle { background-color: #cfe2ff !important; }
.bg-secondary-subtle { background-color: #e2e3e5 !important; }
</style>
