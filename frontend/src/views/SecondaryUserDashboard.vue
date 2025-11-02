<template>
  <div class="container my-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3>RWA Dashboard</h3>
      <div>
        <RouterLink to="/rwa/campaigns" class="btn btn-outline-primary me-2">Campaigns</RouterLink>
        <RouterLink to="/rwa/households" class="btn btn-outline-secondary">Households</RouterLink>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-md-3" v-for="(kpi, idx) in kpis" :key="idx">
        <div class="card text-center p-3 shadow-sm">
          <h6 class="mb-1">{{ kpi.title }}</h6>
          <h4 class="m-0">{{ kpi.value }}</h4>
          <small class="text-muted">{{ kpi.subtitle }}</small>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Left Section -->
      <div class="col-md-8">
        <div class="card p-3 mb-3 shadow-sm">
          <h5>Daily Waste Pickup (last 30 days)</h5>
          <img
            v-if="charts.daily"
            :src="charts.daily"
            class="img-fluid mt-2"
            alt="daily chart"
          />
          <div v-else class="text-center py-5 text-muted">
            No chart available
          </div>
        </div>

        <div class="card p-3 shadow-sm">
          <h5>Household Performance Table</h5>
          <div class="table-responsive mt-2">
            <table class="table table-sm table-striped align-middle">
              <thead class="table-light">
                <tr>
                  <th>Household</th>
                  <th>Segregation %</th>
                  <th>Recyclable %</th>
                  <th>Last Pickup</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="h in topHouseholds" :key="h.id">
                  <td>{{ h.name }}</td>
                  <td>{{ h.segregation_pct }}%</td>
                  <td>{{ h.recyclable_pct }}%</td>
                  <td>{{ h.last_pickup }}</td>
                  <td>
                    <span
                      :class="{
                        'text-success fw-semibold': h.status === 'good',
                        'text-danger fw-semibold': h.status === 'poor'
                      }"
                    >
                      {{ h.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Right Section -->
      <div class="col-md-4">
        <div class="card p-3 mb-3 shadow-sm">
          <h6>Area Summary</h6>
          <ul class="list-unstyled mb-0">
            <li
              v-for="area in areaSummary"
              :key="area.name"
              class="py-2 border-bottom"
            >
              <strong>{{ area.name }}</strong>
              <div class="small text-muted">
                Compliance: {{ area.compliance }}%
              </div>
            </li>
          </ul>
        </div>

        <div class="card p-3 shadow-sm">
          <h6>Quick Actions</h6>
          <div class="d-grid gap-2 mt-2">
            <RouterLink
              class="btn btn-outline-success"
              to="/rwa/campaigns/create"
              >Create Campaign</RouterLink
            >
            <RouterLink class="btn btn-outline-info" to="/rwa/charts"
              >View Charts</RouterLink
            >
            <RouterLink
              class="btn btn-outline-secondary"
              to="/rwa/monthly_report"
              >Monthly Report</RouterLink
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const kpis = ref([]);
const charts = ref({ daily: null });
const topHouseholds = ref([]);
const areaSummary = ref([]);

async function fetchDashboard() {
  try {
    const res = await axios.get("/api/rwa/dashboard");
    const d = res.data;

    kpis.value = d.kpis || [
      { title: "Households", value: d.totalHouseholds || 0, subtitle: "Total" },
      {
        title: "Compliance",
        value: d.compliancePct || "0%",
        subtitle: "Avg segregation",
      },
      {
        title: "Recyclable",
        value: d.recyclablePct || "0%",
        subtitle: "Avg recyclable",
      },
      { title: "Active Campaigns", value: d.activeCampaigns || 0, subtitle: "" },
    ];

    charts.value.daily =
      d.charts && d.charts.daily_jpg
        ? `/static/charts/${d.charts.daily_jpg}`
        : null;

    topHouseholds.value = d.topHouseholds || [];
    areaSummary.value = d.areas || [];
  } catch (e) {
    console.error("Dashboard fetch failed", e);
  }
}

onMounted(fetchDashboard);
</script>

<style scoped>
.card {
  border-radius: 12px;
}
.table thead th {
  font-size: 0.9rem;
  text-transform: uppercase;
}
.table tbody td {
  font-size: 0.9rem;
}
.text-success {
  color: #198754 !important;
}
.text-danger {
  color: #dc3545 !important;
}
</style>
