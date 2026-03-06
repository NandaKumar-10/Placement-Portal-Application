<template>
  <div class="container-fluid p-0 d-flex bg-light min-vh-100 font-sans">
    
    <div class="sidebar d-flex flex-column p-3 text-white">
      <div class="d-flex align-items-center mb-5 mt-2 px-2">
        <i class="bi bi-mortarboard-fill fs-3 me-2"></i>
        <h4 class="mb-0 fw-bold tracking-wide">Placement</h4>
      </div>
      
      <ul class="nav nav-pills flex-column mb-auto gap-2">
        <li class="nav-item">
          <router-link to="/company" class="nav-link active d-flex align-items-center">
            <i class="bi bi-speedometer2 me-3 fs-5"></i> Dashboard
          </router-link>
        </li>
        <!-- <li>
          <a href="/company/applicant" class="nav-link text-white d-flex align-items-center opacity-75">
            <i class="bi bi-people me-3 fs-5"></i> Applicants
          </a>
        </li> -->
      </ul>

      <div class="mt-auto px-2 mb-2">
        <a href="#" @click.prevent="handleLogout" class="text-white text-decoration-none d-flex align-items-center opacity-75 hover-opacity-100">
          <i class="bi bi-box-arrow-right me-3 fs-5"></i> Logout
        </a>
      </div>
    </div>

    <div class="main-content flex-grow-1 p-4 px-md-5 overflow-auto">
      
      <div class="d-flex justify-content-between align-items-center mb-4 mt-2">
        <h2 class="fw-bold mb-0 text-dark">Company Dashboard</h2>
        
        <div class="d-flex align-items-center gap-3">
          <div class="text-end d-none d-md-block">
            <div class="fw-bold text-dark lh-1">{{ companyDetails.name || 'Loading...' }}</div>
            <small class="text-muted" style="font-size: 0.8rem;">Employer Panel</small>
          </div>
          <div class="bg-primary bg-opacity-10 text-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
            <i class="bi bi-building fs-5"></i>
          </div>
        </div>
      </div>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
      </div>

      <div v-else>
        <div v-if="companyDetails.approval_status === 'Pending'" class="alert alert-warning border-0 shadow-sm rounded-4 d-flex align-items-center mb-4 p-3">
          <i class="bi bi-exclamation-triangle-fill fs-3 me-3"></i>
          <div>
            <h6 class="fw-bold mb-1">Account Pending Approval</h6>
            <p class="mb-0 small">Your account is currently under review by the administrator. You cannot create placement drives until you are approved.</p>
          </div>
        </div>

        <div v-if="companyDetails.approval_status === 'Approved'" class="alert alert-success border-0 shadow-sm rounded-4 d-flex align-items-center mb-4 p-3 py-2">
          <i class="bi bi-check-circle-fill fs-4 me-3"></i>
          <span class="fw-semibold">Account Approved & Active</span>
        </div>

        <div class="row g-4 mb-4">
          <div class="col-md-6">
            <div class="card border-0 shadow-sm rounded-4 p-3 h-100">
              <div class="card-body d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="text-muted fw-semibold mb-2">Total Drives Created</h6>
                  <h1 class="fw-bold mb-0 text-dark">{{ drives.length }}</h1>
                </div>
                <div class="bg-blue-light text-primary rounded-3 d-flex justify-content-center align-items-center" style="width: 50px; height: 50px;">
                  <i class="bi bi-briefcase fs-4"></i>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-6">
            <div class="card border-0 shadow-sm rounded-4 p-3 h-100">
              <div class="card-body d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="text-muted fw-semibold mb-2">Total Applicants</h6>
                  <h1 class="fw-bold mb-0 text-dark">{{ totalApplicants }}</h1>
                </div>
                <div class="bg-success-subtle text-success rounded-3 d-flex justify-content-center align-items-center" style="width: 50px; height: 50px;">
                  <i class="bi bi-people-fill fs-4"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card border-0 shadow-sm rounded-4 p-4 mb-5">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h5 class="fw-bold mb-0">Your Placement Drives</h5>
            <button 
              @click="showCreateForm = !showCreateForm" 
              class="btn btn-primary fw-semibold rounded-pill px-4"
              :disabled="companyDetails.approval_status !== 'Approved'">
              <i class="bi" :class="showCreateForm ? 'bi-x-lg' : 'bi-plus-lg'"></i> 
              {{ showCreateForm ? 'Cancel' : 'New Drive' }}
            </button>
          </div>

          <div v-if="showCreateForm && companyDetails.approval_status === 'Approved'" class="bg-light p-4 rounded-4 mb-4 border">
            <h6 class="fw-bold text-primary mb-3">Post a New Role</h6>
            <form @submit.prevent="submitNewDrive" class="row g-3">
              <div class="col-md-4">
                <label class="form-label small fw-semibold">Job Title</label>
                <input type="text" class="form-control" v-model="newDrive.job_title" placeholder="e.g. Software Engineer" required>
              </div>
              <div class="col-md-4">
                <label class="form-label small fw-semibold">Branch</label>
                <input type="text" step="0.1" class="form-control" v-model="newDrive.eligibility_branch" placeholder="e.g. CSE, ECE..." required>
              </div>
              <div class="col-md-4">
                <label class="form-label small fw-semibold">Minimum CGPA</label>
                <input type="number" step="0.1" class="form-control" v-model="newDrive.eligibility_cgpa" placeholder="e.g. 7.5" required>
              </div>
              <div class="col-md-4">
                <label class="form-label small fw-semibold">Eligible Year</label>
                <input type="number" class="form-control" v-model="newDrive.eligiblity_year" required>
              </div>
              <div class="col-md-4">
                <label class="form-label small fw-semibold">Application Deadline</label>
                <input type="date" class="form-control" v-model="newDrive.deadline" required>
              </div>
              <div class="col-12 mt-3 text-end">
                <button type="submit" class="btn btn-success fw-semibold px-4" :disabled="submitting">
                  {{ submitting ? 'Posting...' : 'Post Drive' }}
                </button>
              </div>
            </form>
          </div>

          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="text-muted" style="border-bottom: 2px solid #f4f4f4;">
                <tr>
                  <th class="fw-semibold pb-3 border-0">Job Title</th>
                  <th class="fw-semibold pb-3 border-0">Deadline</th>
                  <th class="fw-semibold pb-3 border-0">Status</th>
                  <th class="fw-semibold pb-3 border-0 text-center">Applicants</th>
                  <th class="fw-semibold pb-3 border-0 text-end">Action</th>
                </tr>
              </thead>
              <tbody v-if="drives.length > 0">
                <tr v-for="drive in drives" :key="drive.drive_id">
                  <td class="py-3 border-light fw-bold text-dark">{{ drive.job_title }}</td>
                  <td class="py-3 border-light text-secondary">{{ formatDate(drive.deadline) }}</td>
                  <td class="py-3 border-light">
                    <span class="badge rounded-pill fw-medium" 
                          :class="drive.status === 'Approved' ? 'bg-success-subtle text-success' : 'bg-warning-subtle text-warning'">
                      {{ drive.status }}
                    </span>
                  </td>
                  <td class="py-3 border-light text-center fw-bold text-primary">{{ drive.applicants }}</td>
                  <td class="py-3 border-light text-end">
                    <button @click="router.push(`/company/drive/${drive.drive_id}/applicants`)"
                    class="btn btn-sm btn-outline-primary rounded-pill px-3 fw-semibold">View Applications</button>
                  </td>
                </tr>
              </tbody>
              <tbody v-else>
                <tr>
                  <td colspan="5" class="text-center py-5 text-muted">No placement drives created yet.</td>
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
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const router = useRouter();
const loading = ref(true);
const submitting = ref(false);
const showCreateForm = ref(false);

const companyDetails = ref({});
const drives = ref([]);

// Form model
const newDrive = ref({
  job_title: '',
  eligibility_branch: '',
  eligibility_cgpa: '',
  eligibility_year: '',
  deadline: ''
});

const totalApplicants = computed(() => {
  return drives.value.reduce((sum, drive) => sum + drive.applicants, 0);
});

const fetchDashboard = async () => {
  loading.value = true;
  try {
    const res = await api.get('/company/dashboard');
    companyDetails.value = res.data.company_details;
    drives.value = res.data.drives;
  } catch (error) {
    console.error(error);
    if (error.response?.status === 401) handleLogout();
  } finally {
    loading.value = false;
  }
};

const submitNewDrive = async () => {
  submitting.value = true;
  try {
    await api.post('/company/drive', newDrive.value);
    
    alert("Drive posted successfully! Waiting for admin approval.");
    
    newDrive.value = { job_title: '', eligibility_cgpa: '', deadline: '' };
    showCreateForm.value = false;
    
    await fetchDashboard();
  } catch (error) {
    console.error(error);
    alert(error.response?.data?.error || "Failed to create drive.");
  } finally {
    submitting.value = false;
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.dispatchEvent(new Event("auth-changed"));
  router.push('/'); 
};

onMounted(() => {
  fetchDashboard();
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

.bg-success-subtle { 
  background-color: #dcfce7 !important; 
}

.bg-warning-subtle { 
  background-color: #fef3c7 !important; 
  color: #d97706 !important; 
  }

</style>