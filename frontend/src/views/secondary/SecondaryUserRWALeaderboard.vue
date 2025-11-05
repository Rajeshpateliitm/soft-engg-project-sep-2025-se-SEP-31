<template>
  <div class="secondary-rwa-leaderboard">
    <div class="container">
      <div class="row mb-4">
        <div class="col-12">
          <h2 class="text-white fw-bold mb-3">RWA LEADERBOARD</h2>
          <p class="text-white-50">View RWA rankings based on waste management performance</p>
        </div>
      </div>

      <!-- Leaderboard Stats -->
      <div class="row mb-4">
        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Total RWAs</h6>
              <h3 class="card-text fw-bold text-primary">45</h3>
              <p class="card-text text-muted small">Participating</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Your Rank</h6>
              <h3 class="card-text fw-bold text-success">5</h3>
              <p class="card-text text-muted small">Out of 45</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Your Points</h6>
              <h3 class="card-text fw-bold text-info">8500</h3>
              <p class="card-text text-muted small">Total score</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Diversion Rate</h6>
              <h3 class="card-text fw-bold text-warning">72%</h3>
              <p class="card-text text-muted small">Waste diverted</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Leaderboard Table -->
      <div class="row">
        <div class="col-12">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white">
              <h5 class="card-title mb-0">TOP RWA PERFORMERS</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th>Rank</th>
                      <th>RWA Name</th>
                      <th>Points</th>
                      <th>Waste Diverted (KG)</th>
                      <th>Diversion Rate</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><span class="badge bg-warning text-dark">1</span></td>
                      <td><strong>Green Valley RWA</strong></td>
                      <td>9200</td>
                      <td>450 KG</td>
                      <td>85%</td>
                      <td><span class="badge bg-success">Leader</span></td>
                    </tr>
                    <tr>
                      <td><span class="badge bg-secondary">2</span></td>
                      <td><strong>Eco Homes RWA</strong></td>
                      <td>8900</td>
                      <td>420 KG</td>
                      <td>82%</td>
                      <td><span class="badge bg-info">Active</span></td>
                    </tr>
                    <tr>
                      <td><span class="badge bg-secondary">3</span></td>
                      <td><strong>Clean City RWA</strong></td>
                      <td>8700</td>
                      <td>400 KG</td>
                      <td>80%</td>
                      <td><span class="badge bg-info">Active</span></td>
                    </tr>
                    <tr>
                      <td><span class="badge bg-secondary">4</span></td>
                      <td><strong>Waste Warriors RWA</strong></td>
                      <td>8600</td>
                      <td>390 KG</td>
                      <td>78%</td>
                      <td><span class="badge bg-info">Active</span></td>
                    </tr>
                    <tr class="table-active">
                      <td><span class="badge bg-primary">5</span></td>
                      <td><strong>Your RWA</strong></td>
                      <td>8500</td>
                      <td>380 KG</td>
                      <td>72%</td>
                      <td><span class="badge bg-primary">You</span></td>
                    </tr>
                    <tr>
                      <td><span class="badge bg-secondary">6</span></td>
                      <td><strong>Sustainable Living RWA</strong></td>
                      <td>8300</td>
                      <td>360 KG</td>
                      <td>70%</td>
                      <td><span class="badge bg-info">Active</span></td>
                    </tr>
                    <tr>
                      <td><span class="badge bg-secondary">7</span></td>
                      <td><strong>Green Initiative RWA</strong></td>
                      <td>8100</td>
                      <td>340 KG</td>
                      <td>68%</td>
                      <td><span class="badge bg-info">Active</span></td>
                    </tr>
                    <tr>
                      <td><span class="badge bg-secondary">8</span></td>
                      <td><strong>Community Care RWA</strong></td>
                      <td>7900</td>
                      <td>320 KG</td>
                      <td>65%</td>
                      <td><span class="badge bg-info">Active</span></td>
                    </tr>
                    <tr>
                      <td><span class="badge bg-secondary">9</span></td>
                      <td><strong>Eco Friendly RWA</strong></td>
                      <td>7700</td>
                      <td>300 KG</td>
                      <td>62%</td>
                      <td><span class="badge bg-info">Active</span></td>
                    </tr>
                    <tr>
                      <td><span class="badge bg-secondary">10</span></td>
                      <td><strong>Future Green RWA</strong></td>
                      <td>7500</td>
                      <td>280 KG</td>
                      <td>60%</td>
                      <td><span class="badge bg-info">Active</span></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Secondary User RWA Leaderboard component
</script>

<style scoped>
.secondary-rwa-leaderboard {
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

.table {
  margin-bottom: 0;
}

.table-hover tbody tr:hover {
  background-color: #f5f5f5;
}

.table-active {
  background-color: #e7f3ff !important;
}

.badge {
  padding: 0.5rem 0.75rem;
  font-size: 0.85rem;
}
</style>
