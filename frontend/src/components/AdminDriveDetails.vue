<template>
  <div class="container-fluid p-0 d-flex bg-light min-vh-100 font-sans">
    
    <div class="sidebar d-flex flex-column p-3 text-white">
      <div class="d-flex align-items-center mb-5 mt-2 px-2">
        <i class="bi bi-mortarboard-fill fs-3 me-2"></i>
        <h4 class="mb-0 fw-bold tracking-wide">Placement</h4>
      </div>
      <ul class="nav nav-pills flex-column mb-auto gap-2">
        <li class="nav-item">
          <router-link to="/admin" class="nav-link text-white d-flex align-items-center">
            <i class="bi bi-arrow-left-short me-2 fs-4"></i> Back to Dashboard
          </router-link>
        </li>
      </ul>
    </div>

    <div class="main-content flex-grow-1 p-4 px-md-5">
      
      <div v-if="loading" class="text-center py-5 mt-5">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-2 text-muted">Loading drive details...</p>
      </div>

      <div v-else-if="drive">
        <div class="d-flex justify-content-between align-items-center mb-4 mt-2">
          <div>
            <h2 class="fw-bold mb-1 text-dark">{{ drive.job_title }}</h2>
            <h5 class="text-primary"><i class="bi bi-building me-2"></i>{{ drive.company_name }}</h5>
          </div>
          <span class="badge fs-6 px-4 py-2 rounded-pill" 
                :class="drive.status === 'Approved' ? 'bg-success-subtle text-success' : 'bg-warning-subtle text-warning'">
            {{ drive.status === 'Approved' ? 'Active' : drive.status }}
          </span>
        </div>

        <div class="row g-4 mb-5">
          <div class="col-md-4">
            <div class="card border-0 shadow-sm rounded-4 h-100 p-3">
              <div class="text-muted small fw-semibold mb-1">Application Deadline</div>
              <div class="fs-5 fw-bold text-dark"><i class="bi bi-calendar-event me-2 text-primary"></i>{{ formatDate(drive.deadline) }}</div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card border-0 shadow-sm rounded-4 h-100 p-3">
              <div class="text-muted small fw-semibold mb-1">Eligibility Criteria</div>
              <div class="fs-5 fw-bold text-dark"><i class="bi bi-star me-2 text-warning"></i>{{ drive.eligibility_cgpa }}+ CGPA</div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card border-0 shadow-sm rounded-4 h-100 p-3">
              <div class="text-muted small fw-semibold mb-1">Total Applicants</div>
              <div class="fs-5 fw-bold text-dark"><i class="bi bi-people me-2 text-success"></i>{{ applicants.length }} Students</div>
            </div>
          </div>
        </div>

        <div class="card border-0 shadow-sm rounded-4 p-4">
          <h5 class="fw-bold mb-4">Applicant List</h5>
          
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="text-muted" style="border-bottom: 2px solid #f4f4f4;">
                <tr>
                  <th class="fw-semibold pb-3 border-0">Student Name</th>
                  <th class="fw-semibold pb-3 border-0">Branch</th>
                  <th class="fw-semibold pb-3 border-0">CGPA</th>
                  <th class="fw-semibold pb-3 border-0">Status</th>
                  <th class="fw-semibold pb-3 border-0 text-end">Resume</th>
                </tr>
              </thead>
              <tbody v-if="applicants.length > 0">
                <tr v-for="app in applicants" :key="app.application_id">
                  <td class="py-3 border-light fw-bold text-dark">{{ app.student_name }}</td>
                  <td class="py-3 border-light text-secondary">{{ app.branch }}</td>
                  <td class="py-3 border-light fw-semibold">{{ app.cgpa }}</td>
                  <td class="py-3 border-light">
                    <span class="badge rounded-pill bg-light border text-dark">{{ app.status }}</span>
                  </td>
                  <td class="py-3 border-light text-end">
                    <a v-if="app.resume_url" :href="app.resume_url" target="_blank" class="btn btn-sm btn-outline-primary rounded-pill px-3">View</a>
                    <span v-else class="small text-muted">N/A</span>
                  </td>
                </tr>
              </tbody>
              <tbody v-else>
                <tr>
                  <td colspan="5" class="text-center py-5 text-muted">No students have applied yet.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../api';

const route = useRoute();
const router = useRouter();
const loading = ref(true);

const drive = ref(null);
const applicants = ref([]);

const fetchDriveDetails = async () => {
  const driveId = route.params.id; 
  
  try {
    const res = await api.get(`/admin/drive/${driveId}`);
    drive.value = res.data.drive_details;
    applicants.value = res.data.applicants;
  } 
  catch (error) {
    console.error(error);
    router.push('/admin');
  } 
  finally {
    loading.value = false;
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

onMounted(() => {
  fetchDriveDetails();
});
</script>

<style scoped>
.font-sans { 
  font-family: sans-serif; 
}

.sidebar { 
  width: 260px; 
  background-color: #111827; 
}

.tracking-wide { 
  letter-spacing: 0.5px; 
}

.bg-success-subtle { 
  background-color: #dcfce7 !important; 
}

.bg-warning-subtle { 
  background-color: #fef3c7 !important; 
  color: #d97706 !important; 
}

</style>