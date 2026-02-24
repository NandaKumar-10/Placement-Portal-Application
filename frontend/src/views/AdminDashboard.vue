<template>
  <div class="dashboard">
    <h1>Admin Dashboard</h1>
    
    <div v-if="loading">Loading stats...</div>
    
    <div v-else class="stats-grid">
      <div class="card">
        <h3>Total Students</h3>
        <p>{{ stats.overview.total_students }}</p>
      </div>
      <div class="card">
        <h3>Total Companies</h3>
        <p>{{ stats.overview.total_companies }}</p>
      </div>
      <div class="card">
        <h3>Placed Students</h3>
        <p>{{ stats.placement_performance.placed_students }}</p>
      </div>
      <div class="card">
        <h3>Placement Rate</h3>
        <p>{{ stats.placement_performance.placement_rate_percentage }}%</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import adminService from '@/services/adminService.js';

const stats = ref(null);
const loading = ref(true);

onMounted(async () => {
  try {
    const response = await adminService.getStatistics();
    stats.value = response.data;
  } catch (error) {
    console.error("Failed to load stats", error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}
.card {
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  background: #f9f9f9;
}
</style>