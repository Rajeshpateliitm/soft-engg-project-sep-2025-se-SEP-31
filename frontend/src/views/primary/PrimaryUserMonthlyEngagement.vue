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
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h2 class="mb-1">Monthly Engagement</h2>
            <p class="text-muted mb-0">Track your monthly activity and participation</p>
          </div>
          <div class="d-flex gap-2">
            <select v-model="selectedYear" class="form-select form-select-sm" style="width: 120px;">
              <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
            </select>
            <div class="dropdown">
              <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" id="exportDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="bi bi-download me-1"></i> Export
              </button>
              <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="exportDropdown">
                <li><a class="dropdown-item" href="#" @click.prevent="exportData('pdf')"><i class="bi bi-file-earmark-pdf me-2"></i>PDF</a></li>
                <li><a class="dropdown-item" href="#" @click.prevent="exportData('csv')"><i class="bi bi-file-earmark-spreadsheet me-2"></i>CSV</a></li>
                <li><a class="dropdown-item" href="#" @click.prevent="exportData('print')"><i class="bi bi-printer me-2"></i>Print</a></li>
              </ul>
            </div>
          </div>
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
      <!-- Quiz Performance by Category -->
      <div class="col-lg-6 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <h5 class="mb-0">Quiz Performance by Category</h5>
          </div>
          <div class="card-body">
            <div class="chart-container" style="position: relative; height: 300px;">
              <canvas ref="categoryChartRef"></canvas>
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
            <router-link to="/activity-log" class="btn btn-sm btn-outline-primary">
              View All Activity
            </router-link>
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
                      class="badge" 
                      :class="activity.points > 0 ? 'bg-success' : 'bg-secondary'"
                    >
                      {{ activity.points > 0 ? '+' + activity.points : activity.points }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Goals & Achievements -->
    <div class="row mt-4">
      <div class="col-md-6 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Monthly Goals</h5>
            <button class="btn btn-sm btn-outline-primary" @click="showAddGoalModal = true">
              <i class="bi bi-plus-lg"></i> Add Goal
            </button>
          </div>
          <div class="card-body">
            <div v-if="goals.length > 0">
              <div v-for="(goal, index) in goals" :key="index" class="mb-3">
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <div>
                    <h6 class="mb-0">{{ goal.title }}</h6>
                    <small class="text-muted">{{ goal.progress }}% completed</small>
                  </div>
                  <div class="dropdown">
                    <button class="btn btn-sm btn-link text-muted p-0" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                      <i class="bi bi-three-dots-vertical"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end">
                      <li><a class="dropdown-item" href="#" @click.prevent="editGoal(goal)"><i class="bi bi-pencil me-2"></i>Edit</a></li>
                      <li><a class="dropdown-item" href="#" @click.prevent="deleteGoal(goal.id)"><i class="bi bi-trash me-2"></i>Delete</a></li>
                    </ul>
                  </div>
                </div>
                <div class="progress" style="height: 8px;">
                  <div 
                    class="progress-bar" 
                    :class="getProgressClass(goal.progress)" 
                    role="progressbar" 
                    :style="{ width: goal.progress + '%' }" 
                    :aria-valuenow="goal.progress" 
                    aria-valuemin="0" 
                    aria-valuemax="100"
                  ></div>
                </div>
                <div class="d-flex justify-content-between mt-1">
                  <small class="text-muted">{{ goal.current }}/{{ goal.target }} {{ goal.unit }}</small>
                  <small class="text-muted">{{ getDaysLeft(goal.endDate) }} days left</small>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <i class="bi bi-flag text-muted" style="font-size: 2rem; opacity: 0.5;"></i>
              <p class="text-muted mt-2 mb-0">No goals set for this month</p>
              <button class="btn btn-sm btn-outline-primary mt-2" @click="showAddGoalModal = true">
                Set Your First Goal
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <h5 class="mb-0">Recent Achievements</h5>
          </div>
          <div class="card-body">
            <div v-if="achievements.length > 0" class="achievements-grid">
              <div v-for="(achievement, index) in achievements" :key="index" class="achievement-item">
                <div class="achievement-badge" :class="'bg-' + achievement.rarity">
                  <i :class="'bi ' + achievement.icon + ' text-white'" style="font-size: 1.5rem;"></i>
                </div>
                <div class="achievement-details">
                  <h6 class="mb-0">{{ achievement.title }}</h6>
                  <small class="text-muted">{{ achievement.description }}</small>
                  <div class="achievement-date">
                    <small class="text-muted">{{ formatDate(achievement.date) }}</small>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <i class="bi bi-trophy text-muted" style="font-size: 2rem; opacity: 0.5;"></i>
              <p class="text-muted mt-2 mb-0">No achievements earned this month</p>
              <router-link to="/primary-dashboard/quiz" class="btn btn-sm btn-outline-primary mt-2">
                Take a Quiz to Earn Achievements
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Add/Edit Goal Modal -->
    <div v-if="showAddGoalModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingGoal ? 'Edit Goal' : 'Add New Goal' }}</h5>
            <button type="button" class="btn-close" @click="closeGoalModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveGoal">
              <div class="mb-3">
                <label for="goalTitle" class="form-label">Goal Title</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="goalTitle" 
                  v-model="goalForm.title"
                  required
                >
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="goalTarget" class="form-label">Target</label>
                  <div class="input-group">
                    <input 
                      type="number" 
                      class="form-control" 
                      id="goalTarget" 
                      v-model.number="goalForm.target"
                      min="1"
                      required
                    >
                    <span class="input-group-text">{{ goalForm.unit }}</span>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="goalUnit" class="form-label">Unit</label>
                  <select 
                    class="form-select" 
                    id="goalUnit"
                    v-model="goalForm.unit"
                    required
                  >
                    <option value="quizzes">Quizzes</option>
                    <option value="points">Points</option>
                    <option value="minutes">Minutes</option>
                    <option value="days">Days</option>
                  </select>
                </div>
              </div>
              <div class="mb-3">
                <label for="goalEndDate" class="form-label">End Date</label>
                <input 
                  type="date" 
                  class="form-control" 
                  id="goalEndDate" 
                  v-model="goalForm.endDate"
                  :min="new Date().toISOString().split('T')[0]"
                  required
                >
              </div>
              <div class="d-flex justify-content-end gap-2">
                <button type="button" class="btn btn-outline-secondary" @click="closeGoalModal">Cancel</button>
                <button type="submit" class="btn btn-primary">{{ editingGoal ? 'Update' : 'Save' }} Goal</button>
              </div>
            </form>
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
    
    // Update monthly engagement stats
    monthlyEngagement.value = {
      quizzes: data.monthly_engagement?.quizzes || 0,
      waste_logs: data.monthly_engagement?.waste_logs || 0,
      campaigns: data.monthly_engagement?.campaigns || 0
    };
    
    // Update daily trends
    dailyTrends.value = data.daily_trends || {};
    
    // Update activity breakdown
    activityBreakdown.value = [
      { name: 'Quizzes Taken', count: monthlyEngagement.value.quizzes, icon: 'bi-check-circle', variant: 'primary', description: 'Total quizzes completed' },
      { name: 'Waste Logs', count: monthlyEngagement.value.waste_logs, icon: 'bi-trash', variant: 'success', description: 'Total waste entries' },
      { name: 'Campaigns', count: monthlyEngagement.value.campaigns, icon: 'bi-calendar-event', variant: 'info', description: 'Campaigns participated' },
      { name: 'Points Earned', count: 0, icon: 'bi-star', variant: 'warning', description: 'Total points this month' }
    ];
    
    // Update engagement stats (calculate from data)
    engagementStats.value = {
      quizzesCompleted: monthlyEngagement.value.quizzes,
      quizzesChange: 0, // Could calculate from previous month
      averageScore: 0, // Get from quiz performance
      scoreChange: 0,
      currentStreak: 0, // Calculate from daily trends
      streakActive: false,
      ranking: 0, // Get from leaderboard
      rankingChange: 0
    };
    
    // Generate recent activities from daily trends
    generateRecentActivities();
    
    // Initialize charts after data is loaded
    await nextTick();
    setTimeout(() => {
      initCharts();
    }, 100);
  } catch (error) {
    console.error('Error fetching monthly engagement:', error);
  } finally {
    isLoading.value = false;
  }
};

// Generate recent activities from trends
const generateRecentActivities = () => {
  const activities = [];
  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  
  // Get quiz attempts and waste logs from trends
  Object.entries(dailyTrends.value).forEach(([day, data]) => {
    if (data.quizzes > 0) {
      activities.push({
        title: 'Quiz Completed',
        subtitle: 'Waste Management Quiz',
        details: `Completed ${data.quizzes} quiz${data.quizzes > 1 ? 'zes' : ''}`,
        points: data.quizzes * 10,
        timestamp: getDateForDay(day),
        icon: 'bi-check-circle',
        variant: 'primary'
      });
    }
    if (data.waste_logs > 0) {
      activities.push({
        title: 'Waste Logged',
        subtitle: 'Daily Waste Entry',
        details: `Logged ${data.waste_logs} entry${data.waste_logs > 1 ? 'ies' : ''}`,
        points: data.waste_logs * 5,
        timestamp: getDateForDay(day),
        icon: 'bi-trash',
        variant: 'success'
      });
    }
  });
  
  // Sort by timestamp (most recent first) and limit to 10
  recentActivities.value = activities
    .sort((a, b) => b.timestamp - a.timestamp)
    .slice(0, 10);
};

// Helper to get date for day name (returns date within last 7 days)
const getDateForDay = (dayName) => {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const today = new Date();
  const todayDay = today.getDay();
  const targetDay = days.indexOf(dayName);
  
  // Find the most recent occurrence of this day within the last 7 days
  let diff = targetDay - todayDay;
  if (diff > 0) {
    diff -= 7; // Go back to previous week
  }
  
  const date = new Date(today);
  date.setDate(today.getDate() + diff);
  date.setHours(12, 0, 0, 0); // Set to noon for consistent time
  return date;
};

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
  
  // Engagement Chart (Line/Bar)
  if (engagementChartRef.value) {
    const ctx1 = engagementChartRef.value.getContext('2d');
    if (ctx1) {
      engagementChartInstance = new Chart(ctx1, {
        type: activeChartTab.value === 'quizzes' ? 'bar' : 'line',
        data: getEngagementChartData(),
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
    }
  }
  
  // Category Performance Chart (Doughnut)
  if (categoryChartRef.value) {
    const ctx2 = categoryChartRef.value.getContext('2d');
    if (ctx2) {
      categoryChartInstance = new Chart(ctx2, {
        type: 'doughnut',
        data: {
          labels: ['Recycling', 'Composting', 'Reduction', 'Reuse', 'Hazardous Waste'],
          datasets: [{
            data: [85, 78, 65, 72, 90],
            backgroundColor: [
              'rgba(54, 162, 235, 0.8)',
              'rgba(75, 192, 192, 0.8)',
              'rgba(255, 206, 86, 0.8)',
              'rgba(153, 102, 255, 0.8)',
              'rgba(255, 99, 132, 0.8)'
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
            }
          },
          cutout: '70%'
        }
      });
    }
  }
  
  // Time of Day Activity (Radar)
  if (timeOfDayChartRef.value) {
    const ctx3 = timeOfDayChartRef.value.getContext('2d');
    if (ctx3) {
      timeOfDayChartInstance = new Chart(ctx3, {
        type: 'radar',
        data: {
          labels: ['12 AM', '3 AM', '6 AM', '9 AM', '12 PM', '3 PM', '6 PM', '9 PM'],
          datasets: [
            {
              label: 'This Week',
              data: [5, 2, 15, 25, 20, 30, 40, 25],
              backgroundColor: 'rgba(78, 115, 223, 0.2)',
              borderColor: 'rgba(78, 115, 223, 1)',
              pointBackgroundColor: 'rgba(78, 115, 223, 1)',
              pointBorderColor: '#fff',
              pointHoverBackgroundColor: '#fff',
              pointHoverBorderColor: 'rgba(78, 115, 223, 1)'
            },
            {
              label: 'Last Week',
              data: [3, 1, 10, 20, 25, 35, 30, 20],
              backgroundColor: 'rgba(110, 118, 135, 0.2)',
              borderColor: 'rgba(110, 118, 135, 1)',
              pointBackgroundColor: 'rgba(110, 118, 135, 1)',
              pointBorderColor: '#fff',
              pointHoverBackgroundColor: '#fff',
              pointHoverBorderColor: 'rgba(110, 118, 135, 1)'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              angleLines: {
                display: true
              },
              suggestedMin: 0,
              suggestedMax: 50
            }
          }
        }
      });
    }
  }
};

const getEngagementChartData = () => {
  // Use daily trends data from backend
  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const labels = [];
  const data = [];
  
  days.forEach(day => {
    if (dailyTrends.value[day]) {
      labels.push(day.substring(0, 3)); // Short day name
      switch (activeChartTab.value) {
        case 'quizzes':
          data.push(dailyTrends.value[day].quizzes || 0);
          break;
        case 'points':
          data.push((dailyTrends.value[day].quizzes || 0) * 10 + (dailyTrends.value[day].waste_logs || 0) * 5);
          break;
        case 'time':
          data.push((dailyTrends.value[day].quizzes || 0) * 5); // Estimate 5 min per quiz
          break;
      }
    } else {
      labels.push(day.substring(0, 3));
      data.push(0);
    }
  });
  
  return {
    labels,
    datasets: [
      {
        label: activeChartTab.value === 'quizzes' ? 'Quizzes' : 
               activeChartTab.value === 'points' ? 'Points' : 'Minutes',
        data,
        backgroundColor: activeChartTab.value === 'quizzes' ? 'rgba(78, 115, 223, 0.8)' : 
                         activeChartTab.value === 'points' ? 'rgba(40, 167, 69, 0.8)' : 'rgba(255, 193, 7, 0.8)',
        borderColor: activeChartTab.value === 'quizzes' ? 'rgba(78, 115, 223, 1)' : 
                     activeChartTab.value === 'points' ? 'rgba(40, 167, 69, 1)' : 'rgba(255, 193, 7, 1)',
        borderWidth: 1,
        tension: activeChartTab.value === 'quizzes' ? 0 : 0.3
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

const exportData = (format) => {
  // In a real app, this would generate and download a file
  alert(`Exporting data as ${format.toUpperCase()}...`);
};

// Watchers
watch(activeChartTab, () => {
  if (engagementChartInstance && typeof engagementChartInstance.destroy === 'function') {
    engagementChartInstance.destroy();
    engagementChartInstance = null;
  }
  nextTick(() => {
    if (engagementChartRef.value) {
      const ctx = engagementChartRef.value.getContext('2d');
      if (ctx) {
        engagementChartInstance = new Chart(ctx, {
          type: activeChartTab.value === 'quizzes' ? 'bar' : 'line',
          data: getEngagementChartData(),
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
