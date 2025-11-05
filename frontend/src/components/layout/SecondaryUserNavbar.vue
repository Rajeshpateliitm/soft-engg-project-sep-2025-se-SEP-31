<template>
  <div>
    <!-- Navbar -->
    <nav 
      class="navbar navbar-expand-lg navbar-light fixed-top" 
      :style="navbarStyle"
      @mouseenter="navbarHover = true"
      @mouseleave="navbarHover = false"
    >
      <div class="container-fluid">
        <!-- Navbar Brand -->
        <router-link to="/" class="navbar-brand fw-bold text-dark">
          WASTEWISE
        </router-link>
        
        <!-- Navbar Toggler -->
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <!-- Navbar Items -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link 
                to="/secondary-dashboard" 
                class="nav-link fw-semibold"
                :class="{ 'text-white': navbarHover, 'text-dark': !navbarHover }"
                active-class="active"
              >
                DASHBOARD
              </router-link>
            </li>
            <li class="nav-item">
              <router-link 
                to="/secondary-dashboard/waste-summary" 
                class="nav-link fw-semibold"
                :class="{ 'text-white': navbarHover, 'text-dark': !navbarHover }"
                active-class="active"
              >
                WASTE SUMMARY
              </router-link>
            </li>
            <li class="nav-item">
              <router-link 
                to="/secondary-dashboard/campaigns" 
                class="nav-link fw-semibold"
                :class="{ 'text-white': navbarHover, 'text-dark': !navbarHover }"
                active-class="active"
              >
                CAMPAIGNS
              </router-link>
            </li>
          </ul>
          
          <!-- Right side items -->
          <ul class="navbar-nav">
            <li class="nav-item">
              <span 
                class="nav-link fw-semibold"
                :class="{ 'text-white': navbarHover, 'text-dark': !navbarHover }"
              >
                <i class="bi bi-clock me-1"></i> {{ currentDateTime }}
              </span>
            </li>
            <li class="nav-item">
              <router-link 
                to="/" 
                class="btn btn-outline-danger btn-sm ms-2"
                @click="handleLogout"
              >
                LOGOUT
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    
    <!-- Main Content Area -->
    <div class="main-content">
      <div class="container py-4">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const navbarHover = ref(false);
const currentDateTime = ref('');

const navbarStyle = computed(() => {
  const baseStyle = {
    border: '2px solid #000',
    transition: 'all 0.3s ease',
    padding: '10px 0',
    zIndex: 1030
  };
  
  return {
    ...baseStyle,
    backgroundColor: navbarHover.value ? '#464A9E' : 'transparent',
    boxShadow: navbarHover.value ? '0 4px 12px rgba(0, 0, 0, 0.1)' : 'none'
  };
});

const updateDateTime = () => {
  const now = new Date();
  // Format as ISO 8601 format
  currentDateTime.value = now.toISOString().split('T')[0] + ' ' + now.toISOString().split('T')[1].substring(0, 8);
};

const handleLogout = () => {
  // Add logout logic here
  console.log('Logging out...');
  // router.push('/login'); // Uncomment when you have a login route
};

let datetimeInterval;

onMounted(() => {
  updateDateTime();
  datetimeInterval = setInterval(updateDateTime, 1000); // Update every second for ISO format
});

onUnmounted(() => {
  if (datetimeInterval) {
    clearInterval(datetimeInterval);
  }
});
</script>

<style scoped>
.navbar {
  transition: all 0.3s ease;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.nav-link {
  position: relative;
  padding: 0.5rem 1rem;
  margin: 0 0.25rem;
  transition: color 0.3s ease;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background-color: currentColor;
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.nav-link:hover::after,
.nav-link.active::after {
  width: 80%;
}

.main-content {
  padding-top: 80px;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Fade transition for route changes */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive adjustments */
@media (max-width: 991.98px) {
  .navbar-collapse {
    background-color: white;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-top: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .nav-link {
    color: #333 !important;
    padding: 0.5rem 0;
  }
  
  .main-content {
    padding-top: 60px;
  }
}
</style>
