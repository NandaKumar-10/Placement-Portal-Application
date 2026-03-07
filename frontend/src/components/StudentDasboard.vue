<template>
  <div class="container-fluid p-0 d-flex bg-light min-vh-100 font-sans">
    
    <div class="sidebar d-flex flex-column p-3 text-white">
      <div class="d-flex align-items-center mb-5 mt-2 px-2">
        <i class="bi bi-mortarboard-fill fs-3 me-2"></i>
        <h4 class="mb-0 fw-bold tracking-wide">Placement</h4>
      </div>
      
      <ul class="nav nav-pills flex-column mb-auto gap-2">
        <li class="nav-item">
          <router-link to="/student/dashboard" class="nav-link active d-flex align-items-center">
            <i class="bi bi-house-door me-3 fs-5"></i> My Profile
          </router-link>
        </li>
        <li>
          <router-link to="/student/drive" class="nav-link text-white d-flex align-items-center">
            <i class="bi bi-search me-3 fs-5"></i> Find Placement Drive
          </router-link>
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
        <h2 class="fw-bold mb-0 text-dark">Student Dashboard</h2>
        
        <div class="d-flex align-items-center gap-4">
          <!-- <button class="btn btn-outline-primary border-0 bg-white shadow-sm rounded-circle p-2 position-relative">
            <i class="bi bi-bell text-primary"></i>
          </button> -->
          
          <div class="d-flex align-items-center gap-3">
            <div class="text-end d-none d-md-block">
              <div class="fw-bold text-dark lh-1">{{ profile.name || 'Loading...' }}</div>
              <small class="text-muted" style="font-size: 0.8rem;">Student</small>
            </div>
            <!-- <div class="bg-secondary rounded-circle d-flex justify-content-center align-items-center text-white" style="width: 40px; height: 40px;">
              <i class="bi bi-person-fill fs-5"></i>
            </div> -->
          </div>
        </div>
      </div>

      <div class="card border-0 shadow-sm rounded-4 mb-4 p-2">
        <div class="card-body d-flex justify-content-between align-items-center flex-wrap gap-3">
          <div class="d-flex align-items-center gap-4">
            <!-- <div class="bg-light rounded-circle d-flex justify-content-center align-items-center text-secondary" style="width: 80px; height: 80px;">
              <i class="bi bi-person-fill" style="font-size: 3rem;"></i>
            </div> -->
            <div>
              <h4 class="fw-bold text-dark mb-1">{{ profile.name }}</h4>
              <p class="text-muted mb-2">
                {{ profile.branch || 'Branch Not Set' }} • <span class="fw-semibold">{{ profile.cgpa ? profile.cgpa.toFixed(2) : 'N/A' }} CGPA</span>
              </p>
              <div class="d-flex gap-2">
                <span class="badge bg-success-subtle text-success px-3 py-2 rounded-pill">Eligible</span>
              </div>
            </div>
          </div>
          
          <router-link to="/student/edit-profile" class="btn btn-outline-primary rounded-pill px-4 fw-semibold">
            Edit Profile
          </router-link>
        </div>
      </div>

      <div class="card border-0 shadow-sm rounded-4 p-4">
        <h5 class="fw-bold mb-4">Applied Drives</h5>

        <div v-if="loading" class="text-center py-4">
          <div class="spinner-border text-primary" role="status"></div>
        </div>

        <div class="table-responsive" v-else>
          <table class="table table-hover align-middle mb-0">
            <thead class="text-muted" style="border-bottom: 2px solid #f4f4f4;">
              <tr>
                <th class="fw-semibold pb-3 border-0">Company</th>
                <th class="fw-semibold pb-3 border-0">Role</th>
                <th class="fw-semibold pb-3 border-0">Applied Date</th>
                <th class="fw-semibold pb-3 border-0">Status</th>
                <th class="fw-semibold pb-3 border-0">Interview Details</th>
              </tr>
            </thead>
            <tbody v-if="applications.length > 0">
              <tr v-for="app in applications" :key="app.id">
                <td class="py-3 border-light fw-bold text-dark">{{ app.company_name }}</td>
                <td class="py-3 border-light text-secondary">{{ app.job_title }}</td>
                <td class="py-3 border-light text-secondary">{{ app.applied_date }}</td>
                <td class="py-3 border-light">
                  <span class="badge rounded-pill fw-medium px-3 py-2" 
                        :class="{
                          'bg-success-subtle text-success': app.status === 'Shortlisted' || app.status === 'Hired' || app.status === 'Applied',
                          'bg-danger-subtle text-danger': app.status === 'Rejected',
                          'bg-warning-subtle text-warning': app.status === 'Pending',
                          'bg-warning-subtle text-warning': app.status === 'Interview Scheduled' ,

                        }">
                    {{ app.status }}
                  </span>
                </td>
                
                <td class="py-3 border-light">
                  <div v-if="app.status === 'Interview Scheduled' && app.interview_date">
                    <div class="small fw-semibold text-dark mb-1">
                      <i class="bi bi-calendar-event text-primary"></i> {{ app.interview_date }}
                    </div>
                    <a v-if="app.interview_link" :href="app.interview_link" target="_blank" class="small text-decoration-none fw-medium">
                      <i class="bi bi-link-45deg"></i> Join Interview
                    </a>
                  </div>
                  <span v-else class="text-muted small">-</span>
                </td>

              </tr>
            </tbody>
            <tbody v-else>
              <tr>
                <td colspan="4" class="text-center py-5 text-muted">You haven't applied to any drives yet.</td>
              </tr>
            </tbody>
          </table>
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
const profile = ref({});
const applications = ref([]);
const loading = ref(true);

const fetchStudentData = async () => {
  loading.value = true;
  try {
    const res = await api.get('/student/dashboard');
    profile.value = res.data.profile;
    applications.value = res.data.applications;
  } 
  catch (err){
    if (err.response?.status === 401) 
      handleLogout();
  } 
  finally {
    loading.value = false;
  }
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.dispatchEvent(new Event("auth-changed"));
  router.push('/'); 
};

onMounted(() => {
  fetchStudentData();
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

.bg-success-subtle { 
  background-color: #dcfce7 !important; 
}

.bg-warning-subtle { 
  background-color: #fef3c7 !important; 
  color: #d97706 !important; 
}

.bg-danger-subtle { 
  background-color: #fee2e2 !important; 
  color: #b91c1c !important; 
}
</style>