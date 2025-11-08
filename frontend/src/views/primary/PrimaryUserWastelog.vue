<template>
  <div class="wastelog-container">
    <div class="card shadow-sm mb-4">
      <div class="card-header bg-primary text-white">
        <h3 class="card-title mb-0">Log Your Waste</h3>
      </div>
      <div class="card-body">
        <form @submit.prevent="submitWasteLog" class="wastelog-form">
          <div class="row g-3">
            <div class="col-md-4">
              <label for="wetWaste" class="form-label">Wet Waste (kg)</label>
              <input 
                type="number" 
                class="form-control" 
                id="wetWaste" 
                v-model.number="wasteLog.wet_waste" 
                min="0" 
                step="0.1"
                placeholder="0.0"
              >
            </div>
            
            <div class="col-md-4">
              <label for="dryWaste" class="form-label">Dry Waste (kg)</label>
              <input 
                type="number" 
                class="form-control" 
                id="dryWaste" 
                v-model.number="wasteLog.dry_waste" 
                min="0" 
                step="0.1"
                placeholder="0.0"
              >
            </div>
            
            <div class="col-md-4">
              <label for="hazardousWaste" class="form-label">Hazardous Waste (kg)</label>
              <input 
                type="number" 
                class="form-control" 
                id="hazardousWaste" 
                v-model.number="wasteLog.hazardous_waste" 
                min="0" 
                step="0.1"
                placeholder="0.0"
              >
            </div>
            
            <div class="col-12">
              <label for="date" class="form-label">Date</label>
              <input 
                type="date" 
                class="form-control" 
                id="date" 
                v-model="wasteLog.log_date"
                required
              >
            </div>
            
            <div class="col-md-6">
              <div class="form-check">
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  id="separated" 
                  v-model="wasteLog.separated"
                >
                <label class="form-check-label" for="separated">
                  Waste was properly separated
                </label>
              </div>
            </div>
            
            <div class="col-md-6">
              <div class="form-check">
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  id="recycled" 
                  v-model="wasteLog.recycled"
                >
                <label class="form-check-label" for="recycled">
                  Waste was recycled/reused/donated
                </label>
              </div>
            </div>
            
            <div class="col-12">
              <label for="questionsDoubts" class="form-label">Questions/Doubts (Optional)</label>
              <textarea 
                class="form-control" 
                id="questionsDoubts" 
                rows="2" 
                v-model="wasteLog.questions_doubts"
                placeholder="Any questions about waste segregation or disposal..."
              ></textarea>
            </div>
            
            <div class="col-12">
              <label for="feedback" class="form-label">Feedback (Optional)</label>
              <textarea 
                class="form-control" 
                id="feedback" 
                rows="2" 
                v-model="wasteLog.feedback"
                placeholder="Any feedback or suggestions..."
              ></textarea>
            </div>
            
            <div class="col-12 mt-3">
              <div v-if="errorMessage" class="alert alert-danger" role="alert">
                {{ errorMessage }}
              </div>
              <div v-if="successMessage" class="alert alert-success" role="alert">
                {{ successMessage }}
              </div>
              <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                {{ isSubmitting ? 'Saving...' : 'Log Waste' }}
              </button>
              <button type="button" class="btn btn-outline-secondary ms-2" @click="resetForm">
                Reset
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
    
    <div class="recent-entries mt-4">
      <h4 class="mb-3">Recent Entries</h4>
      <div v-if="recentEntries.length === 0" class="text-center py-4 text-muted">
        <p>No waste entries logged yet. Start by adding your first entry above.</p>
      </div>
      <div v-else class="table-responsive">
        <table class="table table-hover">
          <thead class="table-light">
            <tr>
              <th>Date</th>
              <th>Category</th>
              <th>Weight (kg)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in recentEntries" :key="entry.id">
              <td>{{ formatDate(entry.log_date) }}</td>
              <td>
                <span class="badge" :class="getWasteTypeBadge(entry.category)">
                  {{ formatWasteType(entry.category) }}
                </span>
              </td>
              <td>{{ entry.quantity_kg }} kg</td>
              <td>
                <div v-if="entry.separated" class="badge bg-success me-1">Separated</div>
                <div v-if="entry.recycled" class="badge bg-info">Recycled</div>
                <span v-if="!entry.separated && !entry.recycled" class="text-muted">—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../../services/api';
import { useRouter } from 'vue-router';

const router = useRouter();

const wasteLog = ref({
  wet_waste: 0,
  dry_waste: 0,
  hazardous_waste: 0,
  log_date: new Date().toISOString().split('T')[0],
  separated: false,
  recycled: false,
  questions_doubts: '',
  feedback: ''
});

const recentEntries = ref([]);
const isSubmitting = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

// Fetch waste logs from backend
const fetchWasteLogs = async () => {
  try {
    const response = await api.get('/primary/waste-logs?limit=20');
    recentEntries.value = response.data.waste_logs || [];
  } catch (error) {
    console.error('Error fetching waste logs:', error);
  }
};

// Load entries from backend on component mount
onMounted(() => {
  fetchWasteLogs();
});

const submitWasteLog = async () => {
  // Validate that at least one waste type has a value
  if (wasteLog.value.wet_waste <= 0 && wasteLog.value.dry_waste <= 0 && wasteLog.value.hazardous_waste <= 0) {
    errorMessage.value = 'Please enter at least one waste type with a value greater than 0.';
    return;
  }
  
  isSubmitting.value = true;
  errorMessage.value = '';
  successMessage.value = '';
  
  try {
    const response = await api.post('/primary/waste-log', {
      wet_waste: wasteLog.value.wet_waste || 0,
      dry_waste: wasteLog.value.dry_waste || 0,
      hazardous_waste: wasteLog.value.hazardous_waste || 0,
      log_date: wasteLog.value.log_date,
      separated: wasteLog.value.separated,
      recycled: wasteLog.value.recycled,
      questions_doubts: wasteLog.value.questions_doubts || null,
      feedback: wasteLog.value.feedback || null
    });
    
    successMessage.value = `Waste logged successfully! You earned points. Total points: ${response.data.points}`;
    
    // Reset form
    resetForm();
    
    // Refresh the list
    await fetchWasteLogs();
    
    // Clear success message after 5 seconds
    setTimeout(() => {
      successMessage.value = '';
    }, 5000);
  } catch (error) {
    console.error('Error logging waste:', error);
    errorMessage.value = error.response?.data?.error || 'Failed to log waste. Please try again.';
  } finally {
    isSubmitting.value = false;
  }
};

const resetForm = () => {
  wasteLog.value = {
    wet_waste: 0,
    dry_waste: 0,
    hazardous_waste: 0,
    log_date: new Date().toISOString().split('T')[0],
    separated: false,
    recycled: false,
    questions_doubts: '',
    feedback: ''
  };
  errorMessage.value = '';
  successMessage.value = '';
};

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

const formatWasteType = (type) => {
  return type.charAt(0).toUpperCase() + type.slice(1);
};

const getWasteTypeBadge = (type) => {
  const badgeClasses = {
    wet: 'bg-success',
    dry: 'bg-info',
    hazardous: 'bg-danger',
    other: 'bg-secondary'
  };
  
  return badgeClasses[type?.toLowerCase()] || 'bg-secondary';
};
</script>

<style scoped>
.wastelog-container {
  max-width: 1000px;
  margin: 0 auto;
}

.wastelog-form {
  max-width: 800px;
  margin: 0 auto;
}

.table th, .table td {
  vertical-align: middle;
}

.badge {
  font-size: 0.85em;
  padding: 0.4em 0.75em;
  border-radius: 50rem;
}

.btn-sm i {
  font-size: 0.9em;
}

.table-responsive {
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.table {
  margin-bottom: 0;
}

.table thead th {
  background-color: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  color: #6c757d;
}

.table-hover tbody tr:hover {
  background-color: rgba(0, 0, 0, 0.02);
}

@media (max-width: 768px) {
  .wastelog-container {
    padding: 0 10px;
  }
  
  .table-responsive {
    border: 1px solid #dee2e6;
    border-radius: 0.25rem;
  }
}
</style>
