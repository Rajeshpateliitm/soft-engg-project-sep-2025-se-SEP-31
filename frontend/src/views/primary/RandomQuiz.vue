<template>
  <div class="container py-4">

    <!-- RETRY BUTTON -->
    <button class="btn btn-primary mt-3 mb-2" @click="retryQuiz" :disabled="loading">
      🔄 Try Another Random Quiz
    </button>

    <!-- LOADING OVERLAY -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p class="loading-text">Generating a new quiz…</p>
    </div>

    <!-- TIMER -->
    <div class="timer-circle">
      <svg>
        <circle cx="50" cy="50" r="45"></circle>
        <circle
          cx="50"
          cy="50"
          r="45"
          :style="{ strokeDashoffset: dashOffset }"
        ></circle>
      </svg>
      <div class="timer-text">{{ timer }}</div>
    </div>

    <!-- QUIZ LOADING -->
    <div v-if="!questions.length && !quizFinished && !loading" class="text-center mt-4">
      <h4 class="text-muted">Loading quiz…</h4>
    </div>

    <!-- QUIZ ACTIVE -->
    <div v-else-if="!quizFinished && !loading">
      <h3 class="fw-bold text-dark">
        Question: {{ index + 1 }} / {{ questions.length }}
      </h3>

      <p class="lead question-text">{{ currentQuestion.question_text }}</p>

      <!-- OPTIONS -->
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

    <!-- QUIZ FINISHED -->
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
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import api from "@/services/api";
import confetti from "canvas-confetti";

const router = useRouter();

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

/* CURRENT QUESTION */
const currentQuestion = computed(() => questions.value[index.value]);

/* LOAD INITIAL QUIZ */
onMounted(() => loadQuizFromLocal());
onBeforeUnmount(() => clearInterval(intervalId.value));

/* LOAD QUIZ FROM LOCALSTORAGE */
const loadQuizFromLocal = () => {
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

  // Reset quiz state
  questions.value = quiz.questions;
  index.value = 0;
  score.value = 0;
  animatedScore.value = 0;
  quizFinished.value = false;

  startTimer();
};

/* TIMER */
const startTimer = () => {
  clearInterval(intervalId.value);

  timer.value = 15;
  dashOffset.value = 283;
  optionsLocked.value = false;

  intervalId.value = setInterval(() => {
    timer.value--;
    dashOffset.value = (timer.value / 15) * 283;

    if (timer.value <= 0) nextQuestion();
  }, 1000);
};

/* SELECT OPTION */
const selectOption = (opt) => {
  optionsLocked.value = true;

  if (opt.is_correct) score.value++;

  setTimeout(() => nextQuestion(), 650);
};

/* NEXT QUESTION */
const nextQuestion = () => {
  clearInterval(intervalId.value);

  if (index.value < questions.value.length - 1) {
    index.value++;
    startTimer();
  } else {
    finishQuiz();
  }
};

/* FINISH QUIZ */
const finishQuiz = () => {
  quizFinished.value = true;

  launchConfetti();

  let x = 0;
  const anim = setInterval(() => {
    animatedScore.value = x;
    if (x >= score.value) clearInterval(anim);
    x++;
  }, 50);

  // Submit score to backend
  submitScore();
};

const submitScore = async () => {
  try {
    await api.post('/genai/random-quiz/score', {
      score: score.value
    });
    // Optional: Show success message or toast
    // alert(`You earned ${score.value} points!`); 
  } catch (err) {
    console.error("Failed to submit score:", err);
  }
};

/* BUTTON COLORS */
const buttonClass = (opt) => {
  if (!optionsLocked.value) return "btn-outline-primary";
  return opt.is_correct ? "btn-success" : "btn-danger";
};

/* RETRY QUIZ */
const retryQuiz = async () => {
  try {
    loading.value = true;

    await new Promise(r => setTimeout(r, 80)); // Let overlay show

    const res = await api.post(
      "/genai/random-quiz",
      {},
      { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } }
    );

    if (!res.data || res.data.error) {
      alert("Error generating quiz: " + res.data?.error);
      loading.value = false;
      return;
    }

    localStorage.setItem("temp_quiz", JSON.stringify(res.data));
    loadQuizFromLocal();

  } catch (err) {
    console.error(err);
    alert("Network or server error. Try again.");
  }

  loading.value = false;
};

/* CONFETTI */
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
.question-text {
  font-size: 20px;
  font-weight: 500;
  color: #333;
}

/* LOADING OVERLAY */
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
  to   { transform: rotate(360deg); }
}

/* OPTIONS */
.option-button {
  font-size: 17px;
  padding: 12px;
}

/* TIMER */
.timer-circle {
  width: 120px;
  height: 120px;
  margin: 15px auto;
  position: relative; 
}
.timer-circle svg {
  width: 120px;
  height: 120px;
  transform: rotate(-90deg);
}
.timer-circle circle {
  fill: none;
  stroke-width: 10;
  stroke: #ddd;
}
.timer-circle circle:nth-child(2) {
  stroke: #ff0000;
  stroke-linecap: round;
  stroke-dasharray: 283;
  transition: stroke-dashoffset 1s linear;
}
.timer-text {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 22px;
  font-weight: bold;
  pointer-events: none; /* Ensure clicks pass through if needed */
}

.confetti-canvas {
  position: fixed;
  top: 0;
  left: 0;
  pointer-events: none;
}

.score-animate {
  animation: pop 0.6s ease-out;
}

@keyframes pop {
  0% { transform: scale(0.6); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
</style>
