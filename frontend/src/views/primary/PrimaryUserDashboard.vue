<template>
  <div class="primary-user-dashboard">
    <div class="row">
      <!-- Container 1: Quiz Performance -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-primary text-white">
            <h5 class="card-title mb-0">QUIZ PERFORMANCE</h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5">85 % AVERAGE SCORE</p>
            <p class="card-text text-muted">Great quiz performance in daily quizzes</p>
            <div class="mt-auto">
              <router-link to="/primary-dashboard/quiz-performance" class="btn btn-primary w-100">
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
            <p class="card-text fs-5">RANK 7 , 1200 Points</p>
            <p class="card-text text-muted">Keep climbing for ecomind</p>
            <div class="mt-auto">
              <router-link to="/primary-dashboard/community-leaderboard" class="btn btn-primary w-100">
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
            <p class="card-text fs-5">18 QUIZZES , 25 LOG ENTRIES , 2 CAMPAIGNS</p>
            <p class="card-text text-muted">Your active participation</p>
            <div class="mt-auto">
              <router-link to="/primary-dashboard/monthly-engagement" class="btn btn-primary w-100">
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
            <p class="card-text fs-5">45 KG WASTE DIVERTED</p>
            <p class="card-text text-muted">Your contribution to a cleaner planet</p>
            <div class="mt-auto">
              <router-link to="/primary-dashboard/waste-summary" class="btn btn-primary w-100">
                DETAILS
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Container 5: Waste Log -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-secondary text-white">
            <h5 class="card-title mb-0">WASTE LOG</h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5">LOG YOUR WASTE</p>
            <p class="card-text text-muted">Track your waste disposal</p>
            <div class="mt-auto">
              <router-link to="/primary-dashboard/wastelog" class="btn btn-primary w-100">
                LOG NOW
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Container 6: WasteWise Chatbot -->
      <div class="col-md-6 col-lg-8 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-dark text-white">
            <h5 class="card-title mb-0">WASTEWISE CHATBOT</h5>
          </div>
          <div class="card-body p-0 d-flex flex-column">
            <div class="chat-messages p-3 flex-grow-1 overflow-auto" style="max-height: 300px;">
              <div v-for="(message, index) in chatMessages" :key="index" class="mb-2">
                <div :class="['p-2 rounded', message.sender === 'user' ? 'bg-light text-end ms-5' : 'bg-primary text-white me-5']">
                  {{ message.text }}
                </div>
              </div>
            </div>
            <div class="input-group p-3 border-top">
              <input 
                v-model="userMessage" 
                type="text" 
                class="form-control" 
                placeholder="Ask me about waste management..."
                @keyup.enter="sendMessage"
              >
              <button class="btn btn-primary" @click="sendMessage">
                <i class="bi bi-send"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const userMessage = ref('');
const chatMessages = ref([
  { text: 'Hello! I\'m your WasteWise assistant. How can I help you with waste management today?', sender: 'bot' }
]);

const sendMessage = () => {
  if (!userMessage.value.trim()) return;
  
  // Add user message to chat
  chatMessages.value.push({ text: userMessage.value, sender: 'user' });
  
  // Simulate bot response
  setTimeout(() => {
    chatMessages.value.push({ 
      text: 'Thank you for your message! I\'m here to help with any waste management questions you have.', 
      sender: 'bot' 
    });
  }, 500);
  
  // Clear input
  userMessage.value = '';
};
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
</style>
