<template>
  <div class="community-leaderboard">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Loading leaderboard data...</p>
    </div>

    <!-- Content -->
    <template v-else>
    <!-- Error Message -->
    <div v-if="errorMessage" class="alert alert-danger mb-4" role="alert">
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ errorMessage }}
      <button class="btn btn-sm btn-outline-danger ms-2" @click="fetchLeaderboard">
        <i class="bi bi-arrow-clockwise me-1"></i> Retry
      </button>
    </div>
    
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
          <h2 class="mb-0">Community Leaderboard</h2>
          <div class="d-flex gap-2">
            <select v-model="timeRange" class="form-select form-select-sm" style="width: auto;">
              <option value="weekly">This Week</option>
              <option value="monthly" selected>This Month</option>
              <option value="yearly">This Year</option>
              <option value="all">All Time</option>
            </select>
            <div class="input-group input-group-sm" style="width: 200px;">
              <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
              <input 
                type="text" 
                class="form-control" 
                placeholder="Search users..."
                v-model="searchQuery"
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Left Column - Leaderboard -->
      <div class="col-lg-8 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <ul class="nav nav-tabs card-header-tabs" id="leaderboardTabs" role="tablist">
              <li class="nav-item" role="presentation">
                <button 
                  class="nav-link active" 
                  id="global-tab" 
                  data-bs-toggle="tab" 
                  data-bs-target="#global" 
                  type="button" 
                  role="tab"
                >
                  <i class="bi bi-globe me-1"></i> Global
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button 
                  class="nav-link" 
                  id="friends-tab" 
                  data-bs-toggle="tab" 
                  data-bs-target="#friends" 
                  type="button" 
                  role="tab"
                >
                  <i class="bi bi-people me-1"></i> Friends
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button 
                  class="nav-link" 
                  id="local-tab" 
                  data-bs-toggle="tab" 
                  data-bs-target="#local" 
                  type="button" 
                  role="tab"
                >
                  <i class="bi bi-geo-alt me-1"></i> Local
                </button>
              </li>
            </ul>
          </div>
          <div class="card-body p-0">
            <div class="tab-content" id="leaderboardTabsContent">
              <!-- Global Leaderboard -->
              <div class="tab-pane fade show active" id="global" role="tabpanel" aria-labelledby="global-tab">
                <div class="table-responsive">
                  <table class="table table-hover align-middle mb-0">
                    <thead class="table-light">
                      <tr>
                        <th style="width: 50px;">#</th>
                        <th>User</th>
                        <th class="text-end">Points</th>
                        <th class="text-center">Level</th>
                        <th class="text-end">Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-if="loading">
                        <td colspan="5" class="text-center py-4">
                          <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                          </div>
                        </td>
                      </tr>
                      <tr v-else-if="!filteredUsers || filteredUsers.length === 0">
                        <td colspan="5" class="text-center py-4">
                          <p class="text-muted mb-0">No users found</p>
                        </td>
                      </tr>
                      <tr 
                        v-else
                        v-for="user in filteredUsers" 
                        :key="user.id || user.rank"
                        :class="{ 'table-primary': user.id === currentUser?.id }"
                      >
                        <td>
                          <span 
                            class="d-flex align-items-center justify-content-center rounded-circle"
                            :class="{
                              'bg-warning text-dark': user.rank === 1,
                              'bg-secondary bg-opacity-25': user.rank === 2,
                              'bg-danger bg-opacity-25': user.rank === 3,
                              'bg-light': user.rank > 3
                            }"
                            style="width: 32px; height: 32px;"
                          >
                            {{ user.rank }}
                          </span>
                        </td>
                        <td>
                          <div class="d-flex align-items-center">
                            <img 
                              :src="user.avatar || 'https://ui-avatars.com/api/?name=' + (user.name || 'User') + '&background=4e73df&color=fff&size=64'" 
                              class="rounded-circle me-2" 
                              width="32" 
                              height="32"
                              alt="User Avatar"
                            >
                            <div>
                              <div class="fw-medium">{{ user.name || 'Unknown' }}</div>
                              <small class="text-muted">@{{ user.username || 'user' }}</small>
                            </div>
                          </div>
                        </td>
                        <td class="text-end">
                          <span class="fw-medium">{{ (user.points || 0).toLocaleString() }}</span>
                          <div class="progress mt-1" style="height: 4px;">
                            <div 
                              class="progress-bar" 
                              role="progressbar" 
                              :style="{ width: (user.activity || 0) + '%' }"
                              :aria-valuenow="user.activity || 0" 
                              aria-valuemin="0" 
                              aria-valuemax="100"
                            ></div>
                          </div>
                        </td>
                        <td class="text-center">
                          <span class="badge bg-primary">Level {{ user.level || 1 }}</span>
                          <div v-if="user.remarks" class="small text-muted mt-1">{{ user.remarks }}</div>
                        </td>
                        <td class="text-end">
                          <button 
                            v-if="user.id !== currentUser?.id"
                            class="btn btn-sm btn-outline-primary"
                            @click="toggleFriend(user.id)"
                          >
                            <i class="bi bi-person-plus"></i>
                          </button>
                          <router-link 
                            v-else
                            to="/profile" 
                            class="btn btn-sm btn-outline-primary"
                          >
                            <i class="bi bi-person-lines-fill"></i>
                          </router-link>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              
              <!-- Friends Leaderboard -->
              <div class="tab-pane fade" id="friends" role="tabpanel" aria-labelledby="friends-tab">
                <div v-if="friends.length > 0">
                  <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                      <thead class="table-light">
                        <tr>
                          <th style="width: 50px;">#</th>
                          <th>User</th>
                          <th class="text-end">Points</th>
                          <th class="text-center">Level</th>
                          <th class="text-end">Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr 
                          v-for="user in friends" 
                          :key="user.id || user.rank"
                          :class="{ 'table-primary': user.id === currentUser?.id }"
                        >
                          <td>
                            <span 
                              class="d-flex align-items-center justify-content-center rounded-circle"
                              :class="{
                                'bg-warning text-dark': user.rank === 1,
                                'bg-secondary bg-opacity-25': user.rank === 2,
                                'bg-danger bg-opacity-25': user.rank === 3,
                                'bg-light': user.rank > 3
                              }"
                              style="width: 32px; height: 32px;"
                            >
                              {{ user.rank }}
                            </span>
                          </td>
                          <td>
                            <div class="d-flex align-items-center">
                              <img 
                                :src="user.avatar || 'https://ui-avatars.com/api/?name=' + (user.name || 'User') + '&background=4e73df&color=fff&size=64'" 
                                class="rounded-circle me-2" 
                                width="32" 
                                height="32"
                                alt="User Avatar"
                              >
                              <div>
                                <div class="fw-medium">{{ user.name || 'Unknown' }}</div>
                                <small class="text-muted">@{{ user.username || 'user' }}</small>
                              </div>
                            </div>
                          </td>
                          <td class="text-end">
                            <span class="fw-medium">{{ (user.points || 0).toLocaleString() }}</span>
                            <div class="progress mt-1" style="height: 4px;">
                              <div 
                                class="progress-bar" 
                                role="progressbar" 
                                :style="{ width: (user.activity || 0) + '%' }"
                                :aria-valuenow="user.activity || 0" 
                                aria-valuemin="0" 
                                aria-valuemax="100"
                              ></div>
                            </div>
                          </td>
                          <td class="text-center">
                            <span class="badge bg-primary">Level {{ user.level || 1 }}</span>
                            <div v-if="user.remarks" class="small text-muted mt-1">{{ user.remarks }}</div>
                          </td>
                          <td class="text-end">
                            <button 
                              v-if="user.id !== currentUser?.id"
                              class="btn btn-sm btn-outline-primary"
                              @click="toggleFriend(user.id)"
                            >
                              <i class="bi bi-person-plus"></i>
                            </button>
                            <router-link 
                              v-else
                              to="/profile" 
                              class="btn btn-sm btn-outline-primary"
                            >
                              <i class="bi bi-person-lines-fill"></i>
                            </router-link>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div v-else class="text-center py-5">
                  <div class="mb-3">
                    <i class="bi bi-people" style="font-size: 3rem; color: #6c757d;"></i>
                  </div>
                  <h5>No Friends Yet</h5>
                  <p class="text-muted">Connect with friends to see how you compare!</p>
                  <button class="btn btn-primary" @click="showFindFriends = true">
                    <i class="bi bi-person-plus me-1"></i> Find Friends
                  </button>
                </div>
              </div>
              
              <!-- Local Leaderboard -->
              <div class="tab-pane fade" id="local" role="tabpanel" aria-labelledby="local-tab">
                <div class="table-responsive">
                  <table class="table table-hover align-middle mb-0">
                    <thead class="table-light">
                      <tr>
                        <th style="width: 50px;">#</th>
                        <th>User</th>
                        <th class="text-end">Points</th>
                        <th class="text-center">Level</th>
                        <th class="text-end">Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-if="loading">
                        <td colspan="5" class="text-center py-4">
                          <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                          </div>
                        </td>
                      </tr>
                      <tr v-else-if="!localUsers || localUsers.length === 0">
                        <td colspan="5" class="text-center py-4">
                          <p class="text-muted mb-0">No users found</p>
                        </td>
                      </tr>
                      <tr 
                        v-else
                        v-for="user in localUsers" 
                        :key="user.id || user.rank"
                        :class="{ 'table-primary': user.id === currentUser?.id }"
                      >
                        <td>
                          <span 
                            class="d-flex align-items-center justify-content-center rounded-circle"
                            :class="{
                              'bg-warning text-dark': user.rank === 1,
                              'bg-secondary bg-opacity-25': user.rank === 2,
                              'bg-danger bg-opacity-25': user.rank === 3,
                              'bg-light': user.rank > 3
                            }"
                            style="width: 32px; height: 32px;"
                          >
                            {{ user.rank }}
                          </span>
                        </td>
                        <td>
                          <div class="d-flex align-items-center">
                            <img 
                              :src="user.avatar || 'https://ui-avatars.com/api/?name=' + (user.name || 'User') + '&background=4e73df&color=fff&size=64'" 
                              class="rounded-circle me-2" 
                              width="32" 
                              height="32"
                              alt="User Avatar"
                            >
                            <div>
                              <div class="fw-medium">{{ user.name || 'Unknown' }}</div>
                              <small class="text-muted">@{{ user.username || 'user' }}</small>
                            </div>
                          </div>
                        </td>
                        <td class="text-end">
                          <span class="fw-medium">{{ (user.points || 0).toLocaleString() }}</span>
                          <div class="progress mt-1" style="height: 4px;">
                            <div 
                              class="progress-bar" 
                              role="progressbar" 
                              :style="{ width: (user.activity || 0) + '%' }"
                              :aria-valuenow="user.activity || 0" 
                              aria-valuemin="0" 
                              aria-valuemax="100"
                            ></div>
                          </div>
                        </td>
                        <td class="text-center">
                          <span class="badge bg-primary">Level {{ user.level || 1 }}</span>
                          <div v-if="user.remarks" class="small text-muted mt-1">{{ user.remarks }}</div>
                        </td>
                        <td class="text-end">
                          <button 
                            v-if="user.id !== currentUser?.id"
                            class="btn btn-sm btn-outline-primary"
                            @click="toggleFriend(user.id)"
                          >
                            <i class="bi bi-person-plus"></i>
                          </button>
                          <router-link 
                            v-else
                            to="/profile" 
                            class="btn btn-sm btn-outline-primary"
                          >
                            <i class="bi bi-person-lines-fill"></i>
                          </router-link>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Right Column - User Stats & Badges -->
      <div class="col-lg-4">
        <!-- User Profile Card -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-body text-center">
            <div class="position-relative d-inline-block mb-3">
              <img 
                :src="currentUser?.avatar || 'https://ui-avatars.com/api/?name=' + (currentUser?.name || 'User') + '&background=4e73df&color=fff&size=128'" 
                class="rounded-circle border border-3 border-primary" 
                width="100" 
                height="100"
                alt="User Avatar"
              >
              <span v-if="currentUser?.rank" class="position-absolute bottom-0 end-0 bg-primary text-white rounded-circle d-flex align-items-center justify-content-center" 
                    style="width: 32px; height: 32px;">
                {{ currentUser.rank }}
              </span>
            </div>
            <h4 class="mb-1">{{ currentUser?.name || 'User' }}</h4>
            <p class="text-muted mb-3">@{{ currentUser?.username || 'username' }}</p>
            
            <div class="d-flex justify-content-center gap-4 mb-3">
              <div>
                <div class="h4 mb-0">{{ (currentUser?.points || 0).toLocaleString() }}</div>
                <small class="text-muted">Points</small>
              </div>
              <div>
                <div class="h4 mb-0">{{ currentUser?.quizzes || 0 }}</div>
                <small class="text-muted">Quizzes</small>
              </div>
              <div>
                <div class="h4 mb-0">{{ currentUser?.friends || 0 }}</div>
                <small class="text-muted">Friends</small>
              </div>
            </div>
            
            <div class="progress mb-3" style="height: 10px;">
              <div 
                class="progress-bar bg-success" 
                role="progressbar" 
                :style="{ width: (currentUser?.progress || 0) + '%' }"
                :aria-valuenow="currentUser?.progress || 0" 
                aria-valuemin="0" 
                aria-valuemax="100"
              ></div>
            </div>
            <p class="small text-muted mb-0">
              {{ (currentUser?.pointsToNextLevel || 0).toLocaleString() }} points to next level
            </p>
          </div>
        </div>
        
        <!-- Badges Earned -->
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-0">
            <h5 class="mb-0">Your Badges</h5>
          </div>
          <div class="card-body">
            <div v-if="currentUser?.badges && currentUser.badges.length > 0" class="row g-3">
              <div v-for="(badge, index) in currentUser.badges" :key="index" class="col-4 text-center">
                <div class="badge-icon mb-2" :title="badge.name">
                  <i :class="badge.icon" class="text-warning" style="font-size: 2rem;"></i>
                </div>
                <div class="small text-truncate">{{ badge.name }}</div>
              </div>
            </div>
            <div v-else class="text-center py-3">
              <p class="text-muted mb-3">No badges earned yet</p>
              <router-link to="/primary-dashboard/quiz" class="btn btn-sm btn-outline-primary">
                Take a Quiz to Earn Badges
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Find Friends Modal -->
    <div v-if="showFindFriends" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Find Friends</h5>
            <button type="button" class="btn-close" @click="showFindFriends = false"></button>
          </div>
          <div class="modal-body">
            <div class="input-group mb-3">
              <input 
                type="text" 
                class="form-control" 
                placeholder="Search by name or email..."
                v-model="friendSearch"
              >
              <button class="btn btn-primary" type="button">
                <i class="bi bi-search"></i>
              </button>
            </div>
            
            <div v-if="friendSearchResults.length > 0" class="friend-results">
              <div 
                v-for="user in friendSearchResults" 
                :key="user.id" 
                class="d-flex align-items-center justify-content-between p-2 border-bottom"
              >
                <div class="d-flex align-items-center">
                  <img 
                    :src="user.avatar || 'https://ui-avatars.com/api/?name=' + user.name + '&background=6c757d&color=fff&size=64'" 
                    class="rounded-circle me-2" 
                    width="40" 
                    height="40"
                    alt="User Avatar"
                  >
                  <div>
                    <div class="fw-medium">{{ user.name }}</div>
                    <small class="text-muted">@{{ user.username }}</small>
                  </div>
                </div>
                <button 
                  class="btn btn-sm" 
                  :class="user.isFriend ? 'btn-outline-secondary' : 'btn-primary'"
                  @click="toggleFriend(user.id)"
                >
                  <i :class="user.isFriend ? 'bi-person-check' : 'bi-person-plus'"></i>
                  {{ user.isFriend ? 'Friends' : 'Add Friend' }}
                </button>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <i class="bi bi-people" style="font-size: 2rem; color: #6c757d;"></i>
              <p class="text-muted mt-2">Search for friends to add them</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showFindFriends = false">Close</button>
          </div>
        </div>
      </div>
    </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../../services/api';
import { useAuthStore } from '../../stores/auth';

const authStore = useAuthStore();

// Data
const timeRange = ref('monthly');
const searchQuery = ref('');
const showFindFriends = ref(false);
const friendSearch = ref('');
const loading = ref(true);

// Current user data
const currentUser = ref({
  id: null,
  name: '',
  username: '',
  avatar: '',
  rank: 0,
  points: 0,
  quizzes: 0,
  friends: 0,
  progress: 0,
  pointsToNextLevel: 0,
  level: 1,
  badges: []
});

// Leaderboard data
const users = ref([]);
const leaderboardData = ref(null);
const errorMessage = ref('');

// Helper function to calculate level from points
const calculateLevel = (points) => {
  // Level = floor(points / 1000) + 1, minimum level 1
  return Math.max(1, Math.floor(points / 1000) + 1);
};

// Helper function to calculate progress to next level
const calculateProgress = (points) => {
  const currentLevel = calculateLevel(points);
  const pointsForCurrentLevel = (currentLevel - 1) * 1000;
  const pointsInCurrentLevel = points - pointsForCurrentLevel;
  const pointsNeededForNextLevel = currentLevel * 1000;
  const progress = (pointsInCurrentLevel / 1000) * 100;
  const pointsToNext = pointsNeededForNextLevel - points;
  return { progress: Math.min(100, Math.max(0, progress)), pointsToNext };
};

// Helper function to calculate activity percentage (simplified)
const calculateActivity = (points, maxPoints = 50000) => {
  // Activity based on points relative to max in leaderboard
  // This is a simplified calculation
  if (!points || points === 0) return 10;
  if (maxPoints === 0) return 10;
  return Math.min(100, Math.max(10, Math.floor((points / maxPoints) * 100)));
};

// Fetch leaderboard data from backend
const fetchLeaderboard = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';
    const response = await api.get('/primary/leaderboard');
    const data = response.data;
    
    console.log('Leaderboard data received:', data);
    
    leaderboardData.value = data;
    
    // Check if leaderboard data exists
    if (!data.leaderboard || !Array.isArray(data.leaderboard)) {
      console.error('Invalid leaderboard data structure:', data);
      users.value = [];
      loading.value = false;
      return;
    }
    
    // Find max points for activity calculation
    const maxPoints = data.leaderboard.length > 0 
      ? Math.max(...data.leaderboard.map(e => e.points || 0))
      : 50000;
    
    // Transform backend data to frontend format
    users.value = data.leaderboard.map((entry) => {
      const username = entry.user || entry.username || 'Unknown';
      const name = entry.name || username.split('@')[0] || username;
      const points = entry.points || 0;
      
      return {
        id: entry.id || `user_${entry.rank}`,
        name: name.charAt(0).toUpperCase() + name.slice(1),
        username: username,
        avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=4e73df&color=fff&size=64`,
        points: points,
        level: calculateLevel(points),
        activity: calculateActivity(points, maxPoints),
        isFriend: false, // Friends feature not implemented yet
        rank: entry.rank || 0,
        remarks: entry.remarks || ''
      };
    });
    
    console.log('Transformed users:', users.value);
    
    // Update current user info
    if (authStore.user) {
      const userProgress = calculateProgress(data.user_score || 0);
      const currentUserId = authStore.user.id;
      currentUser.value = {
        id: currentUserId,
        name: authStore.user.name || authStore.user.username || 'You',
        username: authStore.user.username || authStore.user.email || 'user',
        avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(authStore.user.name || authStore.user.username || 'User')}&background=4e73df&color=fff&size=128`,
        rank: data.user_rank || 0,
        points: data.user_score || 0,
        quizzes: 0, // Could fetch from dashboard
        friends: 0, // Friends feature not implemented
        progress: userProgress.progress,
        pointsToNextLevel: userProgress.pointsToNext,
        level: calculateLevel(data.user_score || 0),
        badges: [] // Badges feature not implemented yet
      };
      
      console.log('Current user:', currentUser.value);
    } else {
      console.warn('No user in auth store');
    }
  } catch (error) {
    console.error('Error fetching leaderboard:', error);
    console.error('Error details:', error.response?.data || error.message);
    errorMessage.value = error.response?.data?.error || 'Failed to load leaderboard data. Please try again.';
    users.value = [];
  } finally {
    loading.value = false;
  }
};

// Computed properties
const filteredUsers = computed(() => {
  if (!users.value || users.value.length === 0) {
    return [];
  }
  
  let filtered = users.value;
  
  // Apply search filter if search query exists
  if (searchQuery.value && searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    filtered = filtered.filter(user => 
      (user.name && user.name.toLowerCase().includes(query)) ||
      (user.username && user.username.toLowerCase().includes(query))
    );
  }
  
  // Sort by points (descending)
  return filtered.sort((a, b) => (b.points || 0) - (a.points || 0));
});

const friends = computed(() => {
  if (!users.value || users.value.length === 0) {
    return [];
  }
  return users.value
    .filter(user => user.isFriend && user.id !== currentUser.value?.id)
    .sort((a, b) => (b.points || 0) - (a.points || 0));
});

const localUsers = computed(() => {
  // In a real app, this would filter users by location
  // For now, just show top 10 users
  if (!users.value || users.value.length === 0) {
    return [];
  }
  return users.value
    .slice(0, 10)
    .sort((a, b) => (b.points || 0) - (a.points || 0));
});

const friendSearchResults = computed(() => {
  if (!friendSearch.value) return [];
  
  return users.value
    .filter(user => 
      (user.name.toLowerCase().includes(friendSearch.value.toLowerCase()) ||
       user.username.toLowerCase().includes(friendSearch.value.toLowerCase())) &&
      user.id !== currentUser.value.id
    )
    .slice(0, 5);
});

// Methods
const toggleFriend = (userId) => {
  const user = users.value.find(u => u.id === userId);
  if (user) {
    user.isFriend = !user.isFriend;
    
    // Update friends count for current user
    if (user.id !== currentUser.value.id) {
      currentUser.value.friends += user.isFriend ? 1 : -1;
    }
  }
};

// Lifecycle hooks
onMounted(() => {
  fetchLeaderboard();
});
</script>

<style scoped>
.community-leaderboard {
  padding: 1.5rem;
}

.card {
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
}

.nav-tabs .nav-link {
  border: none;
  color: #6c757d;
  font-weight: 500;
  padding: 0.75rem 1.25rem;
  transition: all 0.2s;
}

.nav-tabs .nav-link.active {
  color: #4e73df;
  background: transparent;
  border-bottom: 3px solid #4e73df;
}

.nav-tabs .nav-link:hover:not(.active) {
  color: #4e73df;
  border-bottom: 3px solid transparent;
}

.badge-icon {
  transition: transform 0.2s;
}

.badge-icon:hover {
  transform: scale(1.1);
}

/* Custom scrollbar for table */
.table-responsive {
  max-height: 600px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #dee2e6 #f8f9fa;
}

.table-responsive::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.table-responsive::-webkit-scrollbar-track {
  background: #f8f9fa;
}

.table-responsive::-webkit-scrollbar-thumb {
  background-color: #dee2e6;
  border-radius: 3px;
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .community-leaderboard {
    padding: 1rem;
  }
  
  .table th, .table td {
    padding: 0.75rem;
  }
  
  .nav-tabs .nav-link {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
  }
}

/* Animation for table rows */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

tbody tr {
  animation: fadeIn 0.3s ease-out forwards;
  opacity: 0;
}

tbody tr:nth-child(1) { animation-delay: 0.1s; }
tbody tr:nth-child(2) { animation-delay: 0.15s; }
tbody tr:nth-child(3) { animation-delay: 0.2s; }
tbody tr:nth-child(4) { animation-delay: 0.25s; }
tbody tr:nth-child(5) { animation-delay: 0.3s; }
tbody tr:nth-child(n+6) { animation-delay: 0.35s; }

/* Custom styling for the select dropdown */
select.form-select {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M2 5l6 6 6-6'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 16px 12px;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  padding-right: 2.25rem;
  border: 1px solid #d1d3e2;
  border-radius: 0.35rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

select.form-select:focus {
  border-color: #bac8f3;
  box-shadow: 0 0 0 0.25rem rgba(78, 115, 223, 0.25);
}

/* Modal styles */
.modal-content {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.modal-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 1.25rem 1.5rem;
}

.modal-footer {
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  padding: 1rem 1.5rem;
}

.friend-results {
  max-height: 300px;
  overflow-y: auto;
  margin: 0 -1.5rem;
  padding: 0 1.5rem;
}
</style>
