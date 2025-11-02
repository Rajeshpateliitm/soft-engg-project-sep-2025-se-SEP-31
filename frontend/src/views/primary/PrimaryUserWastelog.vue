<template>
  <div class="wastelog-container">
    <div class="card shadow-sm mb-4">
      <div class="card-header bg-primary text-white">
        <h3 class="card-title mb-0">Log Your Waste</h3>
      </div>
      <div class="card-body">
        <form @submit.prevent="submitWasteLog" class="wastelog-form">
          <div class="row g-3">
            <div class="col-md-6">
              <label for="wasteType" class="form-label">Waste Type</label>
              <select class="form-select" id="wasteType" v-model="wasteLog.type" required>
                <option value="" disabled>Select waste type</option>
                <option value="plastic">Plastic</option>
                <option value="paper">Paper</option>
                <option value="glass">Glass</option>
                <option value="metal">Metal</option>
                <option value="organic">Organic</option>
                <option value="ewaste">E-Waste</option>
                <option value="hazardous">Hazardous</option>
                <option value="other">Other</option>
              </select>
            </div>
            
            <div class="col-md-6">
              <label for="weight" class="form-label">Weight (kg)</label>
              <input 
                type="number" 
                class="form-control" 
                id="weight" 
                v-model.number="wasteLog.weight" 
                min="0.1" 
                step="0.1"
                required
              >
            </div>
            
            <div class="col-12">
              <label for="date" class="form-label">Date</label>
              <input 
                type="date" 
                class="form-control" 
                id="date" 
                v-model="wasteLog.date"
                required
              >
            </div>
            
            <div class="col-12">
              <label for="notes" class="form-label">Notes (Optional)</label>
              <textarea 
                class="form-control" 
                id="notes" 
                rows="3" 
                v-model="wasteLog.notes"
                placeholder="Any additional details about this waste..."
              ></textarea>
            </div>
            
            <div class="col-12 mt-3">
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
              <th>Type</th>
              <th>Weight (kg)</th>
              <th>Notes</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(entry, index) in recentEntries" :key="index">
              <td>{{ formatDate(entry.date) }}</td>
              <td>
                <span class="badge" :class="getWasteTypeBadge(entry.type)">
                  {{ formatWasteType(entry.type) }}
                </span>
              </td>
              <td>{{ entry.weight }} kg</td>
              <td>{{ entry.notes || '—' }}</td>
              <td>
                <button 
                  class="btn btn-sm btn-outline-danger"
                  @click="deleteEntry(index)"
                  title="Delete entry"
                >
                  <i class="bi bi-trash"></i>
                </button>
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

const wasteLog = ref({
  type: '',
  weight: '',
  date: new Date().toISOString().split('T')[0],
  notes: ''
});

const recentEntries = ref([]);
const isSubmitting = ref(false);

// Load saved entries from localStorage on component mount
onMounted(() => {
  const savedEntries = localStorage.getItem('wasteLogEntries');
  if (savedEntries) {
    recentEntries.value = JSON.parse(savedEntries);
  }
});

const submitWasteLog = () => {
  isSubmitting.value = true;
  
  // Simulate API call
  setTimeout(() => {
    const newEntry = { ...wasteLog.value };
    recentEntries.value.unshift(newEntry);
    
    // Save to localStorage
    localStorage.setItem('wasteLogEntries', JSON.stringify(recentEntries.value));
    
    // Reset form
    resetForm();
    isSubmitting.value = false;
    
    // Show success message
    alert('Waste entry logged successfully!');
  }, 1000);
};

const resetForm = () => {
  wasteLog.value = {
    type: '',
    weight: '',
    date: new Date().toISOString().split('T')[0],
    notes: ''
  };
};

const deleteEntry = (index) => {
  if (confirm('Are you sure you want to delete this entry?')) {
    recentEntries.value.splice(index, 1);
    localStorage.setItem('wasteLogEntries', JSON.stringify(recentEntries.value));
  }
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
    plastic: 'bg-info text-dark',
    paper: 'bg-light text-dark',
    glass: 'bg-primary',
    metal: 'bg-secondary',
    organic: 'bg-success',
    ewaste: 'bg-warning text-dark',
    hazardous: 'bg-danger',
    other: 'bg-dark'
  };
  
  return badgeClasses[type] || 'bg-secondary';
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
