<template>
  <div class="genai-summary-container mb-4">
    <button 
      class="btn btn-genai w-100 d-flex align-items-center justify-content-center gap-2" 
      @click="analyzeData"
      :disabled="loading"
    >
      <i class="bi bi-stars"></i>
      <span v-if="!loading">Analyze with AI</span>
      <span v-else>Analyzing...</span>
    </button>

    <div v-if="analysis" class="alert alert-primary mt-3 fade show" role="alert">
      <div class="d-flex justify-content-between align-items-start">
        <h6 class="alert-heading mb-2"><i class="bi bi-robot me-2"></i>AI Analysis</h6>
        <button type="button" class="btn-close" @click="analysis = null" aria-label="Close"></button>
      </div>
      <div class="analysis-content" v-html="analysis"></div>
    </div>

    <div v-if="error" class="alert alert-danger mt-3 fade show" role="alert">
      {{ error }}
      <button type="button" class="btn-close float-end" @click="error = null" aria-label="Close"></button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '../services/api';

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  context: {
    type: String,
    default: 'Dashboard Data'
  }
});

const loading = ref(false);
const analysis = ref(null);
const error = ref(null);

const analyzeData = async () => {
  loading.value = true;
  error.value = null;
  analysis.value = null;

  try {
    const response = await api.post('/genai/dashboard-analysis', {
      data: props.data,
      context: props.context
    }, {
      timeout: 35000
    });

    if (response.data && response.data.analysis) {
      analysis.value = response.data.analysis;
    } else {
      throw new Error('No analysis received');
    }
  } catch (err) {
    console.error('Analysis failed:', err);
    if (err.response && err.response.data && err.response.data.error) {
      error.value = err.response.data.error;
    } else {
      error.value = 'Unable to analyze the data at this time. Please try again later.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.btn-genai {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  transition: all 0.3s ease;
  font-weight: 500;
}

.btn-genai:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4);
  color: white;
}

.btn-genai:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.analysis-content {
  font-size: 0.9rem;
  line-height: 1.4;
  color: #2c3e50;
}

.analysis-content :deep(p) {
  margin-bottom: 0.5rem;
}

.analysis-content :deep(ul) {
  margin-bottom: 0;
  padding-left: 1.2rem;
}

.analysis-content :deep(li) {
  margin-bottom: 0.25rem;
}

.analysis-content :deep(strong) {
  color: #0d6efd;
  font-weight: 600;
}
</style>
