<template>
  <div class="secondary-user-dashboard">
    <div class="row">
      <!-- Container 1: Waste Summary -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-info text-white">
            <h5 class="card-title mb-0">WASTE SUMMARY</h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5">RWA WASTE OVERVIEW</p>
            <p class="card-text text-muted">View comprehensive waste statistics for your RWA</p>
            <div class="mt-auto">
              <router-link to="/secondary-dashboard/waste-summary" class="btn btn-primary w-100">
                DETAILS
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Container 2: Campaigns -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-success text-white">
            <h5 class="card-title mb-0">CAMPAIGNS</h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5">MANAGE CAMPAIGNS</p>
            <p class="card-text text-muted">View and manage waste management campaigns</p>
            <div class="mt-auto">
              <router-link to="/secondary-dashboard/campaigns" class="btn btn-primary w-100">
                DETAILS
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Container 3: RWA Leaderboard -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-warning text-dark">
            <h5 class="card-title mb-0">RWA LEADERBOARD</h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5">COMMUNITY RANKINGS</p>
            <p class="card-text text-muted">View RWA rankings and performance metrics</p>
            <div class="mt-auto">
              <router-link to="/secondary-dashboard/rwa-leaderboard" class="btn btn-primary w-100">
                DETAILS
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Container 4: Pickup Details -->
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shadow-lg h-100">
          <div class="card-header bg-secondary text-white">
            <h5 class="card-title mb-0">PICKUP DETAILS</h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text fs-5">SCHEDULED PICKUPS</p>
            <p class="card-text text-muted">View waste pickup schedules and details</p>
            <div class="mt-auto">
              <router-link to="/secondary-dashboard/pickup-details" class="btn btn-primary w-100">
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
// Secondary User Dashboard component
</script>

<style scoped>
.secondary-user-dashboard {
  padding: 1.5rem;
}

.card {
  border: none;
  border-radius: 0.5rem;
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

.card-header {
  border-bottom: none;
  border-radius: 0.5rem 0.5rem 0 0 !important;
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}
</style>
