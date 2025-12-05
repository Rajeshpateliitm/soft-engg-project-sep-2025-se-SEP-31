<template>
  <div class="container py-4">
    <!-- Retry Button -->
    <button class="btn btn-primary mt-3 mb-2" @click="retryQuiz" :disabled="loading">
      Try Another Random Quiz
    </button>

    <!-- Error Message -->
    <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show mt-3" role="alert">
      {{ errorMessage }}
      <button type="button" class="btn-close" @click="errorMessage = ''"></button>
    </div>

    <!-- Loading Overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p class="loading-text">Generating a new quiz…</p>
    </div>

    <!-- Timer Circle -->
    <div class="timer-circle" :class="{ pulse: isPulsing }">
      <svg viewBox="0 0 100 100" aria-hidden="true">
        <circle cx="50" cy="50" r="45" class="track"></circle>
        <circle
          cx="50"
          cy="50"
          r="45"
          :style="{
            strokeDashoffset: dashOffset,
            stroke: strokeColor,
            transition: isRestoring ? 'none' : 'stroke-dashoffset 0.9s linear, stroke 0.3s linear'
          }"
          class="progress"
        ></circle>
      </svg>
      <div class="timer-text">{{ timer }}</div>
    </div>

    <!-- Quiz Loading State -->
    <div v-if="!questions.length && !quizFinished && !loading" class="text-center mt-4">
      <h4 class="text-muted">Loading quiz…</h4>
    </div>

    <!-- Quiz Active -->
    <div v-else-if="!quizFinished && !loading">
      <h3 class="fw-bold text-dark">
        Question: {{ index + 1 }} / {{ questions.length }}
      </h3>
      <p class="lead question-text">{{ currentQuestion.question_text }}</p>

      <!-- Options -->
      <div class="mt-4">
        <button
          v-for="(opt, i) in currentQuestion.options"
          :key="i"
          class="btn w-100 mb-2 option-button"
          :class="buttonClass(opt)"
          :disabled="optionsLocked"
          @click="selectOption(opt)"
        >
          {{ opt.text }}
        </button>
      </div>
    </div>

    <!-- Quiz Finished -->
    <div v-else class="text-center mt-5">
      <canvas id="confetti-canvas" class="confetti-canvas"></canvas>

      <h2 class="score-animate mt-3">
        🎉 Your Score: {{ animatedScore }} / {{ questions.length }}
      </h2>
      <h4 class="text-primary fw-bold mt-2">
        +{{ animatedScore * 10 }} Points Earned
      </h4>

      <h4 class="mt-4">Correct Answers</h4>
      <ul class="list-group mt-3">
        <li class="list-group-item" v-for="(q, qi) in questions" :key="qi">
          <b>Q{{ qi + 1 }}:</b> {{ q.question_text }}<br />
          <span class="text-success">✔ {{ q.options.find(o => o.is_correct).text }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "@/services/api";
import confetti from "canvas-confetti";

const router = useRouter();

// ============================================================================
// STATE
// ============================================================================

const questions = ref([]);
const index = ref(0);
const timer = ref(15);
const dashOffset = ref(283);
const intervalId = ref(null);
const quizFinished = ref(false);
const optionsLocked = ref(false);
const score = ref(0);
const animatedScore = ref(0);
const loading = ref(false);
const errorMessage = ref("");
const restoredProgress = ref(false);
const isRestoring = ref(false);

const strokeColor = ref("#28a745");
const isPulsing = ref(false);

// Daily quiz limit tracking
const DAILY_QUIZ_LIMIT = 2;
const CIRCUMFERENCE = 2 * Math.PI * 45;

// ============================================================================
// COMPUTED
// ============================================================================

const currentQuestion = computed(() => questions.value[index.value]);

// ============================================================================
// DAILY LIMIT HELPERS
// ============================================================================

const getTodayDate = () => {
  const today = new Date();
  return today.toISOString().split("T")[0];
};

const getQuizAttemptsToday = () => {
  const today = getTodayDate();
  const key = `quiz_attempts_${today}`;
  const attempts = localStorage.getItem(key);
  return attempts ? parseInt(attempts, 10) : 0;
};

const incrementQuizAttempts = () => {
  const today = getTodayDate();
  const key = `quiz_attempts_${today}`;
  const current = getQuizAttemptsToday();
  localStorage.setItem(key, (current + 1).toString());
};

const hasReachedDailyLimit = () => {
  return getQuizAttemptsToday() >= DAILY_QUIZ_LIMIT;
};

// ============================================================================
// LIFECYCLE
// ============================================================================

onMounted(() => {
  const saved = localStorage.getItem("quiz_progress");

  if (saved) {
    restoredProgress.value = true;
    loadSavedProgress(JSON.parse(saved));
  } else {
    loadQuizFromLocal();
  }
});

// ============================================================================
// QUIZ LOADING
// ============================================================================

const loadQuizFromLocal = () => {
  if (restoredProgress.value) return;

  const saved = localStorage.getItem("temp_quiz");

  if (!saved) {
    alert("No quiz found. Please try again.");
    router.push({ name: "PrimaryUserDashboard" });
    return;
  }

  const quiz = JSON.parse(saved);

  if (!quiz.questions || quiz.questions.length === 0) {
    alert("Invalid quiz format.");
    router.push({ name: "PrimaryUserDashboard" });
    return;
  }

  questions.value = quiz.questions;
  index.value = 0;
  score.value = 0;
  animatedScore.value = 0;
  quizFinished.value = false;

  startTimer();
};

const loadSavedProgress = (saved) => {
  questions.value = saved.questions;
  index.value = saved.index;
  timer.value = saved.timer;
  score.value = saved.score;
  quizFinished.value = saved.quizFinished;

  // Compute progress arc for restored timer
  const progress = timer.value / 15;
  dashOffset.value = Math.round(CIRCUMFERENCE * (1 - progress));

  // Restore color and pulsing state
  if (timer.value > 10) {
    strokeColor.value = "#28a745";
    isPulsing.value = false;
  } else if (timer.value > 5) {
    strokeColor.value = "#ffc107";
    isPulsing.value = false;
  } else {
    strokeColor.value = "#dc3545";
    isPulsing.value = true;
  }

  if (!quizFinished.value) {
    startTimer(true);
  }
};

// ============================================================================
// TIMER
// ============================================================================

const startTimer = (isRestore = false) => {
  clearInterval(intervalId.value);

  if (!isRestore) {
    timer.value = 15;
    dashOffset.value = 0;
  } else {
    const progress = timer.value / 15;
    dashOffset.value = Math.round(CIRCUMFERENCE * (1 - progress));
  }

  optionsLocked.value = false;
  isPulsing.value = false;

  intervalId.value = setInterval(() => {
    timer.value--;

    const progress = timer.value / 15;
    dashOffset.value = Math.round(CIRCUMFERENCE * (1 - progress));

    if (timer.value > 10) {
      strokeColor.value = "#28a745";
      isPulsing.value = false;
    } else if (timer.value > 5) {
      strokeColor.value = "#ffc107";
      isPulsing.value = false;
    } else {
      strokeColor.value = "#dc3545";
      isPulsing.value = true;
    }

    saveProgress();

    if (timer.value <= 0) nextQuestion();
  }, 1000);
};

// ============================================================================
// QUIZ INTERACTION
// ============================================================================

const selectOption = (opt) => {
  optionsLocked.value = true;

  if (opt.is_correct) score.value++;

  saveProgress();

  setTimeout(() => nextQuestion(), 650);
};

const nextQuestion = () => {
  clearInterval(intervalId.value);

  if (index.value < questions.value.length - 1) {
    index.value++;
    saveProgress();
    startTimer();
  } else {
    finishQuiz();
  }
};

const buttonClass = (opt) => {
  if (!optionsLocked.value) return "btn-outline-primary";
  return opt.is_correct ? "btn-success" : "btn-danger";
};

// ============================================================================
// PROGRESS PERSISTENCE
// ============================================================================

const saveProgress = () => {
  const progress = {
    index: index.value,
    timer: timer.value,
    score: score.value,
    questions: questions.value,
    quizFinished: quizFinished.value
  };
  localStorage.setItem("quiz_progress", JSON.stringify(progress));
};

// ============================================================================
// QUIZ COMPLETION
// ============================================================================

const finishQuiz = () => {
  quizFinished.value = true;
  localStorage.removeItem("quiz_progress");
  localStorage.removeItem("temp_quiz");

  launchConfetti();

  let x = 0;
  const anim = setInterval(() => {
    animatedScore.value = x;
    if (x >= score.value) clearInterval(anim);
    x++;
  }, 50);

  submitScore();
};

const submitScore = async () => {
  try {
    await api.post("/genai/random-quiz/score", {
      score: score.value
    });
  } catch (err) {
    console.error("Failed to submit score:", err);
  }
};

// ============================================================================
// RETRY QUIZ
// ============================================================================

const retryQuiz = async () => {
  // Check daily limit
  if (hasReachedDailyLimit()) {
    errorMessage.value = "You have tried your daily quiz limit. Try next day...";
    return;
  }

  loading.value = true;
  errorMessage.value = "";

  await new Promise((r) => setTimeout(r, 80));

  try {
    const res = await api.post(
      "/genai/random-quiz",
      {},
      {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        timeout: 20000
      }
    );

    if (!res.data || res.data.error) {
      errorMessage.value = "Failed to generate quiz. Please try again.";
      return;
    }

    // Increment attempt counter
    incrementQuizAttempts();

    localStorage.setItem("temp_quiz", JSON.stringify(res.data));
    loadQuizFromLocal();

  } catch (err) {
    console.error("Quiz error:", err);

    if (err.code === "ECONNABORTED") {
      errorMessage.value = "Quiz is taking too long. Please try again.";
      setTimeout(() => (errorMessage.value = ""), 4000);
    } else if (!err.response) {
      errorMessage.value = "Network error — check your connection.";
    } else if (err.response.status === 401) {
      errorMessage.value = "Session expired. Redirecting...";
      router.push("/signin");
    } else {
      errorMessage.value = err.response?.data?.error || "Unknown server error.";
    }
  }

  loading.value = false;
};

// ============================================================================
// CONFETTI
// ============================================================================

const launchConfetti = () => {
  const canvas = document.getElementById("confetti-canvas");
  if (!canvas) return;

  const conf = confetti.create(canvas, { resize: true });

  conf({
    particleCount: 150,
    spread: 90,
    origin: { y: 0.6 }
  });
};
</script>

<style scoped>
/* ========================================================================== */
/* QUESTION TEXT */
/* ========================================================================== */

.question-text {
  font-size: 20px;
  font-weight: 500;
  color: #333;
}

/* ========================================================================== */
/* LOADING OVERLAY */
/* ========================================================================== */

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  backdrop-filter: blur(4px);
  background: rgba(255, 255, 255, 0.65);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 3000;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 6px solid #ccc;
  border-top-color: #0066ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 12px;
  font-size: 18px;
  color: #333;
  font-weight: 600;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ========================================================================== */
/* OPTIONS */
/* ========================================================================== */

.option-button {
  font-size: 17px;
  padding: 12px;
}

/* ========================================================================== */
/* TIMER CIRCLE */
/* ========================================================================== */

.timer-circle {
  width: 120px;
  height: 120px;
  margin: 15px auto;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.18s ease;
}

.timer-circle.pulse {
  transform: scale(1.05);
}

.timer-circle svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.timer-circle .track {
  fill: none;
  stroke: #e0e0e0;
  stroke-width: 8;
}

.timer-circle .progress {
  fill: none;
  stroke-width: 8;
  stroke-linecap: round;
  stroke-dasharray: 282.743;
}

.timer-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 22px;
  font-weight: bold;
  text-align: center;
  pointer-events: none;
}

.timer-circle.pulse .timer-text {
  animation: pulseText 0.8s ease-in-out infinite;
}

@keyframes pulseText {
  0% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.12); }
  100% { transform: translate(-50%, -50%) scale(1); }
}

/* ========================================================================== */
/* CONFETTI */
/* ========================================================================== */

.confetti-canvas {
  position: fixed;
  top: 0;
  left: 0;
  pointer-events: none;
}

/* ========================================================================== */
/* SCORE ANIMATION */
/* ========================================================================== */

.score-animate {
  animation: pop 0.6s ease-out;
}

@keyframes pop {
  0% { transform: scale(0.6); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
</style>
