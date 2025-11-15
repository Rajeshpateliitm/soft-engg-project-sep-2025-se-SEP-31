<template>
  <div class="primary-user-dashboard">
    <!-- Floating Chat Button -->
    <button
      @click.stop="toggleChat"
      class="chat-button"
      :class="{ 'chat-button-active': isChatOpen }"
      :aria-label="isChatOpen ? 'Close chat' : 'Chat with WasteWise'"
      type="button"
    >
      <div class="chat-button-content">
        <i class="bi" :class="isChatOpen ? 'bi-x-lg' : 'bi-chat-dots-fill'"></i>
        <span class="chat-button-text" v-if="!isChatOpen">Need help?</span>
      </div>
      <div class="chat-notification" v-if="!isChatOpen">
        <i class="bi bi-arrow-up"></i>
      </div>
    </button>

    <!-- Chat Window -->
    <div
      class="chat-window"
      :class="{
        'chat-window-open': isChatOpen,
        dragging: isDragging,
        resizing: isResizing,
      }"
      :style="chatWindowStyle"
      @click.stop
      ref="chatWindow"
    >
      <div class="chat-header" @mousedown="startDrag" @touchstart="startDrag">
        <h6 class="mb-0">WasteWise Assistant</h6>
        <div class="chat-header-actions">
          <button
            @click.stop="toggleChat"
            class="btn-close"
            aria-label="Close chat"
            type="button"
            title="Close"
          >
            <i
              class="bi bi-x-lg"
              style="
                display: inline-block;
                color: white !important;
                font-size: 1.1rem;
                line-height: 1;
              "
            ></i>
          </button>
        </div>
      </div>
      <!-- Resize handle -->
      <div
        class="chat-resize-handle"
        @mousedown="startResize"
        @touchstart="startResize"
      ></div>
      <div class="chat-messages" ref="chatContainer">
        <div
          v-for="(message, index) in chatMessages"
          :key="index"
          :class="['message', message.sender]"
        >
          {{ message.text }}
        </div>
      </div>
      <div class="chat-input">
        <input
          type="text"
          v-model="userMessage"
          @keydown.enter="handleEnterKey"
          placeholder="Type your message..."
          class="form-control"
          ref="chatInput"
        />
        <button
          @click.stop="sendMessage"
          class="btn btn-primary"
          :disabled="!userMessage.trim()"
          type="button"
        >
          <i class="bi bi-send-fill"></i>
        </button>
      </div>
    </div>
    <div class="row">
      <!-- Container 1: Quiz Performance -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-primary text-white">
            <h5 class="card-title mb-0">QUIZ PERFORMANCE</h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5">
              {{ quizPerformance.average_score }}% AVERAGE SCORE
            </p>
            <p class="card-text text-muted">{{ quizPerformance.message }}</p>
            <div class="mt-auto">
              <router-link
                to="/primary-dashboard/quiz-performance"
                class="btn btn-primary w-100"
              >
                DETAILS
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Container 2: Community Leaderboard -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-success text-white">
            <h5 class="card-title mb-0">COMMUNITY LEADERBOARD</h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5">
              RANK {{ leaderboard.rank }}, {{ leaderboard.points }} Points
            </p>
            <p class="card-text text-muted">{{ leaderboard.message }}</p>
            <div class="mt-auto">
              <router-link
                to="/primary-dashboard/community-leaderboard"
                class="btn btn-primary w-100"
              >
                DETAILS
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Container 3: Monthly Engagement -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-warning text-dark">
            <h5 class="card-title mb-0">MONTHLY ENGAGEMENT</h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5">
              {{ monthlyEngagement.quizzes }} QUIZZES,
              {{ monthlyEngagement.waste_logs }} LOG ENTRIES,
              {{ monthlyEngagement.campaigns }} CAMPAIGNS
            </p>
            <p class="card-text text-muted">{{ monthlyEngagement.message }}</p>
            <div class="mt-auto">
              <router-link
                to="/primary-dashboard/monthly-engagement"
                class="btn btn-primary w-100"
              >
                DETAILS
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Container 4: Waste Summary -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-info text-white">
            <h5 class="card-title mb-0">WASTE SUMMARY</h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5">
              {{
                (
                  wasteSummary.wet_kg +
                  wasteSummary.dry_kg +
                  wasteSummary.hazardous_kg
                ).toFixed(1)
              }}
              KG WASTE
            </p>
            <p class="card-text text-muted">
              Wet: {{ wasteSummary.wet_kg }}kg, Dry:
              {{ wasteSummary.dry_kg }}kg, Hazardous:
              {{ wasteSummary.hazardous_kg }}kg
            </p>
            <div class="mt-auto">
              <router-link
                to="/primary-dashboard/waste-summary"
                class="btn btn-primary w-100"
              >
                DETAILS
              </router-link>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import api from "../../services/api";

const router = useRouter();
const route = useRoute();

// ............................ -->

const userMessage = ref("");
const isChatOpen = ref(false);
const isDragging = ref(false);
const isResizing = ref(false);
const chatContainer = ref(null);
const dashboardChatContainer = ref(null);
const chatInput = ref(null);
const chatWindow = ref(null);
const chatMessages = ref([
  {
    text: "Hello! I'm your WasteWise assistant. How can I help you with waste management today?",
    sender: "bot",
  },
]);

// Chat window position and size state
const chatWindowStyle = ref({
  width: "350px",
  height: "500px",
  bottom: "5.5rem",
  right: "2rem",
  top: "auto",
  left: "auto",
});

// Drag and resize state
const dragStart = ref({ x: 0, y: 0 });
const windowStart = ref({ left: 0, top: 0 });
const resizeStart = ref({ x: 0, y: 0, width: 0, height: 0 });
const sizeStart = ref({ width: 0, height: 0 });

// Dashboard data
const quizPerformance = ref({
  average_score: 0,
  message: "Start taking quizzes to see your performance!",
});
const leaderboard = ref({
  rank: 0,
  points: 0,
  message: "Start earning points!",
});
const monthlyEngagement = ref({
  quizzes: 0,
  waste_logs: 0,
  campaigns: 0,
  message: "Your active participation.",
});
const wasteSummary = ref({
  wet_kg: 0,
  dry_kg: 0,
  hazardous_kg: 0,
});

// Fetch dashboard data
const fetchDashboardData = async () => {
  try {
    const response = await api.get("/primary/dashboard");
    const data = response.data;

    quizPerformance.value = {
      average_score: data.quiz_performance.average_score,
      message: data.quiz_performance.message,
    };

    leaderboard.value = {
      rank: data.leaderboard.rank,
      points: data.leaderboard.points,
      message: data.leaderboard.message,
    };

    monthlyEngagement.value = {
      quizzes: data.monthly_engagement.quizzes,
      waste_logs: data.monthly_engagement.waste_logs,
      campaigns: data.monthly_engagement.campaigns,
      message: data.monthly_engagement.message,
    };

    wasteSummary.value = {
      wet_kg: data.waste_summary.wet_kg,
      dry_kg: data.waste_summary.dry_kg,
      hazardous_kg: data.waste_summary.hazardous_kg,
    };
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
  }
};

// Event handlers setup
let focusHandler = () => {
  fetchDashboardData();
};

const checkAutoOpenChat = () => {
  if (route.query.openChat === "true") {
    setTimeout(() => {
      isChatOpen.value = true;

      nextTick(() => {
        scrollToBottom();
        if (route.query.quizId) {
          const quizId = route.query.quizId;
          setTimeout(() => {
            chatMessages.value.push({
              text: `I see you're asking about quiz attempt #${quizId}. How can I help you?`,
              sender: "bot",
            });
            scrollToBottom();
          }, 500);
        }
      });

      router.replace({ path: route.path, query: {} });
    }, 300);
  }
};

watch(
  () => route.query.openChat,
  (newVal) => {
    if (newVal === "true") {
      checkAutoOpenChat();
    }
  },
  { immediate: true }
);

// .............

const sendMessage = async () => {
  // Validate input
  if (!userMessage.value.trim()) return;

  // Store user message
  const message = userMessage.value.trim();

  // Add user message to chat
  chatMessages.value.push({ text: message, sender: "user" });

  // Clear input immediately
  userMessage.value = "";

  // Scroll to bottom after message is added
  await nextTick();
  scrollToBottom();

  // Show loading indicator
  const loadingMessageIndex = chatMessages.value.length;
  chatMessages.value.push({
    text: "Thinking...",
    sender: "bot",
    isLoading: true,
  });
  await nextTick();
  scrollToBottom();

  try {
    // Call the genai API endpoint
    const response = await api.post("/genai/chat", {
      message: message,
    });

    // Remove loading message
    chatMessages.value.pop();

    // Add bot response
    if (response.data && response.data.response) {
      chatMessages.value.push({
        text: response.data.response,
        sender: "bot",
      });
    } else if (response.data && response.data.error) {
      // Handle API errors gracefully
      chatMessages.value.push({
        text: "Sorry, I encountered an error. Please try again later.",
        sender: "bot",
      });
    } else {
      // Fallback response
      chatMessages.value.push({
        text: "I'm here to help with waste management questions. How can I assist you?",
        sender: "bot",
      });
    }
  } catch (error) {
    // Remove loading message
    chatMessages.value.pop();

    // Handle errors
    console.error("Chat error:", error);
    let errorMessage =
      "Sorry, I'm having trouble connecting. Please try again.";

    if (error.response) {
      // Server responded with error status
      const errorData = error.response.data;
      if (errorData && errorData.error) {
        errorMessage = `Error: ${errorData.error}`;
      } else {
        errorMessage =
          "Sorry, the service is temporarily unavailable. Please try again later.";
      }
    } else if (error.request) {
      // Request was made but no response received
      errorMessage =
        "Unable to connect to the server. Please check your connection.";
    }

    chatMessages.value.push({
      text: errorMessage,
      sender: "bot",
    });
  }

  // Scroll to bottom after response
  await nextTick();
  scrollToBottom();

  // Refocus input after sending message
  if (chatInput.value) {
    chatInput.value.focus();
  }
};


const toggleChat = (event) => {
  // Prevent event bubbling
  if (event) {
    event.stopPropagation();
    event.preventDefault();
  }

  isChatOpen.value = !isChatOpen.value;

  if (isChatOpen.value) {
    // Reset position when opening
    resetChatPosition();
    // Focus input when chat opens
    nextTick(() => {
      scrollToBottom();
      if (chatInput.value) {
        chatInput.value.focus();
      }
    });
  }
};

// Reset chat window to default position
const resetChatPosition = () => {
  chatWindowStyle.value = {
    width: "350px",
    height: "500px",
    bottom: "5.5rem",
    right: "2rem",
    top: "auto",
    left: "auto",
  };
};

// Start dragging the chat window
const startDrag = (e) => {
  if (!isChatOpen.value) return;

  e.preventDefault();
  e.stopPropagation();

  const clientX = e.touches ? e.touches[0].clientX : e.clientX;
  const clientY = e.touches ? e.touches[0].clientY : e.clientY;

  isDragging.value = true;
  dragStart.value = { x: clientX, y: clientY };

  // Get current position
  const rect = chatWindow.value.getBoundingClientRect();
  windowStart.value = {
    left: rect.left,
    top: rect.top,
  };

  // Change to absolute positioning for dragging
  chatWindowStyle.value.bottom = "auto";
  chatWindowStyle.value.right = "auto";
  chatWindowStyle.value.left = `${rect.left}px`;
  chatWindowStyle.value.top = `${rect.top}px`;

  document.addEventListener("mousemove", handleDrag);
  document.addEventListener("mouseup", stopDrag);
  document.addEventListener("touchmove", handleDrag);
  document.addEventListener("touchend", stopDrag);
};

// Handle dragging
const handleDrag = (e) => {
  if (!isDragging.value) return;

  e.preventDefault();
  const clientX = e.touches ? e.touches[0].clientX : e.clientX;
  const clientY = e.touches ? e.touches[0].clientY : e.clientY;

  const deltaX = clientX - dragStart.value.x;
  const deltaY = clientY - dragStart.value.y;

  // Calculate new position
  let newLeft = windowStart.value.left + deltaX;
  let newTop = windowStart.value.top + deltaY;

  // Get viewport dimensions
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;
  const navbarHeight = 80; // Approximate navbar height

  // Get window dimensions
  const windowWidth = parseInt(chatWindowStyle.value.width) || 350;
  const windowHeight = parseInt(chatWindowStyle.value.height) || 500;

  // Constrain to viewport (account for navbar)
  newLeft = Math.max(0, Math.min(newLeft, viewportWidth - windowWidth));
  newTop = Math.max(
    navbarHeight,
    Math.min(newTop, viewportHeight - windowHeight)
  );

  chatWindowStyle.value.left = `${newLeft}px`;
  chatWindowStyle.value.top = `${newTop}px`;
};

// Stop dragging
const stopDrag = () => {
  isDragging.value = false;
  document.removeEventListener("mousemove", handleDrag);
  document.removeEventListener("mouseup", stopDrag);
  document.removeEventListener("touchmove", handleDrag);
  document.removeEventListener("touchend", stopDrag);
};

// Start resizing the chat window
const startResize = (e) => {
  if (!isChatOpen.value) return;

  e.preventDefault();
  e.stopPropagation();

  const clientX = e.touches ? e.touches[0].clientX : e.clientX;
  const clientY = e.touches ? e.touches[0].clientY : e.clientY;

  isResizing.value = true;
  resizeStart.value = { x: clientX, y: clientY };

  // Get current size
  const currentWidth = parseInt(chatWindowStyle.value.width) || 350;
  const currentHeight = parseInt(chatWindowStyle.value.height) || 500;
  sizeStart.value = { width: currentWidth, height: currentHeight };

  document.addEventListener("mousemove", handleResize);
  document.addEventListener("mouseup", stopResize);
  document.addEventListener("touchmove", handleResize);
  document.addEventListener("touchend", stopResize);
};

// Handle resizing
const handleResize = (e) => {
  if (!isResizing.value) return;

  e.preventDefault();
  const clientX = e.touches ? e.touches[0].clientX : e.clientX;
  const clientY = e.touches ? e.touches[0].clientY : e.clientY;

  const deltaX = resizeStart.value.x - clientX; // Negative because we're resizing from bottom-right
  const deltaY = resizeStart.value.y - clientY;

  // Calculate new size
  let newWidth = sizeStart.value.width - deltaX;
  let newHeight = sizeStart.value.height - deltaY;

  // Minimum and maximum constraints
  const minWidth = 300;
  const minHeight = 300;
  const maxWidth = window.innerWidth - 40;
  const maxHeight = window.innerHeight - 120; // Account for navbar

  newWidth = Math.max(minWidth, Math.min(newWidth, maxWidth));
  newHeight = Math.max(minHeight, Math.min(newHeight, maxHeight));

  chatWindowStyle.value.width = `${newWidth}px`;
  chatWindowStyle.value.height = `${newHeight}px`;

  // Scroll to bottom after resize
  nextTick(() => {
    scrollToBottom();
  });
};

// Stop resizing
const stopResize = () => {
  isResizing.value = false;
  document.removeEventListener("mousemove", handleResize);
  document.removeEventListener("mouseup", stopResize);
  document.removeEventListener("touchmove", handleResize);
  document.removeEventListener("touchend", stopResize);
};

const handleEnterKey = (event) => {
  // Allow Shift+Enter for new line, Enter alone sends message
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    if (userMessage.value.trim()) {
      sendMessage();
    }
  }
};

const scrollToBottom = () => {
  // Scroll floating chat window
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
  // Scroll dashboard chat card
  if (dashboardChatContainer.value) {
    dashboardChatContainer.value.scrollTop =
      dashboardChatContainer.value.scrollHeight;
  }
};

// Close chat when clicking outside
const handleClickOutside = (event) => {
  const chatWindowEl = document.querySelector(".chat-window");
  const chatButton = document.querySelector(".chat-button");

  // Don't close if clicking on chat elements or if dragging/resizing
  if (
    isChatOpen.value &&
    !isDragging.value &&
    !isResizing.value &&
    chatWindowEl &&
    chatButton &&
    !chatWindowEl.contains(event.target) &&
    !chatButton.contains(event.target)
  ) {
    isChatOpen.value = false;
  }
};

onMounted(() => {
  // Fetch dashboard data
  fetchDashboardData();

  // Refresh data when window regains focus (e.g., after completing quiz)
  focusHandler = () => {
    fetchDashboardData();
  };
  window.addEventListener("focus", focusHandler);

  // Setup click outside handler for chat
  document.addEventListener("click", handleClickOutside);

  // Focus input when chat opens
  if (isChatOpen.value && chatInput.value) {
    chatInput.value.focus();
  }
});

onUnmounted(() => {
  // Remove event listeners
  document.removeEventListener("click", handleClickOutside);
  if (focusHandler) {
    window.removeEventListener("focus", focusHandler);
  }
  // Clean up drag/resize listeners
  stopDrag();
  stopResize();
});
</script>

<style scoped>
.primary-user-dashboard {
  padding: 1.5rem;
  background-color: transparent;
}

.card {
  border: 1px solid rgba(0, 0, 0, 0.125);
  border-radius: 0.5rem;
  transition: all 0.2s ease;
  background-color: #fff;
  margin-bottom: 1.5rem;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.card-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 0.5rem 0.5rem 0 0 !important;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.chat-messages {
  min-height: 200px;
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  margin: 0.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  font-weight: 500;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

/* Chat Button */
.chat-button {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  min-width: 60px;
  height: 60px;
  border-radius: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  z-index: 1000;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  padding: 0 1.5rem;
  overflow: hidden;
}

.chat-button-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  white-space: nowrap;
}

.chat-button-text {
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  transform: translateX(0);
  opacity: 1;
}

.chat-button-active .chat-button-text {
  transform: translateX(10px);
  opacity: 0;
  width: 0;
}

.chat-notification {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #ff4d4f;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite;
}

@keyframes ping {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.5);
    opacity: 0.5;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.chat-button i {
  transition: all 0.3s ease;
  font-size: 1.5rem;
}

.chat-button:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
}

.chat-button:hover .chat-button-text {
  transform: translateX(5px);
}

.chat-button-active {
  transform: scale(1) !important;
  border-radius: 50%;
  padding: 0;
  width: 60px;
}

.chat-button-active i {
  transform: rotate(90deg);
}

/* Chat Window */
.chat-window {
  position: fixed;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transform: translateY(20px);
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s ease, transform 0.3s ease;
  z-index: 1050; /* Above navbar (1030) */
  min-width: 300px;
  min-height: 300px;
}

.chat-window.dragging,
.chat-window.resizing {
  transition: none !important;
}

.chat-window-open {
  transform: translateY(0);
  opacity: 1;
  visibility: visible;
}

.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: move;
  user-select: none;
  position: relative;
  z-index: 1;
}

.chat-header h6 {
  margin: 0;
  font-weight: 600;
  flex: 1;
}

.chat-header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-close {
  background: rgba(255, 255, 255, 0.25);
  border: none;
  color: white;
  opacity: 1;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
  font-size: 1rem;
  line-height: 1;
}

.btn-close i {
  display: inline-block;
  color: white !important;
  font-size: 1rem;
  line-height: 1;
  width: auto;
  height: auto;
}

.btn-close:hover {
  background: rgba(255, 255, 255, 0.4);
  transform: scale(1.1);
  opacity: 1;
}

.chat-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  background-color: #f8f9fa;
}

.message {
  max-width: 80%;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  font-size: 0.9rem;
  line-height: 1.4;
  position: relative;
  animation: messageAppear 0.3s ease-out;
}

@keyframes messageAppear {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 0.25rem;
}

.message.bot {
  background: white;
  border: 1px solid #e9ecef;
  align-self: flex-start;
  border-bottom-left-radius: 0.25rem;
  white-space: pre-wrap;
}

.chat-input {
  display: flex;
  padding: 1rem;
  background: white;
  border-top: 1px solid #e9ecef;
  gap: 0.5rem;
}

.chat-input input {
  flex: 1;
  border: 1px solid #dee2e6;
  border-radius: 2rem;
  padding: 0.5rem 1rem;
  outline: none;
  transition: border-color 0.2s;
}

.chat-input input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.25rem rgba(102, 126, 234, 0.25);
}

.chat-input button {
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  transition: all 0.2s ease;
}

.chat-input button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.chat-input button:not(:disabled):hover {
  transform: scale(1.1);
}

/* Resize handle */
.chat-resize-handle {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 20px;
  height: 20px;
  cursor: nwse-resize;
  z-index: 10;
  background: linear-gradient(
    135deg,
    transparent 0%,
    transparent 40%,
    rgba(102, 126, 234, 0.3) 40%,
    rgba(102, 126, 234, 0.3) 60%,
    transparent 60%
  );
}

.chat-resize-handle::after {
  content: "";
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 0 12px 12px;
  border-color: transparent transparent rgba(102, 126, 234, 0.5) transparent;
}

.chat-resize-handle:hover {
  background: linear-gradient(
    135deg,
    transparent 0%,
    transparent 40%,
    rgba(102, 126, 234, 0.5) 40%,
    rgba(102, 126, 234, 0.5) 60%,
    transparent 60%
  );
}

.chat-resize-handle:hover::after {
  border-color: transparent transparent rgba(102, 126, 234, 0.8) transparent;
}

/* Responsive adjustments */
@media (max-width: 576px) {
  .chat-window {
    min-width: calc(100vw - 2rem) !important;
    min-height: 50vh !important;
    max-width: calc(100vw - 2rem) !important;
  }

  .chat-button {
    right: 1rem;
    bottom: 1rem;
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
  }

  .chat-resize-handle {
    width: 24px;
    height: 24px;
  }
}
</style>
