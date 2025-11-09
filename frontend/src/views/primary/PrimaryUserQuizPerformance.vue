<template>
  <div class="quiz-performance">
    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Loading quiz performance data...</p>
    </div>

    <!-- Content -->
    <template v-else>
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
          <h2 class="mb-0">Quiz Performance</h2>
          <div class="d-flex gap-2">
            <select v-model="timeRange" class="form-select form-select-sm" style="width: auto;">
              <option value="7">Last 7 Days</option>
              <option value="30">Last 30 Days</option>
              <option value="90">Last 90 Days</option>
              <option value="all">All Time</option>
            </select>
            <button class="btn btn-sm btn-outline-primary" @click="exportData">
              <i class="bi bi-download me-1"></i> Export
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="row g-4 mb-4">
      <div class="col-md-3 col-sm-6">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-2">Average Score</h6>
                <h3 class="mb-0">{{ stats.averageScore }}%</h3>
                <span :class="getTrendClass(stats.scoreTrend)">
                  <i :class="getTrendIcon(stats.scoreTrend)"></i> {{ Math.abs(stats.scoreTrend) }}%
                </span>
              </div>
              <div class="bg-primary bg-opacity-10 p-3 rounded-circle">
                <i class="bi bi-graph-up text-primary" style="font-size: 1.5rem;"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-3 col-sm-6">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-2">Quizzes Taken</h6>
                <h3 class="mb-0">{{ stats.quizzesTaken }}</h3>
                <span :class="getTrendClass(stats.quizzesTrend)">
                  <i :class="getTrendIcon(stats.quizzesTrend)"></i> {{ Math.abs(stats.quizzesTrend) }}%
                </span>
              </div>
              <div class="bg-success bg-opacity-10 p-3 rounded-circle">
                <i class="bi bi-check2-circle text-success" style="font-size: 1.5rem;"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-3 col-sm-6">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-2">Correct Answers</h6>
                <h3 class="mb-0">{{ stats.correctAnswers }}/{{ stats.totalQuestions }}</h3>
                <span :class="getTrendClass(stats.accuracyTrend)">
                  <i :class="getTrendIcon(stats.accuracyTrend)"></i> {{ Math.abs(stats.accuracyTrend) }}%
                </span>
              </div>
              <div class="bg-info bg-opacity-10 p-3 rounded-circle">
                <i class="bi bi-check-all text-info" style="font-size: 1.5rem;"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-3 col-sm-6">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-2">Best Category</h6>
                <h3 class="mb-0">{{ stats.bestCategory || 'N/A' }}</h3>
                <span class="text-success">{{ stats.bestCategoryScore }}% Accuracy</span>
              </div>
              <div class="bg-warning bg-opacity-10 p-3 rounded-circle">
                <i class="bi bi-trophy-fill text-warning" style="font-size: 1.5rem;"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="row g-4 mb-4">
      <!-- Score Trend Chart -->
      <div class="col-lg-8">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-header bg-white border-0">
            <h5 class="mb-0">Score Trend</h5>
          </div>
          <div class="card-body">
            <div class="chart-container" style="position: relative; height: 300px;">
              <canvas ref="scoreTrendChartRef"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Category Performance -->
      <div class="col-lg-4">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-header bg-white border-0">
            <h5 class="mb-0">Category Performance</h5>
          </div>
          <div class="card-body">
            <div class="chart-container" style="position: relative; height: 300px;">
              <canvas ref="categoryChartRef"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Quizzes -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
        <h5 class="mb-0">Recent Quiz Attempts</h5>
        <router-link to="/primary-dashboard/quiz" class="btn btn-sm btn-outline-primary">
          Take New Quiz
        </router-link>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Date</th>
                <th>Quiz</th>
                <th>Score</th>
                <th>Time Spent</th>
                <th>Correct/Total</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(attempt, index) in recentAttempts" :key="index">
                <td>{{ formatDate(attempt.date) }}</td>
                <td>{{ attempt.quizName }}</td>
                <td>
                  <div class="d-flex align-items-center">
                    <div class="progress flex-grow-1 me-2" style="height: 6px;">
                      <div 
                        class="progress-bar" 
                        :class="getScoreClass(attempt.score)"
                        role="progressbar" 
                        :style="{ width: attempt.score + '%' }"
                        :aria-valuenow="attempt.score" 
                        aria-valuemin="0" 
                        aria-valuemax="100"
                      ></div>
                    </div>
                    <span class="fw-medium">{{ attempt.score }}%</span>
                  </div>
                </td>
                <td>{{ attempt.timeSpent }}</td>
                <td>{{ attempt.correct }}/{{ attempt.total }}</td>
                <td>
                  <span class="badge" :class="getStatusClass(attempt.status)">
                    {{ attempt.status }}
                  </span>
                </td>
                <td>
                  <button class="btn btn-sm btn-outline-primary" @click="viewDetails(attempt.id)">
                    <i class="bi bi-eye"></i> View
                  </button>
                </td>
              </tr>
              <tr v-if="recentAttempts.length === 0">
                <td colspan="7" class="text-center py-4">
                  <div class="text-muted">No quiz attempts found. <router-link to="/primary-dashboard/quiz">Take a quiz</router-link> to see your performance.</div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="card-footer bg-white border-0 d-flex justify-content-end">
        <button class="btn btn-link text-decoration-none" @click="viewAllAttempts">
          View All Attempts <i class="bi bi-arrow-right ms-1"></i>
        </button>
      </div>
    </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onBeforeUnmount, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';
import { useRouter } from 'vue-router';
import api from '../../services/api';

// Register Chart.js components
Chart.register(...registerables);

const router = useRouter();
const scoreTrendChartRef = ref(null);
const categoryChartRef = ref(null);
let scoreTrendChart = null;
let categoryChart = null;

const timeRange = ref('30');
const stats = ref({
  averageScore: 0,
  scoreTrend: 0,
  quizzesTaken: 0,
  quizzesTrend: 0,
  correctAnswers: 0,
  totalQuestions: 0,
  accuracyTrend: 0,
  bestCategory: 'N/A',
  bestCategoryScore: 0,
  worstCategory: 'N/A',
  worstCategoryScore: 0
});

const recentAttempts = ref([]);
const isLoading = ref(true);

// Fetch quiz performance data
const fetchQuizPerformance = async () => {
  try {
    isLoading.value = true;
    const response = await api.get('/primary/quiz/performance');
    const data = response.data;
    
    // Calculate stats
    const pastQuizzes = data.past_quizzes || [];
    const totalCorrect = pastQuizzes.reduce((sum, q) => sum + q.score, 0);
    const totalQuestions = pastQuizzes.reduce((sum, q) => sum + q.total_questions, 0);
    const categoryBreakdown = data.category_breakdown || {};
    const categoryKeys = Object.keys(categoryBreakdown);
    const categoryValues = Object.values(categoryBreakdown);
    
    stats.value = {
      averageScore: data.average_quiz_score || data.overall_accuracy || 0,
      scoreTrend: 0, // Calculate from previous attempts if needed
      quizzesTaken: pastQuizzes.length,
      quizzesTrend: 0,
      correctAnswers: totalCorrect,
      totalQuestions: totalQuestions,
      accuracyTrend: 0,
      bestCategory: categoryKeys.length > 0 ? categoryKeys[0] : 'N/A',
      bestCategoryScore: categoryValues.length > 0 ? Math.max(...categoryValues) : 0,
      worstCategory: categoryKeys.length > 0 ? categoryKeys[categoryKeys.length - 1] : 'N/A',
      worstCategoryScore: categoryValues.length > 0 ? Math.min(...categoryValues) : 0
    };
    
    // Update recent attempts
    recentAttempts.value = (data.past_quizzes || []).slice(0, 10).map(attempt => ({
      id: attempt.id,
      date: attempt.date,
      quizName: 'Waste Management Quiz',
      score: attempt.percentage,
      timeSpent: 'N/A',
      correct: attempt.score,
      total: attempt.total_questions,
      status: 'Completed'
    }));
    
    // Initialize charts after data is loaded and DOM is ready
    await nextTick();
    // Small delay to ensure canvas elements are rendered
    setTimeout(() => {
      initCharts();
    }, 100);
  } catch (error) {
    console.error('Error fetching quiz performance:', error);
  } finally {
    isLoading.value = false;
  }
};

// Chart data
const scoreTrendData = computed(() => {
  const attempts = recentAttempts.value.slice(0, 10).reverse();
  if (attempts.length === 0) {
    return {
      labels: ['No Data'],
      datasets: [
        {
          label: 'Your Score',
          data: [0],
          borderColor: '#4e73df',
          backgroundColor: 'rgba(78, 115, 223, 0.1)',
          tension: 0.3,
          fill: true
        }
      ]
    };
  }
  return {
    labels: attempts.map((_, index) => `Quiz ${index + 1}`),
    datasets: [
      {
        label: 'Your Score',
        data: attempts.map(a => a.score),
        borderColor: '#4e73df',
        backgroundColor: 'rgba(78, 115, 223, 0.1)',
        tension: 0.3,
        fill: true
      }
    ]
  };
});

const categoryData = computed(() => {
  const breakdown = stats.value.bestCategory !== 'N/A' ? {
    [stats.value.bestCategory]: stats.value.bestCategoryScore
  } : {};
  
  const labels = Object.keys(breakdown);
  const data = Object.values(breakdown);
  
  if (labels.length === 0) {
    return {
      labels: ['No Data'],
      datasets: [{
        data: [100],
        backgroundColor: ['rgba(200, 200, 200, 0.8)'],
        borderColor: '#fff',
        borderWidth: 2
      }]
    };
  }
  
  return {
    labels: labels,
    datasets: [{
      data: data,
      backgroundColor: [
        'rgba(78, 115, 223, 0.8)',
        'rgba(28, 200, 138, 0.8)',
        'rgba(54, 185, 204, 0.8)',
        'rgba(246, 194, 62, 0.8)',
        'rgba(231, 74, 59, 0.8)'
      ],
      borderColor: '#fff',
      borderWidth: 2
    }]
  };
});

// Format date
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

// Get trend class based on value (positive/negative)
const getTrendClass = (value) => {
  return value >= 0 ? 'text-success' : 'text-danger';
};

// Get trend icon
const getTrendIcon = (value) => {
  return value >= 0 ? 'bi-arrow-up' : 'bi-arrow-down';
};

// Get score class based on percentage
const getScoreClass = (score) => {
  if (score >= 80) return 'bg-success';
  if (score >= 60) return 'bg-info';
  if (score >= 40) return 'bg-warning';
  return 'bg-danger';
};

// Get status class
const getStatusClass = (status) => {
  const classes = {
    'Completed': 'bg-success',
    'In Progress': 'bg-warning',
    'Failed': 'bg-danger',
    'Expired': 'bg-secondary'
  };
  return classes[status] || 'bg-secondary';
};

// View quiz details
const viewDetails = (id) => {
  router.push(`/quiz/attempt/${id}`);
};

// View all attempts
const viewAllAttempts = () => {
  // In a real app, this would navigate to a detailed attempts page
  console.log('View all attempts');
};

// Export data
const exportData = () => {
  // In a real app, this would generate and download a CSV/PDF
  console.log('Exporting data...');
  // Simulate export
  setTimeout(() => {
    alert('Your data has been exported successfully!');
  }, 1000);
};

// Initialize charts
const initCharts = () => {
  // Destroy existing charts if they exist
  if (scoreTrendChart && typeof scoreTrendChart.destroy === 'function') {
    scoreTrendChart.destroy();
    scoreTrendChart = null;
  }
  if (categoryChart && typeof categoryChart.destroy === 'function') {
    categoryChart.destroy();
    categoryChart = null;
  }

  // Score Trend Chart (Line)
  if (scoreTrendChartRef.value) {
    const scoreCtx = scoreTrendChartRef.value.getContext('2d');
    if (scoreCtx && scoreTrendData.value && scoreTrendData.value.datasets && scoreTrendData.value.datasets[0] && scoreTrendData.value.datasets[0].data.length > 0) {
      scoreTrendChart = new Chart(scoreCtx, {
        type: 'line',
        data: scoreTrendData.value,
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
              max: 100,
              ticks: {
                callback: function(value) {
                  return value + '%';
                }
              }
            }
          }
        }
      });
    }
  }

  // Category Performance Chart (Doughnut)
  if (categoryChartRef.value) {
    const categoryCtx = categoryChartRef.value.getContext('2d');
    if (categoryCtx && categoryData.value && categoryData.value.datasets && categoryData.value.datasets[0] && categoryData.value.datasets[0].data.length > 0) {
      categoryChart = new Chart(categoryCtx, {
        type: 'doughnut',
        data: categoryData.value,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '70%',
          plugins: {
            legend: {
              position: 'right',
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `${context.label}: ${context.raw}%`;
                }
              }
            }
          }
        }
      });
    }
  }
};

// Watch for time range changes
watch(timeRange, () => {
  fetchQuizPerformance();
});

// Initialize component
onMounted(() => {
  fetchQuizPerformance();
  
  // Add resize event listener to handle chart resizing
  window.addEventListener('resize', initCharts);
});

// Clean up
onBeforeUnmount(() => {
  if (scoreTrendChart && typeof scoreTrendChart.destroy === 'function') {
    scoreTrendChart.destroy();
  }
  if (categoryChart && typeof categoryChart.destroy === 'function') {
    categoryChart.destroy();
  }
  window.removeEventListener('resize', initCharts);
});
</script>

<style scoped>
.quiz-performance {
  padding: 1.5rem;
}

.card {
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
}

.card-header {
  background-color: #fff;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 1.25rem 1.5rem;
  border-top-left-radius: 0.5rem !important;
  border-top-right-radius: 0.5rem !important;
}

.card-body {
  padding: 1.5rem;
}

.table th, .table td {
  padding: 1rem 1.5rem;
  vertical-align: middle;
}

.badge {
  font-weight: 500;
  padding: 0.35em 0.65em;
  font-size: 0.75em;
  letter-spacing: 0.5px;
}

.progress {
  height: 0.5rem;
  border-radius: 1rem;
  background-color: #eaecf4;
}

.progress-bar {
  border-radius: 1rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .quiz-performance {
    padding: 0.75rem;
  }
  
  .card-header, .card-body, .table th, .table td {
    padding: 0.75rem;
  }
  
  .btn {
    padding: 0.375rem 0.75rem;
    font-size: 0.9rem;
  }
  
  h2 {
    font-size: 1.5rem;
  }
  
  h5 {
    font-size: 1.1rem;
  }
}

/* Custom scrollbar for table */
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

/* Hover effects */
.table-hover > tbody > tr:hover {
  background-color: rgba(0, 0, 0, 0.02);
  cursor: pointer;
}

/* Animation for cards */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.card {
  animation: fadeIn 0.3s ease-out forwards;
}

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
</style>
