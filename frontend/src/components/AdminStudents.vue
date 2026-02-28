<template>
  <div class="container-fluid p-0 d-flex bg-light min-vh-100 font-sans">

    <div class="sidebar d-flex flex-column p-3 text-white">
      <div class="d-flex align-items-center mb-5 mt-2 px-2">
        <i class="bi bi-mortarboard-fill fs-3 me-2"></i>
        <h4 class="mb-0 fw-bold tracking-wide">Placement</h4>
      </div>
      
      <ul class="nav nav-pills flex-column mb-auto gap-2">
        <li>
          <router-link to="/admin" class="nav-link text-white d-flex align-items-center text-decoration-none">
            <i class="bi bi-graph-up me-3 fs-5"></i> Dashboard
          </router-link>
        </li>
        <li>
          <router-link to="/admin/companies" class="nav-link text-white d-flex align-items-center text-decoration-none">
            <i class="bi bi-building me-3 fs-5"></i> Companies
          </router-link>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link active d-flex align-items-center">
            <i class="bi bi-people me-3 fs-5"></i> Students
          </a>
        </li>
      </ul>

      <div class="mt-auto px-2 mb-2">
        <a href="#" @click.prevent="handleLogout" class="text-white text-decoration-none d-flex align-items-center opacity-75 hover-opacity-100">
          <i class="bi bi-box-arrow-right me-3 fs-5"></i> Logout
        </a>
      </div>
    </div>

    <div class="main-content flex-grow-1 p-4 px-md-5">
      
      <div class="d-flex justify-content-between align-items-center mb-5 mt-2">
        <h2 class="fw-bold mb-0 text-dark">Manage Students</h2>
        <div class="d-flex align-items-center gap-3">
          <div class="text-end d-none d-md-block">
            <div class="fw-bold text-dark lh-1">Admin User</div>
            <small class="text-muted" style="font-size: 0.8rem;">Administrator</small>
          </div>
          <div class="bg-secondary rounded-circle d-flex justify-content-center align-items-center text-white" style="width: 40px; height: 40px;">
            <i class="bi bi-person-fill fs-5"></i>
          </div>
        </div>
      </div>

      <div class="card border-0 shadow-sm rounded-4 p-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h5 class="fw-bold mb-0">Registered Students</h5>
          
          <div class="input-group" style="max-width: 300px;">
            <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
            <input type="text" v-model="searchQuery" class="form-control border-start-0 ps-0" placeholder="Search by name or email...">
          </div>
        </div>

        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="text-muted mt-2">Loading students...</p>
        </div>

        <div class="table-responsive" v-else>
          <table class="table table-hover align-middle mb-0">
            <thead class="text-muted" style="border-bottom: 2px solid #f4f4f4;">
              <tr>
                <th class="fw-semibold pb-3 border-0">Student Name</th>
                <th class="fw-semibold pb-3 border-0">Branch</th>
                <th class="fw-semibold pb-3 border-0">CGPA</th>
                <th class="fw-semibold pb-3 border-0">Resume</th>
                <th class="fw-semibold pb-3 border-0 text-end">Actions</th>
              </tr>
            </thead>
            <tbody v-if="students.length > 0">
              <tr v-for="student in filteredStudents" :key="student.student_id">
                
                <td class="py-3 border-light">
                  <div class="d-flex align-items-center">
                    <div class="bg-blue-light text-primary rounded-circle d-flex justify-content-center align-items-center me-3" style="width: 40px; height: 40px;">
                      <span class="fw-bold">{{ student.name.charAt(0).toUpperCase() }}</span>
                    </div>
                    <div>
                      <div class="fw-bold text-dark">{{ student.name }}</div>
                      <small class="text-muted">{{ student.email }}</small>
                    </div>
                  </div>
                </td>
                
                <td class="py-3 border-light text-secondary">
                  {{ student.branch }} <br>
                  <small class="text-muted">Year: {{ student.year }}</small>
                </td>
                
                <td class="py-3 border-light">
                  <span class="badge bg-light text-dark border px-2 py-1 fs-6">
                    {{ student.cgpa.toFixed(2) }}
                  </span>
                </td>
                
                <td class="py-3 border-light">
                  <a v-if="student.resume_url" :href="student.resume_url" target="_blank" class="btn btn-sm btn-outline-primary rounded-pill px-3">
                    <i class="bi bi-file-earmark-pdf me-1"></i> View
                  </a>
                  <span v-else class="text-muted small">Not uploaded</span>
                </td>
                
                <td class="py-3 border-light text-end">
                  <button @click="deleteStudent(student.student_id)" class="btn btn-sm btn-outline-danger rounded-3" title="Delete Student">
                    <i class="bi bi-trash3"></i>
                  </button>
                </td>
                
              </tr>
            </tbody>
            <tbody v-else>
              <tr>
                <td colspan="5" class="text-center py-5 text-muted">No students registered yet.</td>
              </tr>
            </tbody>
          </table>
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
const students = ref([]);
const loading = ref(true);
const searchQuery = ref('');

const filteredStudents = computed(() => {
  if (!searchQuery.value) return students.value;
  const query = searchQuery.value.toLowerCase();
  return students.value.filter(student => 
    student.name.toLowerCase().includes(query) || 
    student.email.toLowerCase().includes(query)
  );
});

const fetchStudents = async () => {
  loading.value = true;
  try {
    const response = await api.get('/admin/students');
    students.value = response.data;
  } catch (error) {
    console.error("Error fetching students:", error);
    if (error.response?.status === 401) handleLogout();
  } finally {
    loading.value = false;
  }
};

const deleteStudent = async (studentId) => {
  if (!confirm("Are you sure you want to delete this student? This will permanently remove their user account as well.")) return;
  
  try {
    await api.delete(`/admin/student/${studentId}`);
    students.value = students.value.filter(s => s.student_id !== studentId);
  } catch (error) {
    console.error("Error deleting student:", error);
    alert("Failed to delete student.");
  }
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.dispatchEvent(new Event("auth-changed"));
  router.push('/'); 
};

onMounted(() => {
  fetchStudents();
});
</script>

<style scoped>
.font-sans { font-family: 'Inter', -apple-system, sans-serif; }
.sidebar { width: 260px; background-color: #111827; }
.tracking-wide { letter-spacing: 0.5px; }

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
  content: ''; position: absolute; left: -16px; top: 10%; height: 80%; width: 4px;
  background-color: #3b82f6; border-radius: 0 4px 4px 0;
}

.bg-blue-light { background-color: #eff6ff; }
.table th { text-transform: capitalize; font-size: 0.9rem; }
.table td { font-size: 0.95rem; }
</style>