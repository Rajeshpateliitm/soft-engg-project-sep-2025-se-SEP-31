<template>
  <nav 
    class="navbar navbar-expand-lg fixed-top"
    style="background-color: #f8f9fa; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
  >
    <div class="container-fluid">
      <!-- App Name / Brand -->
      <router-link to="/" class="navbar-brand fw-bold text-dark">
        WASTEWISE
      </router-link>
      
      <!-- Navbar Toggler -->
      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#standardNavbarNav"
        aria-controls="standardNavbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <!-- Navbar Items -->
      <div class="collapse navbar-collapse" id="standardNavbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link 
              to="/signin" 
              class="nav-link fw-semibold text-dark"
              active-class="active"
            >
              LOGIN
            </router-link>
          </li>
          <li class="nav-item">
            <router-link 
              to="/register" 
              class="nav-link fw-semibold text-dark"
              active-class="active"
            >
              REGISTER
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
// Standard navbar for non-authenticated pages (Home, Login, Register)
</script>

<style scoped>
.navbar {
  z-index: 1030;
}

.nav-link {
  padding: 0.5rem 1rem;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #4e73df !important;
}

.nav-link.active {
  color: #4e73df !important;
  font-weight: 600;
}

.navbar-brand {
  font-size: 1.5rem;
  letter-spacing: 1px;
  transition: color 0.2s;
}

.navbar-brand:hover {
  color: #4e73df !important;
}
</style>

