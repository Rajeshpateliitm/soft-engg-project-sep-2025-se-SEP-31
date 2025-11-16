<template>
  
  <div class="primary-user-quiz">
    <!-- <button class="btn btn-primary" @click="startRandomQuiz">
  Try Random Quiz
</button> -->
<div class="quiz-header d-flex justify-content-between align-items-center mb-4">

  <!-- LEFT SIDE TEXT -->
  <h2 class="fw-bold m-0">Waste Management Quiz</h2>

  <!-- RIGHT SIDE BUTTON -->
  <button class="btn btn-primary" @click="startRandomQuiz">
    Try Random Quiz
  </button>

</div>

<!-- FULLSCREEN LOADING OVERLAY -->
<div v-if="loading" class="loading-overlay">
  <div class="spinner"></div>
  <p class="loading-text">Generating your random quiz…</p>
</div>


    <div class="quiz-container">
      <!-- Quiz Header -->
       
      <div class="quiz-header text-center mb-4">
        <!-- <h2 class="fw-bold">Waste Management Quiz</h2> -->
        <div class="quiz-progress">
          
          <div class="progress" style="height: 10px;">
            <div 
              class="progress-bar bg-success" 
              role="progressbar" 
              :style="{ width: progress + '%' }"
              :aria-valuenow="progress" 
              aria-valuemin="0" 
              aria-valuemax="100"
            ></div>
          </div>
          <div class="d-flex justify-content-between mt-2">
            <span>Question {{ currentQuestionIndex + 1 }} of {{ questions.length || 0 }}</span>
            <span v-if="!quizCompleted">Score: {{ score }}/{{ questions.length || 0 }}</span>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3">Loading quiz questions...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="errorMessage && questions.length === 0" class="alert alert-danger" role="alert">
        {{ errorMessage }}
        <button class="btn btn-primary mt-2" @click="fetchQuestions">Retry</button>
      </div>

      <!-- Quiz Content -->
      <div v-else-if="!quizCompleted && questions.length > 0 && currentQuestion" class="quiz-content">
        <div class="question-card card shadow-sm mb-4">
          <div class="card-body">
            <h4 class="question-text mb-4">{{ currentQuestion.question_text }}</h4>
            
            <div v-if="currentQuestion.image" class="question-image mb-4">
              <img 
                :src="currentQuestion.image" 
                :alt="'Question ' + (currentQuestionIndex + 1)" 
                class="img-fluid rounded"
              >
            </div>

            <div class="options-container">
              <div 
                v-for="(option, index) in currentQuestion.options" 
                :key="index"
                class="option-item mb-3"
                :class="{ 
                  'selected': selectedOption === index,
                  'correct': showFeedback && option.is_correct,
                  'incorrect': showFeedback && selectedOption === index && !option.is_correct
                }"
                @click="selectOption(index)"
              >
                <div class="option-content">
                  <span class="option-letter">{{ String.fromCharCode(65 + index) }}.</span>
                  <span class="option-text">{{ option.option_text }}</span>
                </div>
                <div v-if="showFeedback" class="feedback-icon">
                  <i 
                    v-if="option.is_correct" 
                    class="bi bi-check-circle-fill text-success"
                  ></i>
                  <i 
                    v-else-if="selectedOption === index && !option.is_correct"
                    class="bi bi-x-circle-fill text-danger"
                  ></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Navigation Buttons -->
        <div class="quiz-navigation d-flex justify-content-between">
          <button 
            class="btn btn-outline-primary" 
            :disabled="currentQuestionIndex === 0"
            @click="previousQuestion"
          >
            <i class="bi bi-arrow-left me-1"></i> Previous
          </button>
          
          <button 
            v-if="!showFeedback"
            class="btn btn-primary" 
            :disabled="selectedOption === null"
            @click="checkAnswer"
          >
            Submit Answer
          </button>
          
          <button 
            v-else
            class="btn btn-primary" 
            @click="nextQuestion"
          >
            {{ isLastQuestion ? 'Finish Quiz' : 'Next Question' }}
          </button>
        </div>
      </div>

      <!-- Quiz Results -->
      <div v-else class="quiz-results text-center">
        <div class="card shadow-sm">
          <div class="card-body p-5">
            <div class="result-icon mb-4">
              <i class="bi bi-trophy-fill" style="font-size: 4rem; color: #ffc107;"></i>
            </div>
            <h3 class="mb-3">Quiz Completed!</h3>
            <p class="lead">Your Score: {{ score }}/{{ questions.length || 0 }}</p>
            <p v-if="submittedScore" class="text-success mb-2">
              <strong>Points Earned: {{ submittedScore.points_earned }}</strong>
            </p>
            <p class="text-muted mb-4">
              {{ getResultMessage }}
            </p>
            <div v-if="errorMessage" class="alert alert-warning mb-3">
              {{ errorMessage }}
            </div>
            <div class="d-flex justify-content-center gap-3">
              <button class="btn btn-primary" @click="restartQuiz">
                <i class="bi bi-arrow-repeat me-2"></i>Retake Quiz
              </button>
              <router-link to="/primary-dashboard" class="btn btn-outline-secondary">
                <i class="bi bi-house-door me-2"></i>Back to Dashboard
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../../services/api';

const router = useRouter();

const questions = ref([]);
const userAnswers = ref({}); // Store {question_id: selected_option_id}
const currentQuestionIndex = ref(0);
const selectedOption = ref(null);
const score = ref(0);
const showFeedback = ref(false);
const quizCompleted = ref(false);
const isLoading = ref(true);
const errorMessage = ref('');
const submittedScore = ref(null);

// Fetch questions from backend
const fetchQuestions = async () => {
  try {
    isLoading.value = true;
    const response = await api.get('/primary/quiz/questions?limit=10');
    questions.value = response.data.questions;
    
    if (questions.value.length === 0) {
      errorMessage.value = 'No quiz questions available. Please try again later.';
    }
  } catch (error) {
    console.error('Error fetching questions:', error);
    errorMessage.value = 'Failed to load quiz questions. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchQuestions();
});

const currentQuestion = computed(() => {
  if (questions.value.length === 0 || currentQuestionIndex.value >= questions.value.length) {
    return null;
  }
  return questions.value[currentQuestionIndex.value];
});
const isLastQuestion = computed(() => {
  if (questions.value.length === 0) return false;
  return currentQuestionIndex.value === questions.value.length - 1;
});
const progress = computed(() => {
  if (questions.value.length === 0) return 0;
  return ((currentQuestionIndex.value + 1) / questions.value.length) * 100;
});
const getResultMessage = computed(() => {
  if (questions.value.length === 0) return '';
  const percentage = (score.value / questions.value.length) * 100;
  if (percentage >= 80) return 'Excellent! You\'re a waste management expert!';
  if (percentage >= 60) return 'Good job! You know quite a bit about waste management.';
  if (percentage >= 40) return 'Not bad! Keep learning about proper waste disposal.';
  return 'Keep trying! Check out our resources to learn more about waste management.';
});

const selectOption = (index) => {
  if (!showFeedback.value && !quizCompleted.value && currentQuestion.value) {
    selectedOption.value = index;
    
    // Store the answer
    const question = currentQuestion.value;
    if (question && question.options && question.options[index]) {
      const selectedOptionObj = question.options[index];
      userAnswers.value[question.id] = selectedOptionObj.id;
    }
  }
};

const checkAnswer = () => {
  if (selectedOption.value === null || !currentQuestion.value) return;
  
  showFeedback.value = true;
  
  const question = currentQuestion.value;
  if (question.options && question.options[selectedOption.value]) {
    const selectedOptionObj = question.options[selectedOption.value];
    
    if (selectedOptionObj.is_correct) {
      score.value++;
    }
  }
};

const nextQuestion = async () => {
  if (isLastQuestion.value) {
    // Submit quiz when finished
    await submitQuiz();
    quizCompleted.value = true;
  } else {
    currentQuestionIndex.value++;
    resetQuestion();
  }
};

const submitQuiz = async () => {
  try {
    // Prepare answers in the format expected by backend
    const answers = Object.entries(userAnswers.value).map(([question_id, selected_option_id]) => ({
      question_id: parseInt(question_id),
      selected_option_id: selected_option_id
    }));

    const response = await api.post('/primary/quiz/submit', {
      answers: answers
    });

    submittedScore.value = {
      score: response.data.score,
      total_questions: response.data.total_questions,
      percentage: response.data.percentage,
      points_earned: response.data.points_earned,
      total_points: response.data.total_points
    };

    // Update score with actual score from backend
    score.value = response.data.score;
  } catch (error) {
    console.error('Error submitting quiz:', error);
    errorMessage.value = 'Failed to submit quiz. Your answers may not be saved.';
  }
};

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--;
    resetQuestion();
  }
};

const resetQuestion = () => {
  // Restore previously selected option if exists
  const question = currentQuestion.value;
  if (question && question.options && userAnswers.value[question.id]) {
    const selectedOptionId = userAnswers.value[question.id];
    const optionIndex = question.options.findIndex(opt => opt.id === selectedOptionId);
    selectedOption.value = optionIndex >= 0 ? optionIndex : null;
  } else {
    selectedOption.value = null;
  }
  showFeedback.value = false;
};

const restartQuiz = () => {
  currentQuestionIndex.value = 0;
  score.value = 0;
  quizCompleted.value = false;
  userAnswers.value = {};
  submittedScore.value = null;
  errorMessage.value = '';
  resetQuestion();
  fetchQuestions();
};

// const startRandomQuiz = async () => {
//   const res = await api.post(
//     "/genai/random-quiz",
//     {}, 
//     {
//       headers: {
//         Authorization: `Bearer ${localStorage.getItem("token")}`
//       }
//     }
//   );

//   const quiz = res.data;

//   // store quiz temporarily
//   localStorage.setItem("temp_quiz", JSON.stringify(quiz));

//   // go to quiz page
//   router.push("/random-quiz");
// };

const loading = ref(false);
const startRandomQuiz = async () => {
  try {
    loading.value = true;

    // Allow overlay to render
    await new Promise(r => setTimeout(r, 100));
    const res = await api.post(
      "/genai/random-quiz",
      {}, // no body sent
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`
        }
      }
    );
    if (!res.data || res.data.error) {
      alert("Error generating quiz: " + res.data?.error);
      loading.value = false;
      return;
    }

    const quiz = res.data; // axios uses res.data

    localStorage.setItem("temp_quiz", JSON.stringify(quiz));
    router.push({ name: "RandomQuiz" });

  } catch (err) {
    console.error(err);
    alert("Could not start random quiz!");
  }
};


</script>

<style scoped>
.primary-user-quiz {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.quiz-header {
  margin-bottom: 2rem;
}

.quiz-header h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.question-card {
  border: none;
  border-radius: 0.5rem;
  background-color: #fff;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.question-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.question-text {
  color: #2c3e50;
  font-weight: 600;
}

.option-item {
  padding: 1rem;
  border: 2px solid #e9ecef;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.option-item:hover {
  border-color: #86b7fe;
  background-color: rgba(13, 110, 253, 0.05);
}

.option-item.selected {
  border-color: #86b7fe;
  background-color: rgba(13, 110, 253, 0.1);
}

.option-item.correct {
  border-color: #198754;
  background-color: rgba(25, 135, 84, 0.1);
}

.option-item.incorrect {
  border-color: #dc3545;
  background-color: rgba(220, 53, 69, 0.1);
}

.option-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.option-letter {
  font-weight: bold;
  color: #6c757d;
}

.option-text {
  flex: 1;
  text-align: left;
}

.feedback-icon {
  margin-left: 1rem;
  font-size: 1.25rem;
}

.quiz-navigation {
  margin-top: 2rem;
}

.quiz-results {
  max-width: 600px;
  margin: 0 auto;
}

.result-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.85);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 3000;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 6px solid #ddd;
  border-top-color: #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 15px;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}




@media (max-width: 768px) {
  .primary-user-quiz {
    padding: 0.5rem;
  }
   
  .option-item {
    padding: 0.75rem;
  }
  
  .quiz-navigation {
    flex-direction: column;
    gap: 1rem;
  }
  
  .quiz-navigation button {
    width: 100%;
  }
}
</style>
