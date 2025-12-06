<template>
  <div class="monthly-engagement">
    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Loading engagement data...</p>
    </div>

    <!-- Content -->
    <template v-else>
    <div class="row mb-4">
      <div class="col-12">
        <div>
          <h2 class="mb-1">Monthly Engagement</h2>
          <p class="text-muted mb-0">Track your monthly activity and participation</p>
        </div>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="row mb-4">
      <div class="col-md-3 mb-3 mb-md-0">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="bg-primary bg-opacity-10 p-3 rounded-3 me-3">
                <i class="bi bi-check-circle text-primary" style="font-size: 1.5rem;"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Quizzes Completed</h6>
                <h3 class="mb-0">{{ engagementStats.quizzesCompleted }}</h3>
                <small class="text-success" v-if="engagementStats.quizzesChange > 0">
                  <i class="bi bi-arrow-up"></i> {{ engagementStats.quizzesChange }}% from last month
                </small>
                <small class="text-danger" v-else-if="engagementStats.quizzesChange < 0">
                  <i class="bi bi-arrow-down"></i> {{ Math.abs(engagementStats.quizzesChange) }}% from last month
                </small>
                <small class="text-muted" v-else>No change from last month</small>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-3 mb-md-0">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="bg-success bg-opacity-10 p-3 rounded-3 me-3">
                <i class="bi bi-star text-success" style="font-size: 1.5rem;"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Average Score</h6>
                <h3 class="mb-0">{{ engagementStats.averageScore }}%</h3>
                <small class="text-success" v-if="engagementStats.scoreChange > 0">
                  <i class="bi bi-arrow-up"></i> {{ engagementStats.scoreChange }}% from last month
                </small>
                <small class="text-danger" v-else-if="engagementStats.scoreChange < 0">
                  <i class="bi bi-arrow-down"></i> {{ Math.abs(engagementStats.scoreChange) }}% from last month
                </small>
                <small class="text-muted" v-else>No change from last month</small>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-3 mb-md-0">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="bg-warning bg-opacity-10 p-3 rounded-3 me-3">
                <i class="bi bi-lightning text-warning" style="font-size: 1.5rem;"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Current Streak</h6>
                <h3 class="mb-0">{{ engagementStats.currentStreak }} days</h3>
                <small class="text-muted">
                  <span v-if="engagementStats.streakActive">
                    <i class="bi bi-fire text-warning"></i> Keep it up!
                  </span>
                  <span v-else>
                    Start a new streak by taking a quiz today!
                  </span>
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="bg-info bg-opacity-10 p-3 rounded-3 me-3">
                <i class="bi bi-trophy text-info" style="font-size: 1.5rem;"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Ranking</h6>
                <h3 class="mb-0">#{{ engagementStats.ranking }}</h3>
                <small class="text-success" v-if="engagementStats.rankingChange > 0">
                  <i class="bi bi-arrow-up"></i> {{ engagementStats.rankingChange }} positions up
                </small>
                <small class="text-danger" v-else-if="engagementStats.rankingChange < 0">
                  <i class="bi bi-arrow-down"></i> {{ Math.abs(engagementStats.rankingChange) }} positions down
                </small>
                <small class="text-muted" v-else>No change in ranking</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Main Chart -->
      <div class="col-lg-8 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Monthly Activity Overview</h5>
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
              <canvas ref="engagementChartRef"></canvas>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Activity Breakdown -->
      <div class="col-lg-4 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <h5 class="mb-0">Activity Breakdown</h5>
          </div>
          <div class="card-body p-0">
            <div class="list-group list-group-flush">
              <div 
                v-for="(activity, index) in activityBreakdown" 
                :key="index"
                class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
              >
                <div class="d-flex align-items-center">
                  <div 
                    class="rounded-circle d-flex align-items-center justify-content-center me-3" 
                    :class="`bg-${activity.variant}-subtle`"
                    style="width: 40px; height: 40px;"
                  >
                    <i :class="`bi ${activity.icon} text-${activity.variant}`" style="font-size: 1.25rem;"></i>
                  </div>
                  <div>
                    <h6 class="mb-0">{{ activity.name }}</h6>
                    <small class="text-muted">{{ activity.description }}</small>
                  </div>
                </div>
                <span class="badge rounded-pill" :class="'bg-' + activity.variant">{{ activity.count }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="row">
      <!-- Monthly Summary -->
      <div class="col-lg-6 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <h5 class="mb-0">Monthly Summary</h5>
          </div>
          <div class="card-body">
            <div class="d-flex flex-column gap-3">
              <div class="d-flex justify-content-between align-items-center p-3 bg-light rounded">
                <div>
                  <h6 class="text-muted mb-1">Total Points Earned</h6>
                  <h3 class="mb-0">{{ activityBreakdown.find(a => a.name === 'Points Earned')?.count || 0 }}</h3>
            </div>
                <div class="bg-warning bg-opacity-10 p-3 rounded-circle">
                  <i class="bi bi-star-fill text-warning" style="font-size: 1.5rem;"></i>
                </div>
              </div>
              <div class="d-flex justify-content-between align-items-center p-3 bg-light rounded">
                <div>
                  <h6 class="text-muted mb-1">Quizzes Completed</h6>
                  <h3 class="mb-0">{{ engagementStats.quizzesCompleted }}</h3>
                </div>
                <div class="bg-primary bg-opacity-10 p-3 rounded-circle">
                  <i class="bi bi-check-circle text-primary" style="font-size: 1.5rem;"></i>
                </div>
              </div>
              <div class="d-flex justify-content-between align-items-center p-3 bg-light rounded">
                <div>
                  <h6 class="text-muted mb-1">Average Score</h6>
                  <h3 class="mb-0">{{ engagementStats.averageScore }}%</h3>
                </div>
                <div class="bg-success bg-opacity-10 p-3 rounded-circle">
                  <i class="bi bi-graph-up text-success" style="font-size: 1.5rem;"></i>
                </div>
              </div>
              <div class="d-flex justify-content-between align-items-center p-3 bg-light rounded">
                <div>
                  <h6 class="text-muted mb-1">Current Streak</h6>
                  <h3 class="mb-0">{{ engagementStats.currentStreak }} days</h3>
                </div>
                <div class="bg-danger bg-opacity-10 p-3 rounded-circle">
                  <i class="bi bi-fire text-danger" style="font-size: 1.5rem;"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Time of Day Activity -->
      <div class="col-lg-6 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <h5 class="mb-0">Time of Day Activity</h5>
          </div>
          <div class="card-body">
            <div class="chart-container" style="position: relative; height: 300px;">
              <canvas ref="timeOfDayChartRef"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Recent Activity -->
    <div class="row">
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Recent Activity</h5>
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>Activity</th>
                  <th>Date & Time</th>
                  <th>Details</th>
                  <th class="text-end">Points</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="recentActivities.length === 0">
                  <td colspan="4" class="text-center py-4">
                    <p class="text-muted mb-0">No recent activity found</p>
                  </td>
                </tr>
                <tr v-for="(activity, index) in recentActivities" :key="index">
                  <td>
                    <div class="d-flex align-items-center">
                      <div 
                        class="rounded-circle d-flex align-items-center justify-content-center me-3" 
                        :class="'bg-' + activity.variant + '-subtle'"
                        style="width: 36px; height: 36px;"
                      >
                        <i :class="`bi ${activity.icon} text-${activity.variant}`" style="font-size: 1rem;"></i>
                      </div>
                      <div>
                        <div class="fw-medium">{{ activity.title }}</div>
                        <small class="text-muted">{{ activity.subtitle }}</small>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="text-nowrap">{{ formatDate(activity.timestamp) }}</div>
                    <small class="text-muted">{{ formatTime(activity.timestamp) }}</small>
                  </td>
                  <td>
                    <span class="text-muted">{{ activity.details }}</span>
                  </td>
                  <td class="text-end">
                    <span 
                      v-if="activity.points > 0"
                      class="badge bg-success"
                    >
                      +{{ activity.points }}
                    </span>
                    <span 
                      v-else-if="activity.points < 0"
                      class="badge bg-danger"
                    >
                      {{ activity.points }}
                    </span>
                    <span 
                      v-else-if="activity.pickup_status === 'pending'"
                      class="badge bg-warning"
                    >
                      Pending
                    </span>
                    <span 
                      v-else
                      class="badge bg-secondary"
                    >
                      {{ activity.points }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    
        </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick, onBeforeUnmount } from 'vue';
import { Chart, registerables } from 'chart.js';
import api from '../../services/api';
import 'chartjs-adapter-date-fns';

// Register Chart.js components
Chart.register(...registerables);

// Refs
const selectedYear = ref(new Date().getFullYear());
const years = ref(Array.from({ length: 5 }, (_, i) => new Date().getFullYear() - i));
const activeChartTab = ref('quizzes');
const showAddGoalModal = ref(false);
const editingGoal = ref(null);
const engagementChartRef = ref(null);
const categoryChartRef = ref(null);
const timeOfDayChartRef = ref(null);
const isLoading = ref(true);

// Form data
const goalForm = ref({
  id: null,
  title: '',
  target: 10,
  current: 0,
  unit: 'quizzes',
  endDate: new Date(new Date().setMonth(new Date().getMonth() + 1)).toISOString().split('T')[0]
});

// Engagement data
const engagementStats = ref({
  quizzesCompleted: 0,
  quizzesChange: 0,
  averageScore: 0,
  scoreChange: 0,
  currentStreak: 0,
  streakActive: false,
  ranking: 0,
  rankingChange: 0
});

const dailyTrends = ref({});
const monthlyEngagement = ref({
  quizzes: 0,
  waste_logs: 0,
  campaigns: 0
});
const timeOfDayData = ref({});

const chartTabs = [
  { id: 'quizzes', label: 'Quizzes' },
  { id: 'points', label: 'Points' },
  { id: 'time', label: 'Time Spent' }
];

const activityBreakdown = ref([
  { name: 'Quizzes Taken', count: 0, icon: 'bi-check-circle', variant: 'primary', description: 'Total quizzes completed' },
  { name: 'Waste Logs', count: 0, icon: 'bi-trash', variant: 'success', description: 'Total waste entries' },
  { name: 'Campaigns', count: 0, icon: 'bi-calendar-event', variant: 'info', description: 'Campaigns participated' },
  { name: 'Points Earned', count: 0, icon: 'bi-star', variant: 'warning', description: 'Total points this month' }
]);

const recentActivities = ref([]);

const goals = ref([
  { 
    id: 1, 
    title: 'Complete 20 Quizzes', 
    progress: 75, 
    current: 15, 
    target: 20, 
    unit: 'quizzes', 
    endDate: '2023-12-31'
  },
  { 
    id: 2, 
    title: 'Reach 1000 Points', 
    progress: 45, 
    current: 450, 
    target: 1000, 
    unit: 'points', 
    endDate: '2023-12-31'
  },
  { 
    id: 3, 
    title: '30-Day Streak', 
    progress: 23, 
    current: 7, 
    target: 30, 
    unit: 'days', 
    endDate: '2023-12-31'
  }
]);

const achievements = ref([
  { 
    id: 1, 
    title: 'Quiz Master', 
    description: 'Complete 10 quizzes with 90%+ score', 
    icon: 'bi-trophy', 
    rarity: 'warning',
    date: '2023-11-15'
  },
  { 
    id: 2, 
    title: 'Early Bird', 
    description: 'Complete a quiz before 8 AM', 
    icon: 'bi-sun', 
    rarity: 'info',
    date: '2023-11-10'
  },
  { 
    id: 3, 
    title: 'Perfect Score', 
    description: 'Get 100% on any quiz', 
    icon: 'bi-star', 
    rarity: 'danger',
    date: '2023-11-05'
  },
  { 
    id: 4, 
    title: 'Quick Learner', 
    description: 'Complete 3 quizzes in one day', 
    icon: 'bi-lightning', 
    rarity: 'success',
    date: '2023-10-28'
  }
]);

// Chart instances
let engagementChartInstance = null;
let categoryChartInstance = null;
let timeOfDayChartInstance = null;

// Fetch monthly engagement data
const fetchMonthlyEngagement = async () => {
  try {
    isLoading.value = true;
    const response = await api.get('/primary/monthly-engagement');
    const data = response.data;
    
    console.log('Monthly engagement data:', data);
    
    // Update monthly engagement stats
    monthlyEngagement.value = {
      quizzes: data.monthly_engagement?.quizzes || 0,
      waste_logs: data.monthly_engagement?.waste_logs || 0,
      campaigns: data.monthly_engagement?.campaigns || 0
    };
    
    // Update daily trends (now with actual dates)
    dailyTrends.value = {};
    if (data.daily_trends && Array.isArray(data.daily_trends)) {
      data.daily_trends.forEach(trend => {
        dailyTrends.value[trend.date] = trend;
      });
    }
    
    // Update engagement stats from backend
    if (data.stats) {
      engagementStats.value = {
        quizzesCompleted: data.stats.quizzes_completed || 0,
        quizzesChange: data.stats.quizzes_change || 0,
        averageScore: data.stats.average_score || 0,
        scoreChange: data.stats.score_change || 0,
        currentStreak: data.stats.current_streak || 0,
        streakActive: data.stats.streak_active || false,
        ranking: data.stats.ranking || 0,
        rankingChange: data.stats.ranking_change || 0
      };
    }
    
    // Update activity breakdown with real data
    activityBreakdown.value = [
      { name: 'Quizzes Taken', count: monthlyEngagement.value.quizzes, icon: 'bi-check-circle', variant: 'primary', description: 'Total quizzes completed' },
      { name: 'Waste Logs', count: monthlyEngagement.value.waste_logs, icon: 'bi-trash', variant: 'success', description: 'Total waste entries' },
      { name: 'Campaigns', count: monthlyEngagement.value.campaigns, icon: 'bi-calendar-event', variant: 'info', description: 'Campaigns participated' },
      { name: 'Points Earned', count: data.monthly_engagement?.points || 0, icon: 'bi-star', variant: 'warning', description: 'Total points this month' }
    ];
    
    // Update recent activities from backend
    if (data.recent_activities && Array.isArray(data.recent_activities)) {
      recentActivities.value = data.recent_activities.map(activity => ({
        title: activity.title,
        subtitle: activity.subtitle,
        details: activity.details,
        points: activity.points || 0,
        timestamp: new Date(activity.timestamp),
        icon: activity.icon,
        variant: activity.variant,
        pickup_status: activity.pickup_status || null
      }));
    } else {
      recentActivities.value = [];
    }
    
    // Store time of day data
    if (data.time_of_day) {
      timeOfDayData.value = data.time_of_day;
    }
    
    // Initialize charts after data is loaded
    await nextTick();
    setTimeout(() => {
      initCharts();
    }, 100);
  } catch (error) {
    console.error('Error fetching monthly engagement:', error);
    console.error('Error details:', error.response?.data || error.message);
  } finally {
    isLoading.value = false;
  }
};

// Recent activities are now fetched from backend - no need to generate them

// Computed properties
const filteredActivities = computed(() => {
  return recentActivities.value
    .filter(activity => activity.timestamp.getFullYear() === selectedYear.value)
    .sort((a, b) => b.timestamp - a.timestamp);
});

// Methods
const initCharts = () => {
  // Destroy existing charts if they exist
  if (engagementChartInstance && typeof engagementChartInstance.destroy === 'function') {
    engagementChartInstance.destroy();
    engagementChartInstance = null;
  }
  if (categoryChartInstance && typeof categoryChartInstance.destroy === 'function') {
    categoryChartInstance.destroy();
    categoryChartInstance = null;
  }
  if (timeOfDayChartInstance && typeof timeOfDayChartInstance.destroy === 'function') {
    timeOfDayChartInstance.destroy();
    timeOfDayChartInstance = null;
  }
  
  // Engagement Chart (Line/Bar) with dates
  if (engagementChartRef.value) {
    const ctx1 = engagementChartRef.value.getContext('2d');
    if (ctx1) {
      const chartData = getEngagementChartData();
      const dataPoints = chartData.datasets[0].data;
      
      // Only create chart if we have data points
      if (dataPoints && dataPoints.length > 0) {
  engagementChartInstance = new Chart(ctx1, {
    type: activeChartTab.value === 'quizzes' ? 'bar' : 'line',
          data: chartData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
            interaction: {
              mode: 'index',
              intersect: false,
            },
      plugins: {
        legend: {
                display: true,
          position: 'top',
        },
        tooltip: {
          mode: 'index',
          intersect: false,
                callbacks: {
                  title: function(context) {
                    // Format date in tooltip
                    if (context && context.length > 0 && context[0].parsed && context[0].parsed.x) {
                      const date = new Date(context[0].parsed.x);
                      return date.toLocaleDateString('en-US', { 
                        year: 'numeric', 
                        month: 'short', 
                        day: 'numeric'
                      });
                    }
                    return '';
                  },
                  label: function(context) {
                    if (context.parsed && context.parsed.y !== null && context.parsed.y !== undefined) {
                      const label = context.dataset.label || '';
                      const value = context.parsed.y;
                      if (activeChartTab.value === 'time') {
                        return `${label}: ${value} minutes`;
                      }
                      return `${label}: ${value}`;
                    }
                    return '';
                  }
                }
        }
      },
      scales: {
              x: {
                type: 'time',
                time: {
                  unit: 'day',
                  displayFormats: {
                    day: 'MMM dd',
                    week: 'MMM dd',
                    month: 'MMM yyyy'
                  },
                  tooltipFormat: 'MMM dd, yyyy'
                },
                title: {
                  display: true,
                  text: 'Date'
                },
                grid: {
                  display: true,
                  color: 'rgba(0, 0, 0, 0.05)'
                },
                ticks: {
                  autoSkip: true,
                  maxTicksLimit: 15,
                  maxRotation: 45,
                  minRotation: 0
                }
              },
        y: {
          beginAtZero: true,
                title: {
                  display: true,
                  text: activeChartTab.value === 'quizzes' ? 'Quizzes' : 
                        activeChartTab.value === 'points' ? 'Points' : 'Minutes'
                },
          ticks: {
            precision: 0
                },
                grid: {
                  display: true,
                  color: 'rgba(0, 0, 0, 0.05)'
          }
        }
      }
    }
  });
      }
    }
  }
  
  // Category Performance Chart (Doughnut) - Not using real data, keeping simple placeholder
  // Note: Category breakdown data is not available from backend currently
  if (categoryChartRef.value) {
    const ctx2 = categoryChartRef.value.getContext('2d');
    if (ctx2) {
      // Create a simple empty/minimal chart or skip if no data
      // For now, we'll just not create it since we replaced it with a summary card
      // But keep the ref check in case the chart ref still exists
    }
  }
  
  // Time of Day Activity (Bar Chart) - using backend data
  if (timeOfDayChartRef.value) {
    const ctx3 = timeOfDayChartRef.value.getContext('2d');
    if (ctx3) {
      // Group hours into time periods for better visualization
      const timeLabels = ['12 AM', '3 AM', '6 AM', '9 AM', '12 PM', '3 PM', '6 PM', '9 PM'];
      const timeHours = [0, 3, 6, 9, 12, 15, 18, 21];
      
      // Get data from backend time_of_day
      const timeData = timeHours.map(hour => {
        // Sum activity in the 3-hour window (hour, hour+1, hour+2)
        let count = 0;
        for (let h = hour; h < hour + 3 && h < 24; h++) {
          count += timeOfDayData.value[h] || 0;
        }
        return count;
      });
      
      const maxValue = Math.max(...timeData, 1);
      
  timeOfDayChartInstance = new Chart(ctx3, {
        type: 'bar',
    data: {
          labels: timeLabels,
      datasets: [
        {
              label: 'Quiz Attempts',
              data: timeData,
              backgroundColor: 'rgba(78, 115, 223, 0.8)',
          borderColor: 'rgba(78, 115, 223, 1)',
              borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top',
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `Quizzes: ${context.parsed.y}`;
                }
              }
            }
          },
      scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Number of Quizzes'
              },
              ticks: {
                precision: 0,
                stepSize: 1
              },
              suggestedMax: Math.max(maxValue + 2, 5)
            },
            x: {
              title: {
                display: true,
                text: 'Time of Day'
              }
        }
      }
    }
  });
    }
  }
};

const getEngagementChartData = () => {
  // Use daily trends data from backend with actual dates
  const trendsList = Object.keys(dailyTrends.value)
    .sort()
    .map(dateStr => ({
      date: new Date(dateStr),
      ...dailyTrends.value[dateStr]
    }));
  
  if (trendsList.length === 0) {
    return {
      datasets: [
        {
          label: activeChartTab.value === 'quizzes' ? 'Quizzes' : 
                 activeChartTab.value === 'points' ? 'Points' : 'Minutes',
          data: [],
          backgroundColor: activeChartTab.value === 'quizzes' ? 'rgba(78, 115, 223, 0.8)' : 
                           activeChartTab.value === 'points' ? 'rgba(40, 167, 69, 0.8)' : 'rgba(255, 193, 7, 0.8)',
          borderColor: activeChartTab.value === 'quizzes' ? 'rgba(78, 115, 223, 1)' : 
                       activeChartTab.value === 'points' ? 'rgba(40, 167, 69, 1)' : 'rgba(255, 193, 7, 1)',
          borderWidth: 1,
          tension: activeChartTab.value === 'quizzes' ? 0 : 0.3,
          fill: activeChartTab.value !== 'quizzes'
        }
      ]
    };
  }
  
  // Create data points with dates
  const chartData = trendsList.map(trend => {
    let yValue = 0;
    switch (activeChartTab.value) {
      case 'quizzes':
        yValue = trend.quizzes || 0;
        break;
      case 'points':
        yValue = trend.points || 0;
        break;
      case 'time':
        yValue = (trend.quizzes || 0) * 5; // Estimate 5 min per quiz
        break;
    }
    return {
      x: trend.date,
      y: yValue
    };
  });
  
  return {
    datasets: [
      {
        label: activeChartTab.value === 'quizzes' ? 'Quizzes' : 
               activeChartTab.value === 'points' ? 'Points' : 'Minutes',
        data: chartData,
        backgroundColor: activeChartTab.value === 'quizzes' ? 'rgba(78, 115, 223, 0.8)' : 
                         activeChartTab.value === 'points' ? 'rgba(40, 167, 69, 0.8)' : 'rgba(255, 193, 7, 0.8)',
        borderColor: activeChartTab.value === 'quizzes' ? 'rgba(78, 115, 223, 1)' : 
                     activeChartTab.value === 'points' ? 'rgba(40, 167, 69, 1)' : 'rgba(255, 193, 7, 1)',
        borderWidth: 2,
        tension: activeChartTab.value === 'quizzes' ? 0 : 0.3,
        fill: activeChartTab.value !== 'quizzes',
        pointRadius: activeChartTab.value === 'quizzes' ? 4 : 3,
        pointHoverRadius: 6,
        pointBackgroundColor: activeChartTab.value === 'quizzes' ? 'rgba(78, 115, 223, 1)' : 
                              activeChartTab.value === 'points' ? 'rgba(40, 167, 69, 1)' : 'rgba(255, 193, 7, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2
      }
    ]
  };
};

const formatDate = (date) => {
  if (!date) return 'N/A';
  const dateObj = new Date(date);
  return isNaN(dateObj.getTime()) 
    ? 'Invalid Date' 
    : dateObj.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
};

const formatTime = (date) => {
  if (!date) return 'N/A';
  const dateObj = new Date(date);
  return isNaN(dateObj.getTime())
    ? 'Invalid Time'
    : dateObj.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true
      });
};

const getDaysLeft = (endDate) => {
  const today = new Date();
  const end = new Date(endDate);
  const diffTime = end - today;
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
};

const getProgressClass = (progress) => {
  if (progress < 25) return 'bg-danger';
  if (progress < 50) return 'bg-warning';
  if (progress < 75) return 'bg-info';
  return 'bg-success';
};

const addGoal = () => {
  goalForm.value = {
    id: null,
    title: '',
    target: 10,
    current: 0,
    unit: 'quizzes',
    endDate: new Date(new Date().setMonth(new Date().getMonth() + 1)).toISOString().split('T')[0]
  };
  editingGoal.value = null;
  showAddGoalModal.value = true;
};

const editGoal = (goal) => {
  goalForm.value = { ...goal };
  editingGoal.value = goal.id;
  showAddGoalModal.value = true;
};

const saveGoal = () => {
  if (editingGoal.value) {
    // Update existing goal
    const index = goals.value.findIndex(g => g.id === editingGoal.value);
    if (index !== -1) {
      goals.value[index] = { ...goalForm.value };
    }
  } else {
    // Add new goal
    const newGoal = {
      ...goalForm.value,
      id: Math.max(0, ...goals.value.map(g => g.id)) + 1,
      progress: 0
    };
    goals.value.push(newGoal);
  }
  closeGoalModal();
};

const deleteGoal = (id) => {
  if (confirm('Are you sure you want to delete this goal?')) {
    goals.value = goals.value.filter(goal => goal.id !== id);
  }
};

const closeGoalModal = () => {
  showAddGoalModal.value = false;
  editingGoal.value = null;
};


// Watchers
watch(activeChartTab, () => {
  // Reinitialize engagement chart when tab changes
  if (engagementChartInstance && typeof engagementChartInstance.destroy === 'function') {
    engagementChartInstance.destroy();
    engagementChartInstance = null;
  }
    nextTick(() => {
    if (engagementChartRef.value) {
      const ctx = engagementChartRef.value.getContext('2d');
      if (ctx) {
        const chartData = getEngagementChartData();
        const dataPoints = chartData.datasets[0].data;
        
        if (dataPoints && dataPoints.length > 0) {
      engagementChartInstance = new Chart(ctx, {
        type: activeChartTab.value === 'quizzes' ? 'bar' : 'line',
            data: chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
              interaction: {
                mode: 'index',
                intersect: false,
              },
          plugins: {
            legend: {
                  display: true,
              position: 'top',
            },
            tooltip: {
              mode: 'index',
              intersect: false,
                  callbacks: {
                    title: function(context) {
                      if (context && context.length > 0 && context[0].parsed && context[0].parsed.x) {
                        const date = new Date(context[0].parsed.x);
                        return date.toLocaleDateString('en-US', { 
                          year: 'numeric', 
                          month: 'short', 
                          day: 'numeric'
                        });
                      }
                      return '';
                    },
                    label: function(context) {
                      if (context.parsed && context.parsed.y !== null && context.parsed.y !== undefined) {
                        const label = context.dataset.label || '';
                        const value = context.parsed.y;
                        if (activeChartTab.value === 'time') {
                          return `${label}: ${value} minutes`;
                        }
                        return `${label}: ${value}`;
                      }
                      return '';
                    }
                  }
            }
          },
          scales: {
                x: {
                  type: 'time',
                  time: {
                    unit: 'day',
                    displayFormats: {
                      day: 'MMM dd',
                      week: 'MMM dd',
                      month: 'MMM yyyy'
                    },
                    tooltipFormat: 'MMM dd, yyyy'
                  },
                  title: {
                    display: true,
                    text: 'Date'
                  },
                  grid: {
                    display: true,
                    color: 'rgba(0, 0, 0, 0.05)'
                  },
                  ticks: {
                    autoSkip: true,
                    maxTicksLimit: 15,
                    maxRotation: 45,
                    minRotation: 0
                  }
                },
            y: {
              beginAtZero: true,
                  title: {
                    display: true,
                    text: activeChartTab.value === 'quizzes' ? 'Quizzes' : 
                          activeChartTab.value === 'points' ? 'Points' : 'Minutes'
                  },
              ticks: {
                precision: 0
                  },
                  grid: {
                    display: true,
                    color: 'rgba(0, 0, 0, 0.05)'
              }
            }
          }
        }
    });
        }
      }
  }
  });
});

// Lifecycle hooks
onMounted(() => {
  fetchMonthlyEngagement();
  
  // Add window resize event listener to handle chart resizing
  window.addEventListener('resize', () => {
    if (engagementChartInstance || categoryChartInstance || timeOfDayChartInstance) {
      initCharts();
    }
  });
});

onBeforeUnmount(() => {
  if (engagementChartInstance && typeof engagementChartInstance.destroy === 'function') {
    engagementChartInstance.destroy();
  }
  if (categoryChartInstance && typeof categoryChartInstance.destroy === 'function') {
    categoryChartInstance.destroy();
  }
  if (timeOfDayChartInstance && typeof timeOfDayChartInstance.destroy === 'function') {
    timeOfDayChartInstance.destroy();
  }
  window.removeEventListener('resize', initCharts);
});
</script>

<style scoped>
.monthly-engagement {
  padding: 1.5rem;
}

.card {
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
}

.progress {
  border-radius: 10px;
  height: 10px;
}

.progress-bar {
  border-radius: 10px;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.achievement-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.achievement-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.05);
}

.achievement-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-right: 1rem;
  flex-shrink: 0;
}

.achievement-details {
  flex: 1;
  min-width: 0;
}

.achievement-date {
  font-size: 0.75rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .monthly-engagement {
    padding: 1rem;
  }
  
  .achievements-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }
}

@media (max-width: 768px) {
  .achievements-grid {
    grid-template-columns: 1fr;
  }
  
  .achievement-item {
    padding: 0.5rem;
  }
  
  .achievement-badge {
    width: 40px;
    height: 40px;
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

/* Custom styling for the select dropdown */
select.form-select {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M2 5l6 6 6-6'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 16px 12px;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  padding-right: 2.25rem;
  border: 1px solid #d1d3e2;
  border-radius: 0.35rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

select.form-select:focus {
  border-color: #bac8f3;
  box-shadow: 0 0 0 0.25rem rgba(78, 115, 223, 0.25);
}

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
.bg-info { background-color: #17a2b8 !important; }
.bg-success { background-color: #28a745 !important; }
.bg-danger { background-color: #dc3545 !important; }
.bg-primary { background-color: #4e73df !important; }
.bg-secondary { background-color: #6c757d !important; }

/* Background subtle colors */
.bg-warning-subtle { background-color: #fff3cd !important; }
.bg-info-subtle { background-color: #d1ecf1 !important; }
.bg-success-subtle { background-color: #d4edda !important; }
.bg-danger-subtle { background-color: #f8d7da !important; }
.bg-primary-subtle { background-color: #d6e4ff !important; }
</style>
