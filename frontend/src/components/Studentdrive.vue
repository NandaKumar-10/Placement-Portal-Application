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
        <li class="nav-item">
          <a href="/student/drive" class="nav-link active d-flex align-items-center">
            <i class="bi bi-search me-3 fs-5"></i> Find Placement Drive
          </a>
        </li>
        <li>
          <router-link to="/student/history" class="nav-link text-white d-flex align-items-center">
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
        <h2 class="fw-bold mb-0 text-dark">Available Drives</h2>
      </div>

      <div class="card border-0 shadow-sm rounded-4 mb-4 p-3 bg-white">
        <div class="row g-3 align-items-end">
          <div class="col-md-4">
            <label class="form-label small fw-semibold text-muted mb-1">Target Branch</label>
            <input type="text" class="form-control bg-light" v-model="filters.branch" placeholder="e.g. Computer Science">
          </div>
          <div class="col-md-4">
            <label class="form-label small fw-semibold text-muted mb-1">Max Eligibility CGPA</label>
            <input type="number" step="0.1" class="form-control bg-light" v-model="filters.cgpa" placeholder="e.g. 7.5">
          </div>
          <div class="col-md-4 d-flex gap-2">
            <button @click="fetchDrives" class="btn btn-primary fw-semibold px-4">Filter</button>
            <button @click="clearFilters" class="btn btn-light fw-semibold px-4 border">Clear</button>
          </div>
        </div>
      </div>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="text-muted mt-2">Loading opportunities...</p>
      </div>

      <div class="row g-4" v-else-if="drives.length > 0">
        <div class="col-md-6 col-lg-4" v-for="drive in drives" :key="drive.drive_id">
          <div class="card h-100 border-0 shadow-sm rounded-4 drive-card transition-all">
            <div class="card-body p-4">
              
              <div class="d-flex justify-content-between align-items-start mb-3">
                <div class="bg-blue-light text-primary rounded-3 d-flex justify-content-center align-items-center" style="width: 48px; height: 48px;">
                  <i class="bi bi-building fs-4"></i>
                </div>
                <span class="badge bg-light text-dark border"><i class="bi bi-clock me-1"></i> {{ formatDate(drive.deadline) }}</span>
              </div>
              
              <h5 class="fw-bold text-dark mb-1">{{ drive.job_title }}</h5>
              <h6 class="text-primary mb-3">{{ drive.company_name }}</h6>
              
              <div class="d-flex flex-wrap gap-2 mb-4">
                <span class="badge bg-secondary-subtle text-secondary fw-medium px-2 py-1"><i class="bi bi-mortarboard me-1"></i> {{ drive.eligibility_branch || 'Any Branch' }}</span>
                <span class="badge bg-secondary-subtle text-secondary fw-medium px-2 py-1"><i class="bi bi-star me-1"></i> {{ drive.eligibility_cgpa }}+ CGPA</span>
              </div>
              
              <button 
                @click="applyForDrive(drive.drive_id)" 
                class="btn w-100 fw-semibold rounded-pill"
                :class="drive.has_applied ? 'btn-secondary text-white border-0' : 'btn-outline-primary'"
                :disabled="applying === drive.drive_id || drive.has_applied">
                {{drive.has_applied ? 'Already Applied' : (applying === drive.drive_id ? 'Applying...' : 'Apply Now') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-5 bg-white rounded-4 shadow-sm">
        <i class="bi bi-search display-4 text-muted mb-3 opacity-50"></i>
        <h5 class="fw-bold text-dark">No drives found</h5>
        <p class="text-muted">Try adjusting your filters to see more results.</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const router = useRouter();
const drives = ref([]);
const loading = ref(true);
const applying = ref(null);

const filters = ref({
  branch: '',
  cgpa: ''
});

const fetchDrives = async () => {
  loading.value = true;
  try {
    const params = {};
    if (filters.value.branch) params.branch = filters.value.branch;
    if (filters.value.cgpa) params.cgpa = filters.value.cgpa;

    const res = await api.get('/student/drive', { params });
    drives.value = res.data;
  } 
  catch (error) {
    console.error("Failed to fetch drives:", error);
    if (error.response?.status === 401) handleLogout();
  } 
  finally {
    loading.value = false;
  }
};

const clearFilters = () => {
  filters.value = { branch: '', cgpa: '' };
  fetchDrives();
};

const applyForDrive = async (driveId) => {
  applying.value = driveId;
  try {
    const res = await api.post('/student/apply', { drive_id: driveId });
    alert(res.data.message || "Successfully applied!");
    const driveToUpdate = drives.value.find(d => d.drive_id === driveId);
    if (driveToUpdate) {
      driveToUpdate.has_applied = true; 
    }    
  } 
  catch (error) {
    console.error(error);
    alert(error.response?.data?.error || "Failed to apply.");
  }
  finally {
    applying.value = null;
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.dispatchEvent(new Event("auth-changed"));
  router.push('/'); 
};

onMounted(() => {
  fetchDrives();
});
</script>

<style scoped>
.font-sans { 
  font-family: 'Inter', 
  -apple-system, sans-serif; 
}

.sidebar { 
  width: 260px; 
  background-color: #111827; 
}

.tracking-wide { 
  letter-spacing: 0.5px; 
}

.nav-pills .nav-link { 
  border-radius: 8px; 
  padding: 12px 16px; 
  margin-bottom: 4px; 
  color: #9ca3af !important; 
  transition: all 0.2s ease; 
}

.nav-pills .nav-link:hover { 
  background-color: rgba(255, 255, 255, 0.05); 
  color: white !important; 
}

.nav-pills .nav-link.active { 
  background-color: #1f2937 !important; 
  color: white !important; 
  position: relative; 
}

.nav-pills .nav-link.active::before { 
  content: ''; 
  position: absolute; 
  left: -16px; top: 10%; 
  height: 80%; width: 4px; 
  background-color: #3b82f6; 
  border-radius: 0 4px 4px 0; 
}

.bg-blue-light { 
  background-color: #eff6ff; 
}

.bg-secondary-subtle { 
  background-color: #f3f4f6 !important; 
}

.drive-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
}

.transition-all { 
  transition: all 0.3s ease; 
}
</style>