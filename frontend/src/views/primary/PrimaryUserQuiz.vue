<template>
  <div class="primary-user-quiz">
    <div class="quiz-container">
      <!-- Quiz Header -->
      <div class="quiz-header text-center mb-4">
        <h2 class="fw-bold">Waste Management Quiz</h2>
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
            <span>Question {{ currentQuestionIndex + 1 }} of {{ questions.length }}</span>
            <span>Score: {{ score }}/{{ questions.length }}</span>
          </div>
        </div>
      </div>

      <!-- Quiz Content -->
      <div v-if="!quizCompleted" class="quiz-content">
        <div class="question-card card shadow-sm mb-4">
          <div class="card-body">
            <h4 class="question-text mb-4">{{ currentQuestion.question }}</h4>
            
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
                  'correct': showFeedback && option.correct,
                  'incorrect': showFeedback && selectedOption === index && !option.correct
                }"
                @click="selectOption(index)"
              >
                <div class="option-content">
                  <span class="option-letter">{{ String.fromCharCode(65 + index) }}.</span>
                  <span class="option-text">{{ option.text }}</span>
                </div>
                <div v-if="showFeedback" class="feedback-icon">
                  <i 
                    v-if="option.correct" 
                    class="bi bi-check-circle-fill text-success"
                  ></i>
                  <i 
                    v-else-if="selectedOption === index && !option.correct"
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
            <p class="lead">Your Score: {{ score }}/{{ questions.length }}</p>
            <p class="text-muted mb-4">
              {{ getResultMessage }}
            </p>
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
import { ref, computed } from 'vue';

const questions = [
  {
    question: 'Which of the following items can be recycled?',
    options: [
      { text: 'Plastic water bottle', correct: true },
      { text: 'Used pizza box', correct: false },
      { text: 'Plastic shopping bag', correct: false },
      { text: 'Styrofoam container', correct: false }
    ],
    image: null
  },
  {
    question: 'What is the best way to dispose of electronic waste?',
    options: [
      { text: 'Throw in regular trash', correct: false },
      { text: 'Burn it', correct: false },
      { text: 'Take to e-waste recycling center', correct: true },
      { text: 'Bury it in the backyard', correct: false }
    ],
    image: null
  },
  {
    question: 'Which bin should you use for food waste?',
    options: [
      { text: 'Recycling bin', correct: false },
      { text: 'Compost bin', correct: true },
      { text: 'Landfill bin', correct: false },
      { text: 'None of the above', correct: false }
    ],
    image: null
  },
  {
    question: 'How can you reduce waste when shopping?',
    options: [
      { text: 'Use reusable shopping bags', correct: false },
      { text: 'Buy in bulk', correct: false },
      { text: 'Choose products with minimal packaging', correct: false },
      { text: 'All of the above', correct: true }
    ],
    image: null
  }
];

const currentQuestionIndex = ref(0);
const selectedOption = ref(null);
const score = ref(0);
const showFeedback = ref(false);
const quizCompleted = ref(false);

const currentQuestion = computed(() => questions[currentQuestionIndex.value]);
const isLastQuestion = computed(() => currentQuestionIndex.value === questions.length - 1);
const progress = computed(() => (currentQuestionIndex.value / questions.length) * 100);
const getResultMessage = computed(() => {
  const percentage = (score.value / questions.length) * 100;
  if (percentage >= 80) return 'Excellent! You\'re a waste management expert!';
  if (percentage >= 60) return 'Good job! You know quite a bit about waste management.';
  if (percentage >= 40) return 'Not bad! Keep learning about proper waste disposal.';
  return 'Keep trying! Check out our resources to learn more about waste management.';
});

const selectOption = (index) => {
  if (!showFeedback.value) {
    selectedOption.value = index;
  }
};

const checkAnswer = () => {
  if (selectedOption.value === null) return;
  
  showFeedback.value = true;
  
  if (currentQuestion.value.options[selectedOption.value].correct) {
    score.value++;
  }
};

const nextQuestion = () => {
  if (isLastQuestion.value) {
    quizCompleted.value = true;
  } else {
    currentQuestionIndex.value++;
    resetQuestion();
  }
};

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--;
    resetQuestion();
  }
};

const resetQuestion = () => {
  selectedOption.value = null;
  showFeedback.value = false;
};

const restartQuiz = () => {
  currentQuestionIndex.value = 0;
  score.value = 0;
  quizCompleted.value = false;
  resetQuestion();
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
