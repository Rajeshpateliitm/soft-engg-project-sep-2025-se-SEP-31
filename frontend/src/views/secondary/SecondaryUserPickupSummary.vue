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
            <div class="stat-value">{{ summaryData.total_scheduled || 0 }}</div>
            <div class="stat-icon">
              <i class="bi bi-arrow-down-circle"></i>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3 mb-3">
          <div class="stat-card">
            <div class="stat-label">TOTAL PICKUPS COMPLETED</div>
            <div class="stat-value">{{ summaryData.total_completed || 0 }}</div>
            <div class="stat-icon">
              <i class="bi bi-check-circle"></i>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3 mb-3">
          <div class="stat-card">
            <div class="stat-label">TOTAL PENDING PICKUPS</div>
            <div class="stat-value">{{ summaryData.total_pending || 0 }}</div>
            <div class="stat-icon">
              <i class="bi bi-clock-history"></i>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3 mb-3">
          <div class="stat-card">
            <div class="stat-label">TOTAL REJECTED PICKUPS</div>
            <div class="stat-value">{{ summaryData.total_rejected || 0 }}</div>
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
            <div class="card-header text-white d-flex justify-content-between align-items-center" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; border: none;">
              <div>
                <h5 class="card-title mb-1 fw-bold">
                  <i class="bi bi-bar-chart-line me-2"></i>Daily Pick-ups Status
                </h5>
                <small class="text-white-50 opacity-75">Interactive chart showing pickup trends over time</small>
              </div>
              <button class="btn btn-sm btn-light shadow-sm" @click="exportData" style="border-radius: 20px; transition: all 0.3s;">
                <i class="bi bi-download me-1"></i>Export Data
              </button>
            </div>
            <div class="card-body">
              <div v-if="Object.keys(summaryData.daily_breakdown || {}).length === 0 && !loading" class="text-center py-5 text-muted">
                <i class="bi bi-bar-chart" style="font-size: 3rem; color: #6c757d;"></i>
                <p class="mt-3">No pickup data available for the selected period.</p>
              </div>
              <div v-else class="chart-container">
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
              <div v-if="summaryData.waste_type_distribution.wet > 0 || summaryData.waste_type_distribution.dry > 0 || summaryData.waste_type_distribution.hazardous > 0">
                <div class="waste-type-item" v-if="summaryData.waste_type_distribution.wet > 0">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="waste-label">Wet Waste (Organic)</span>
                    <span class="waste-percentage">{{ summaryData.waste_type_distribution.wet.toFixed(1) }}%</span>
                </div>
                <div class="progress" style="height: 8px;">
                    <div class="progress-bar bg-success" :style="{ width: summaryData.waste_type_distribution.wet + '%' }"></div>
                  </div>
                </div>
                <div class="waste-type-item" v-if="summaryData.waste_type_distribution.dry > 0">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="waste-label">Dry Waste (Recyclable)</span>
                    <span class="waste-percentage">{{ summaryData.waste_type_distribution.dry.toFixed(1) }}%</span>
                </div>
                <div class="progress" style="height: 8px;">
                    <div class="progress-bar bg-info" :style="{ width: summaryData.waste_type_distribution.dry + '%' }"></div>
                  </div>
                </div>
                <div class="waste-type-item" v-if="summaryData.waste_type_distribution.hazardous > 0">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="waste-label">Hazardous Waste</span>
                    <span class="waste-percentage">{{ summaryData.waste_type_distribution.hazardous.toFixed(1) }}%</span>
                </div>
                <div class="progress" style="height: 8px;">
                    <div class="progress-bar bg-warning" :style="{ width: summaryData.waste_type_distribution.hazardous + '%' }"></div>
                </div>
                </div>
              </div>
              <div v-else class="text-center text-muted py-3">
                <p>No waste data available for the selected period.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Monthly Statistics Table -->
        <div class="col-lg-6 mb-3">
          <div class="card shadow-lg">
            <div class="card-header bg-success text-white">
              <h5 class="card-title mb-0">Monthly Statistics (Last 30 Days)</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-sm">
                  <tbody>
                    <tr>
                      <td><strong>Total Waste Collected</strong></td>
                      <td class="text-end"><strong>{{ summaryData.total_waste_collected.toFixed(2) }} KG</strong></td>
                    </tr>
                    <tr>
                      <td>Average Daily Pickup</td>
                      <td class="text-end">{{ summaryData.average_daily_pickup.toFixed(2) }} KG</td>
                    </tr>
                    <tr v-if="summaryData.peak_pickup_day">
                      <td>Peak Pickup Day</td>
                      <td class="text-end">
                        {{ formatDateShort(summaryData.peak_pickup_day.date) }} 
                        ({{ summaryData.peak_pickup_day.waste_kg }} KG, {{ summaryData.peak_pickup_day.pickup_count }} pickups)
                      </td>
                    </tr>
                    <tr v-else>
                      <td>Peak Pickup Day</td>
                      <td class="text-end">N/A</td>
                    </tr>
                    <tr v-if="summaryData.lowest_pickup_day">
                      <td>Lowest Pickup Day</td>
                      <td class="text-end">
                        {{ formatDateShort(summaryData.lowest_pickup_day.date) }} 
                        ({{ summaryData.lowest_pickup_day.waste_kg }} KG, {{ summaryData.lowest_pickup_day.pickup_count }} pickups)
                      </td>
                    </tr>
                    <tr v-else>
                      <td>Lowest Pickup Day</td>
                      <td class="text-end">N/A</td>
                    </tr>
                    <tr>
                      <td><strong>Completion Rate</strong></td>
                      <td class="text-end"><strong>{{ summaryData.completion_rate.toFixed(2) }}%</strong></td>
                    </tr>
                    <tr>
                      <td>Rejection Rate</td>
                      <td class="text-end">{{ summaryData.rejection_rate.toFixed(2) }}%</td>
                    </tr>
                    <tr>
                      <td>Pending Rate</td>
                      <td class="text-end">{{ summaryData.pending_rate.toFixed(2) }}%</td>
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
              <h5 class="card-title mb-0">Detailed Pickup Breakdown</h5>
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
                    <tr v-if="loading">
                      <td colspan="7" class="text-center py-4">
                        <div class="spinner-border text-primary" role="status">
                          <span class="visually-hidden">Loading...</span>
                        </div>
                      </td>
                    </tr>
                    <tr v-else-if="errorMessage">
                      <td colspan="7" class="text-center py-4">
                        <div class="alert alert-danger mb-0">{{ errorMessage }}</div>
                      </td>
                    </tr>
                    <tr v-else-if="dailyBreakdown.length === 0">
                      <td colspan="7" class="text-center py-4 text-muted">
                        No pickup data available
                      </td>
                    </tr>
                    <tr v-else v-for="(day, index) in dailyBreakdown" :key="day.dateStr || index" :class="{ 'table-info': day.isToday }">
                      <td>
                        <strong>{{ day.date }}</strong>
                        <span v-if="day.isToday" class="badge bg-primary ms-2">Today</span>
                      </td>
                      <td>{{ day.scheduled }}</td>
                      <td><span class="badge bg-success">{{ day.completed }}</span></td>
                      <td><span class="badge bg-warning text-dark">{{ day.pending }}</span></td>
                      <td><span class="badge bg-danger">{{ day.rejected }}</span></td>
                      <td><strong>{{ day.waste }} KG</strong></td>
                      <td>
                        <div class="progress" style="height: 20px;">
                          <div class="progress-bar" :class="getCompletionBarClass(day.completion)" :style="{ width: day.completion + '%' }">
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
import { ref, onMounted, computed, onBeforeUnmount, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const router = useRouter();
const loading = ref(true);
const errorMessage = ref('');
const summaryData = ref({
  total_scheduled: 0,
  total_completed: 0,
  total_pending: 0,
  total_rejected: 0,
  total_waste_collected: 0,
  average_daily_pickup: 0,
  completion_rate: 0,
  rejection_rate: 0,
  pending_rate: 0,
  peak_pickup_day: null,
  lowest_pickup_day: null,
  waste_type_distribution: {
    wet: 0,
    dry: 0,
    hazardous: 0
  },
  daily_breakdown: {}
});

const dailyBreakdown = computed(() => {
  const breakdown = [];
  const dailyData = summaryData.value.daily_breakdown || {};
  
  // Get today's date (set to start of day for comparison)
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  // Filter dates: only today and future dates (no past dates)
  const allDates = Object.keys(dailyData).filter(dateStr => {
    const date = new Date(dateStr);
    date.setHours(0, 0, 0, 0);
    return date >= today; // Include today and future dates only
  });
  
  // Sort dates in ascending order (oldest first, newest last) so today is at bottom, future dates above
  const sortedDates = allDates.sort((a, b) => new Date(a) - new Date(b));
  
  // Limit to last 7 days from today (including today and up to 6 future days)
  const limitedDates = sortedDates.slice(0, 7);
  
  limitedDates.forEach((dateStr) => {
    const day = dailyData[dateStr];
    const date = new Date(dateStr);
    const scheduled = day.scheduled || ((day.completed || 0) + (day.pending || 0) + (day.rejected || 0) + (day.accepted || 0));
    const completed = day.completed || 0;
    const pending = day.pending || 0;
    const rejected = day.rejected || 0;
    const waste_kg = day.waste_kg || 0;
    const completion = scheduled > 0 ? Math.round((completed / scheduled) * 100) : 0;
    
    // Format date as DD-MM-YYYY
    const dayStr = String(date.getDate()).padStart(2, '0');
    const monthStr = String(date.getMonth() + 1).padStart(2, '0');
    const yearStr = date.getFullYear();
    const formattedDate = `${dayStr}-${monthStr}-${yearStr}`;
    
    // Check if this is today
    const isToday = date.getTime() === today.getTime();
    
    breakdown.push({
      date: formattedDate,
      dateStr: dateStr,
      scheduled: scheduled,
      completed: completed,
      pending: pending,
      rejected: rejected,
      waste: waste_kg.toFixed(2),
      completion: completion,
      isToday: isToday
    });
  });
  
  // Return in ascending order (today at bottom, future dates above)
  return breakdown;
});

const fetchPickupSummary = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';
    const response = await api.get('/secondary/pickup-summary', {
      params: { months: 1 }
    });
    
    // Ensure all fields are set with defaults
    summaryData.value = {
      total_scheduled: response.data.total_scheduled || 0,
      total_completed: response.data.total_completed || 0,
      total_pending: response.data.total_pending || 0,
      total_rejected: response.data.total_rejected || 0,
      total_waste_collected: response.data.total_waste_collected || 0,
      average_daily_pickup: response.data.average_daily_pickup || 0,
      completion_rate: response.data.completion_rate || 0,
      rejection_rate: response.data.rejection_rate || 0,
      pending_rate: response.data.pending_rate || 0,
      peak_pickup_day: response.data.peak_pickup_day || null,
      lowest_pickup_day: response.data.lowest_pickup_day || null,
      waste_type_distribution: response.data.waste_type_distribution || {
        wet: 0,
        dry: 0,
        hazardous: 0
      },
      daily_breakdown: response.data.daily_breakdown || {}
    };
    
  } catch (error) {
    console.error('Error fetching pickup summary:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to load pickup summary. Please try again.';
    summaryData.value = {
      total_scheduled: 0,
      total_completed: 0,
      total_pending: 0,
      total_rejected: 0,
      total_waste_collected: 0,
      average_daily_pickup: 0,
      completion_rate: 0,
      rejection_rate: 0,
      pending_rate: 0,
      peak_pickup_day: null,
      lowest_pickup_day: null,
      waste_type_distribution: { wet: 0, dry: 0, hazardous: 0 },
      daily_breakdown: {}
    };
  } finally {
    loading.value = false;
    // Initialize chart after data is loaded and DOM is ready
    await nextTick();
    setTimeout(() => {
      initChart();
    }, 200);
  }
};

let pickupChartInstance = null;

const initChart = () => {
  const ctx = document.getElementById('pickupChart');
  if (!ctx) return;
  
  // Destroy existing chart if it exists
  if (pickupChartInstance) {
    pickupChartInstance.destroy();
  }
  
  const dailyData = summaryData.value.daily_breakdown || {};
  
  // Get today's date (set to start of day for comparison)
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  // Filter dates: only today and future dates (no past dates)
  const allDates = Object.keys(dailyData).filter(dateStr => {
    const date = new Date(dateStr);
    date.setHours(0, 0, 0, 0);
    return date >= today; // Include today and future dates only
  });
  
  // Sort dates in ascending order (oldest to newest) so today is at right, future dates to the left
  const sortedDates = allDates.sort((a, b) => new Date(a) - new Date(b)).slice(0, 30);
  
  if (sortedDates.length === 0) {
    // Show empty state message
    return;
  }
  
  // Get canvas context for gradients
  const chartArea = ctx.getContext('2d');
  
  // Create gradient colors for each dataset
  const completedGradient = chartArea.createLinearGradient(0, 0, 0, 450);
  completedGradient.addColorStop(0, 'rgba(40, 167, 69, 0.95)');
  completedGradient.addColorStop(0.5, 'rgba(40, 167, 69, 0.7)');
  completedGradient.addColorStop(1, 'rgba(40, 167, 69, 0.4)');

  const pendingGradient = chartArea.createLinearGradient(0, 0, 0, 450);
  pendingGradient.addColorStop(0, 'rgba(255, 193, 7, 0.95)');
  pendingGradient.addColorStop(0.5, 'rgba(255, 193, 7, 0.7)');
  pendingGradient.addColorStop(1, 'rgba(255, 193, 7, 0.4)');

  const rejectedGradient = chartArea.createLinearGradient(0, 0, 0, 450);
  rejectedGradient.addColorStop(0, 'rgba(220, 53, 69, 0.95)');
  rejectedGradient.addColorStop(0.5, 'rgba(220, 53, 69, 0.7)');
  rejectedGradient.addColorStop(1, 'rgba(220, 53, 69, 0.4)');

  // Store sorted dates in a variable accessible to tooltip callbacks
  // Create a copy that will be accessible in the chart options
  const chartDates = [...sortedDates];
  
  pickupChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartDates.map(d => {
        const date = new Date(d);
        return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
      }),
      datasets: [
        {
          label: '✅ Completed',
          data: chartDates.map(d => dailyData[d]?.completed || 0),
          backgroundColor: completedGradient,
          borderColor: '#28a745',
          borderWidth: 2,
          borderRadius: {
            topLeft: 8,
            topRight: 8,
            bottomLeft: 0,
            bottomRight: 0
          },
          borderSkipped: false,
          barThickness: 'flex',
          maxBarThickness: 50,
          categoryPercentage: 0.7,
          barPercentage: 0.85
        },
        {
          label: '⏳ Pending',
          data: chartDates.map(d => dailyData[d]?.pending || 0),
          backgroundColor: pendingGradient,
          borderColor: '#ffc107',
          borderWidth: 2,
          borderRadius: {
            topLeft: 8,
            topRight: 8,
            bottomLeft: 0,
            bottomRight: 0
          },
          borderSkipped: false,
          barThickness: 'flex',
          maxBarThickness: 50,
          categoryPercentage: 0.7,
          barPercentage: 0.85
        },
        {
          label: '❌ Rejected',
          data: chartDates.map(d => dailyData[d]?.rejected || 0),
          backgroundColor: rejectedGradient,
          borderColor: '#dc3545',
          borderWidth: 2,
          borderRadius: {
            topLeft: 8,
            topRight: 8,
            bottomLeft: 0,
            bottomRight: 0
          },
          borderSkipped: false,
          barThickness: 'flex',
          maxBarThickness: 50,
          categoryPercentage: 0.7,
          barPercentage: 0.85
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 1500,
        easing: 'easeInOutQuart',
        delay: (context) => {
          return context.dataIndex * 30;
        }
      },
      plugins: {
        legend: {
          position: 'top',
          align: 'center',
          labels: {
            usePointStyle: true,
            pointStyle: 'circle',
            padding: 20,
            font: {
              size: 13,
              weight: '600',
              family: "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
            },
            color: '#2c3e50',
            boxWidth: 12,
            boxHeight: 12
          },
          onClick: (e, legendItem) => {
            // Allow toggling datasets on legend click
            const index = legendItem.datasetIndex;
            const chart = pickupChartInstance;
            const meta = chart.getDatasetMeta(index);
            meta.hidden = !meta.hidden;
            chart.update();
          }
        },
        tooltip: {
          enabled: true,
          mode: 'index',
          intersect: false,
          backgroundColor: 'rgba(0, 0, 0, 0.85)',
          padding: 16,
          titleFont: {
            size: 14,
            weight: 'bold',
            family: "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
          },
          bodyFont: {
            size: 13,
            weight: '500',
            family: "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
          },
          titleColor: '#fff',
          bodyColor: '#fff',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          cornerRadius: 8,
          displayColors: true,
          callbacks: {
            title: function(context) {
              // Get the actual date from the sorted dates array using the data index
              const dayIndex = context[0].dataIndex;
              const dateStr = chartDates[dayIndex];
              
              if (!dateStr) {
                // Fallback: return the label as-is
                return context[0].label;
              }
              
              // Parse the ISO date string (format: YYYY-MM-DD) to get the correct date with year
              // The dateStr is already in ISO format from the backend
              const date = new Date(dateStr);
              // Validate the date
              if (isNaN(date.getTime())) {
                return context[0].label;
              }
              
              const today = new Date();
              today.setHours(0, 0, 0, 0);
              const dateOnly = new Date(date);
              dateOnly.setHours(0, 0, 0, 0);
              const isToday = dateOnly.getTime() === today.getTime();
              
              // Format date with full year
              let title = date.toLocaleDateString('en-GB', { 
                weekday: 'long', 
                day: 'numeric', 
                month: 'long', 
                year: 'numeric' 
              });
              
              if (isToday) {
                title += ' (Today)';
              }
              
              return title;
            },
            label: function(context) {
              let label = context.dataset.label || '';
              // Remove emoji for tooltip
              label = label.replace(/[✅⏳❌]/g, '').trim();
              if (label) {
                label += ': ';
              }
              const value = context.parsed.y;
              label += value + ' pickup' + (value !== 1 ? 's' : '');
              
              // Add percentage of day's total pickups
              const dayIndex = context.dataIndex;
              const dayData = context.chart.data.datasets.map(d => d.data[dayIndex] || 0);
              const dayTotal = dayData.reduce((a, b) => a + b, 0);
              if (dayTotal > 0) {
                const percentage = ((value / dayTotal) * 100).toFixed(1);
                label += ` (${percentage}% of day's total)`;
              }
              
              return label;
            },
            labelColor: function(context) {
              return {
                borderColor: context.dataset.borderColor,
                backgroundColor: context.dataset.borderColor,
                borderWidth: 2,
                borderRadius: 4
              };
            }
          }
        }
      },
      scales: {
        x: {
          stacked: false,
          grid: {
            display: false,
            drawBorder: false
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45,
            font: {
              size: 11,
              weight: '500',
              family: "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
            },
            color: '#6c757d',
            padding: 8
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1,
            precision: 0,
            font: {
              size: 11,
              weight: '500',
              family: "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
            },
            color: '#6c757d',
            padding: 10
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.06)',
            drawBorder: false,
            lineWidth: 1
          },
          title: {
            display: true,
            text: 'Number of Pickups',
            font: {
              size: 13,
              weight: '600',
              family: "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
            },
            color: '#495057',
            padding: {
              top: 10,
              bottom: 15
            }
          }
        }
      },
      interaction: {
        mode: 'index',
        intersect: false
      },
      onHover: (event, activeElements) => {
        event.native.target.style.cursor = activeElements.length > 0 ? 'pointer' : 'default';
      }
    }
  });
};

const formatDateShort = (dateStr) => {
  if (!dateStr) return 'N/A';
  const date = new Date(dateStr);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  return `${day}-${month}`;
};

const goBack = () => {
  router.push('/secondary-dashboard/pickup-details');
};

const getCompletionBarClass = (completion) => {
  if (completion >= 80) return 'bg-success';
  if (completion >= 50) return 'bg-info';
  if (completion >= 25) return 'bg-warning';
  return 'bg-danger';
};

const exportData = () => {
  // Create CSV content
  let csv = 'Date,Scheduled,Completed,Pending,Rejected,Waste (KG),Completion %\n';
  dailyBreakdown.value.forEach(day => {
    csv += `${day.date},${day.scheduled},${day.completed},${day.pending},${day.rejected},${day.waste},${day.completion}%\n`;
  });
  
  // Create download link
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `pickup-summary-${new Date().toISOString().split('T')[0]}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
};

onMounted(async () => {
  await fetchPickupSummary();
});

onBeforeUnmount(() => {
  if (pickupChartInstance) {
    pickupChartInstance.destroy();
    pickupChartInstance = null;
  }
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
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.75rem 1.5rem rgba(0, 0, 0, 0.15) !important;
}

.card-header {
  border-bottom: none;
  border-radius: 0.75rem 0.75rem 0 0 !important;
}

.chart-container {
  position: relative;
  height: 450px;
  margin-bottom: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 0.75rem;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.chart-container:hover {
  box-shadow: inset 0 2px 12px rgba(0, 0, 0, 0.08);
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
