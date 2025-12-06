<template>
  <div class="layout-wrapper">
    <!-- Navbar -->
    <nav
      class="navbar navbar-expand-lg fixed-top"
      style="
        background-color: #f8f9fa;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      "
    >
      <div class="container-fluid">
        <!-- Navbar Brand -->
        <router-link
          to="/collector-dashboard"
          class="navbar-brand fw-bold text-success"
        >
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
                to="/collector-dashboard"
                :class="['nav-link', 'fw-semibold', 'text-dark', isActive('/collector-dashboard') ? 'active' : '']"
              >
                COLLECTOR PICKUP DASHBOARD
              </router-link>
            </li>
          </ul>

          <!-- Theme Toggle (Center) -->
          <div class="navbar-nav mx-auto">
            <ThemeToggle />
          </div>

          <!-- Right side items -->
          <ul class="navbar-nav">
            <li class="nav-item">
              <span class="nav-link fw-semibold text-dark">
                <i class="bi bi-clock me-1"></i> {{ currentDateTime }}
              </span>
            </li>
            <li class="nav-item">
              <router-link
                to="/"
                class="btn btn-outline-danger btn-sm ms-2 fw-semibold"
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

    <!-- Footer -->
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "../../stores/auth";
import ThemeToggle from "../ThemeToggle.vue";
import AppFooter from "./AppFooter.vue";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const currentDateTime = ref("");

const updateDateTime = () => {
  const now = new Date();
  // Format date as YYYY-MM-DD using local timezone
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  
  currentDateTime.value = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
};

const isActive = (path) => {
  return route.path === path;
};

const handleLogout = () => {
  authStore.logout();
  router.push("/signin");
};

let datetimeInterval;

onMounted(() => {
  updateDateTime();
  datetimeInterval = setInterval(updateDateTime, 1000);
});

onUnmounted(() => {
  if (datetimeInterval) {
    clearInterval(datetimeInterval);
  }
});
</script>

<style scoped>
.navbar {
  padding: 0.75rem 2rem;
}

.navbar-brand {
  font-size: 1.75rem;
  font-weight: 700;
  color: #2c3e50;
  letter-spacing: 0.5px;
}

.nav-link {
  font-size: 1rem;
  padding: 0.75rem 1.25rem;
  transition: all 0.2s ease;
  position: relative;
  color: #2c3e50 !important;
}

.nav-link:hover {
  color: #4a6baf !important;
}

.nav-link.active {
  color: #4a6baf !important;
  font-weight: 600;
}

.nav-link.active::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 1.25rem;
  right: 1.25rem;
  height: 3px;
  background-color: #4a6baf;
  border-radius: 3px 3px 0 0;
}

.navbar-toggler {
  border: none;
  padding: 0.5rem;
}

.navbar-toggler:focus {
  box-shadow: none;
  outline: none;
}

.btn-outline-danger {
  border-width: 2px;
  padding: 0.35rem 1rem;
  margin-left: 0.75rem;
}

.navbar-nav .nav-item {
  display: flex;
  align-items: center;
}

.layout-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  padding-top: 80px;
  flex: 1;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
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
