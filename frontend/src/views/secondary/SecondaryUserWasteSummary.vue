<template>
  <div class="secondary-waste-summary">
    <div class="container">
      <div class="row mb-4">
        <div class="col-12">
          <h2 class="text-white fw-bold mb-3">WASTE SUMMARY</h2>
          <p class="text-white-50">View comprehensive waste statistics and trends for your RWA</p>
        </div>
      </div>

      <!-- Summary Cards -->
      <div class="row mb-4">
        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Total Waste Collected</h6>
              <h3 class="card-text fw-bold text-primary">250 KG</h3>
              <p class="card-text text-muted small">This month</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Waste Diverted</h6>
              <h3 class="card-text fw-bold text-success">180 KG</h3>
              <p class="card-text text-muted small">Recycled/Composted</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Landfill Waste</h6>
              <h3 class="card-text fw-bold text-danger">70 KG</h3>
              <p class="card-text text-muted small">Sent to landfill</p>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3 mb-3">
          <div class="card shadow-lg h-100">
            <div class="card-body text-center">
              <h6 class="card-title text-muted">Diversion Rate</h6>
              <h3 class="card-text fw-bold text-info">72%</h3>
              <p class="card-text text-muted small">Waste diverted</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Detailed Table -->
      <div class="row">
        <div class="col-12">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white">
              <h5 class="card-title mb-0">WASTE BREAKDOWN BY CATEGORY</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th>Category</th>
                      <th>Quantity (KG)</th>
                      <th>Percentage</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Organic Waste</td>
                      <td>120 KG</td>
                      <td>48%</td>
                      <td><span class="badge bg-success">Composted</span></td>
                    </tr>
                    <tr>
                      <td>Recyclable Waste</td>
                      <td>80 KG</td>
                      <td>32%</td>
                      <td><span class="badge bg-info">Recycled</span></td>
                    </tr>
                    <tr>
                      <td>Hazardous Waste</td>
                      <td>20 KG</td>
                      <td>8%</td>
                      <td><span class="badge bg-warning">Processed</span></td>
                    </tr>
                    <tr>
                      <td>Landfill Waste</td>
                      <td>30 KG</td>
                      <td>12%</td>
                      <td><span class="badge bg-danger">Landfill</span></td>
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
// Secondary User Waste Summary component
</script>

<style scoped>
.secondary-waste-summary {
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

.badge {
  padding: 0.5rem 0.75rem;
  font-size: 0.85rem;
}
</style>
