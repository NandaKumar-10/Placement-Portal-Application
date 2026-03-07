<template>
  <div class="container-fluid p-0 d-flex bg-light min-vh-100 font-sans">
    <div class="sidebar d-flex flex-column p-3 text-white">
      <div class="d-flex align-items-center mb-5 mt-2 px-2">
        <i class="bi bi-mortarboard-fill fs-3 me-2"></i>
        <h4 class="mb-0 fw-bold tracking-wide">Placement</h4>
      </div>
      <ul class="nav nav-pills flex-column mb-auto gap-2">
        <li>
          <router-link to="/student/dashboard" class="nav-link text-white d-flex align-items-center">
            <i class="bi bi-house-door me-3 fs-5"></i> My Profile
          </router-link>
        </li>
        <li>
          <router-link to="/student/drive" class="nav-link text-white d-flex align-items-center">
            <i class="bi bi-search me-3 fs-5"></i> Find Placement Drive
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/student/history" class="nav-link active d-flex align-items-center">
            <i class="bi bi-clock-history me-3 fs-5"></i> History
          </router-link>
        </li>
      </ul>
      <div class="mt-auto px-2 mb-2">
        <a href="#" @click.prevent="handleLogout" class="text-white text-decoration-none d-flex align-items-center opacity-75 hover-opacity-100">
          <i class="bi bi-box-arrow-right me-3 fs-5"></i> Logout
        </a>
      </div>
    </div>

    <div class="main-content flex-grow-1 p-4 px-md-5">
      <div class="d-flex justify-content-between align-items-center mb-4 mt-2">
        <h2 class="fw-bold mb-0 text-dark">Application History</h2>
        <button @click="triggerExport" :disabled="isExporting" class="btn btn-primary d-flex align-items-center gap-2">
          <span v-if="isExporting" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          <i v-else class="bi bi-cloud-download"></i>
          {{ isExporting ? 'Starting Export...' : 'Export to CSV' }}
        </button>
      </div>

      <div class="card border-0 shadow-sm rounded-4 p-4">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
        </div>

        <div v-else>
          <div v-if="history.length > 0" class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="text-muted" style="border-bottom: 2px solid #f4f4f4;">
                <tr>
                  <th class="fw-semibold pb-3 border-0">Company</th>
                  <th class="fw-semibold pb-3 border-0">Role</th>
                  <th class="fw-semibold pb-3 border-0">Date</th>
                  <th class="fw-semibold pb-3 border-0">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="app in history" :key="app.application_id">
                  <td class="py-3 border-light fw-bold text-dark">{{ app.company }}</td>
                  <td class="py-3 border-light text-secondary">{{ app.role }}</td>
                  <td class="py-3 border-light text-secondary">{{ app.applied_on }}</td>
                  <td class="py-3 border-light">
                    <span class="badge rounded-pill fw-medium px-3 py-2" 
                          :class="statusClass(app.status)">
                      {{ app.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div v-else class="text-center py-5">
            <i class="bi bi-archive display-4 text-muted mb-3 opacity-50"></i>
            <h5 class="fw-bold text-dark">No history found</h5>
            <p class="text-muted">Completed or rejected applications will appear here.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const router = useRouter();
const history = ref([]);
const loading = ref(true);

const fetchHistory = async () => {
  loading.value = true;
  try {
    const res = await api.get('/student/history'); 
    history.value = res.data.history;
  } 
  catch (error) {
    console.error("Error fetching history:", error);
  } 
  finally {
    loading.value = false;
  }
};

const isExporting = ref(false);

const triggerExport = async () => {
  isExporting.value = true;
  try {
    const res = await api.post('/student/export-history');
    alert(res.data.message);
  } 
  catch (error) {
    console.error("Export failed:", error);
  } 
  finally {
    isExporting.value = false;
  }
};

const statusClass = (status) => {
  return {
    'bg-success-subtle text-success': ['Hired', 'Accepted','Interview Scheduled'].includes(status),
    'bg-danger-subtle text-danger': status === 'Rejected',
    'bg-warning-subtle text-warning': status === 'Shortlisted',
    'badge bg-dark': status === 'Applied'
  };
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.dispatchEvent(new Event("auth-changed"));
  router.push('/');
};

onMounted(fetchHistory);
</script>

<style scoped>
.font-sans { 
    font-family: 'Inter', sans-serif; 
}

.sidebar { 
    width: 260px; 
    background-color: #111827; 
}

.nav-pills .nav-link { 
    border-radius: 8px; 
    padding: 12px 16px; 
    color: #9ca3af !important; 
}

.nav-pills .nav-link.active { 
    background-color: #1f2937 !important; 
    color: white !important; 
}

.bg-success-subtle { 
    background-color: #dcfce7 !important; 
}

.bg-danger-subtle { 
    background-color: #fee2e2 !important; 
}
</style>