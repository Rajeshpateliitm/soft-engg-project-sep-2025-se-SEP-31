const PrimaryUserDashboard = {
    template: `
        <div>
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
                            <p class="card-text fs-5">5.2 KG WET , 3.2 KG DRY , 1 KG HAZARDOUS</p>
                            <p class="card-text text-muted">&nbsp;</p>
                            <div class="mt-auto">
                                <router-link to="/primary-dashboard/waste-summary" class="btn btn-primary w-100">
                                    DETAILS
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Container 5: Chatbot -->
                <div class="col-md-6 col-lg-8 mb-4">
                    <div class="card shadow-lg h-100">
                        <div class="card-header bg-dark text-white">
                            <h5 class="card-title mb-0">WASTEWISE CHATBOT</h5>
                        </div>
                        <div class="card-body">
                            <!-- Chatbot Messages Area -->
                            <div class="chat-messages mb-3 p-3 border rounded" style="height: 200px; overflow-y: auto; background-color: #f8f9fa;">
                                <div class="message bot-message mb-2">
                                    <strong>WasteBot:</strong> Hello! I'm your waste management assistant. How can I help you today?
                                </div>
                                <div v-for="(message, index) in chatMessages" :key="index" 
                                     :class="['message', 'mb-2', message.type === 'user' ? 'user-message text-end' : 'bot-message']">
                                    <strong v-if="message.type === 'bot'">WasteBot:</strong> 
                                    {{ message.text }}
                                    <strong v-if="message.type === 'user'">You:</strong>
                                </div>
                            </div>
                            
                            <!-- Chat Input -->
                            <div class="input-group">
                                <input type="text" 
                                       class="form-control" 
                                       v-model="userMessage"
                                       placeholder="Type your message here..."
                                       @keyup.enter="sendMessage">
                                <button class="btn btn-primary" @click="sendMessage">
                                    Send
                                </button>
                            </div>
                            <small class="text-muted">Note: This is a dummy chatbot. Responses will be implemented later.</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            userMessage: '',
            chatMessages: []
        };
    },
    methods: {
        sendMessage() {
            if (this.userMessage.trim()) {
                // Add user message
                this.chatMessages.push({
                    type: 'user',
                    text: this.userMessage
                });
                
                // Clear input
                const message = this.userMessage;
                this.userMessage = '';
                
                // Simulate bot "thinking" but no actual response
                setTimeout(() => {
                    this.chatMessages.push({
                        type: 'bot',
                        text: 'Thank you for your message. The chatbot functionality is currently under development.'
                    });
                }, 1000);
            }
        }
    }
};

export default PrimaryUserDashboard;