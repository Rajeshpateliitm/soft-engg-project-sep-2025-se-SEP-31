<template>
  <div class="home">
    <div class="hero-section text-center py-5">
      <h1 class="display-4 fw-bold mb-4">Welcome to WasteWise</h1>
      <p class="lead mb-4">Your smart waste management solution</p>
      <div class="d-flex justify-content-center gap-3">
        <router-link to="/register" class="btn btn-primary btn-lg">
          Get Started
        </router-link>
      </div>
    </div>

    <div class="features-section py-5">
      <div class="container">
        <h2 class="text-center mb-5">Features</h2>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="card h-100 shadow-sm">
              <div class="card-body text-center">
                <div class="feature-icon mb-3">
                  <i class="bi bi-graph-up-arrow fs-1 text-primary"></i>
                </div>
                <h3>Waste Tracking</h3>
                <p>Track your waste disposal activities and monitor your environmental impact.</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card h-100 shadow-sm">
              <div class="card-body text-center">
                <div class="feature-icon mb-3">
                  <i class="bi bi-trophy fs-1 text-primary"></i>
                </div>
                <h3>Challenges</h3>
                <p>Participate in waste reduction challenges and climb the leaderboard.</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card h-100 shadow-sm">
              <div class="card-body text-center">
                <div class="feature-icon mb-3">
                  <i class="bi bi-chat-dots fs-1 text-primary"></i>
                </div>
                <h3>Smart Assistant</h3>
                <p>Get personalized tips and answers to your waste management questions.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// You can add any component logic here if needed
</script>

<style scoped>
.home {
  min-height: calc(100vh - 76px);
  background-color: #f8f9fa;
}

.hero-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 4rem 1rem;
  margin-bottom: 2rem;
}

.features-section {
  padding: 2rem 0;
}

.feature-icon {
  color: #4e73df;
  margin-bottom: 1rem;
}

.card {
  border: none;
  border-radius: 0.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
}

.btn-primary {
  padding: 0.5rem 2rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

h1, h2, h3 {
  color: #2c3e50;
}

.lead {
  color: #6c757d;
  font-size: 1.25rem;
}
</style>
