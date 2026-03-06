<template>
  <div class="container-fluid p-0 d-flex bg-light min-vh-100 font-sans relative">
    
    <div class="sidebar d-flex flex-column p-3 text-white">
      <div class="d-flex align-items-center mb-5 mt-2 px-2">
        <i class="bi bi-mortarboard-fill fs-3 me-2"></i>
        <h4 class="mb-0 fw-bold tracking-wide">Placement</h4>
      </div>
      <ul class="nav nav-pills flex-column mb-auto gap-2">
        <li class="nav-item">
          <router-link to="/company/dashboard" class="nav-link text-white d-flex align-items-center">
            <i class="bi bi-arrow-left-short me-2 fs-4"></i> Back to Dashboard
          </router-link>
        </li>
      </ul>
    </div>

    <div class="main-content flex-grow-1 p-4 px-md-5 overflow-auto">
      <div class="d-flex justify-content-between align-items-center mb-4 mt-2">
        <h2 class="fw-bold mb-0 text-dark">Drive Applicants</h2>
      </div>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
      </div>

      <div v-else class="card border-0 shadow-sm rounded-4 p-4">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="text-muted" style="border-bottom: 2px solid #f4f4f4;">
              <tr>
                <th class="fw-semibold pb-3 border-0">Student Name</th>
                <th class="fw-semibold pb-3 border-0">Branch</th>
                <th class="fw-semibold pb-3 border-0">CGPA</th>
                <th class="fw-semibold pb-3 border-0">Resume</th>
                <th class="fw-semibold pb-3 border-0">Current Status</th>
                <th class="fw-semibold pb-3 border-0 text-end">Action</th>
              </tr>
            </thead>
            <tbody v-if="applicants.length > 0">
              <tr v-for="app in applicants" :key="app.application_id">
                <td class="py-3 border-light">
                  <div class="fw-bold text-dark">{{ app.student_name }}</div>
                  <div class="small text-muted">{{ app.student_email }}</div>
                </td>
                <td class="py-3 border-light text-secondary">{{ app.branch }}</td>
                <td class="py-3 border-light fw-semibold">{{ app.cgpa }}</td>
                <td class="py-3 border-light">
                  <a v-if="app.resume_url" :href="app.resume_url" target="_blank" class="btn btn-sm btn-light text-primary">
                    <i class="bi bi-file-earmark-pdf"></i> View
                  </a>
                  <span v-else class="text-muted small">Not provided</span>
                </td>
                <td class="py-3 border-light">
                  <span class="badge rounded-pill fw-medium px-3 py-2" :class="statusClass(app.status)">
                    {{ app.status }}
                  </span>
                  <div v-if="app.interview_date" class="small text-muted mt-1">
                    <i class="bi bi-calendar-event"></i> {{ app.interview_date }}
                  </div>
                </td>
                <td class="py-3 border-light text-end">
                  
                  <div v-if="app.status === 'Pending'" class="btn-group btn-group-sm">
                    <button @click="updateStatus(app.application_id, 'Shortlisted')" class="btn btn-outline-primary fw-medium">Shortlist</button>
                    <button @click="updateStatus(app.application_id, 'Rejected')" class="btn btn-outline-danger fw-medium">Reject</button>
                  </div>

                  <div v-else-if="app.status === 'Shortlisted'">
                    <button @click="openScheduleModal(app)" class="btn btn-sm btn-info text-white fw-medium">
                      Schedule Interview
                    </button>
                  </div>

                  <div v-else-if="app.status === 'Interview Scheduled'" class="btn-group btn-group-sm">
                    <button @click="updateStatus(app.application_id, 'Hired')" class="btn btn-success fw-medium">Hire</button>
                    <button @click="updateStatus(app.application_id, 'Rejected')" class="btn btn-outline-danger fw-medium">Reject</button>
                  </div>

                  <div v-else class="text-muted small fw-medium">
                    Process Completed
                  </div>

                </td>
              </tr>
            </tbody>
            <tbody v-else>
              <tr>
                <td colspan="6" class="text-center py-5 text-muted">No students have applied to this drive yet.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay d-flex justify-content-center align-items-center">
      <div class="bg-white rounded-4 p-4 shadow-lg" style="width: 400px;">
        <h5 class="fw-bold mb-3">Schedule Interview</h5>
        <p class="small text-muted mb-4">Scheduling for: <strong class="text-dark">{{ selectedApp.student_name }}</strong></p>
        
        <form @submit.prevent="submitInterview">
          <div class="mb-3">
            <label class="form-label small fw-semibold">Date & Time</label>
            <input type="datetime-local" class="form-control" v-model="interviewForm.date" required>
          </div>
          <div class="mb-4">
            <label class="form-label small fw-semibold">Interview Link / Location (Optional)</label>
            <input type="text" class="form-control" placeholder="e.g. Google Meet link or Room 204" v-model="interviewForm.link">
          </div>
          <div class="d-flex justify-content-end gap-2">
            <button type="button" class="btn btn-light fw-medium" @click="closeModal">Cancel</button>
            <button type="submit" class="btn btn-primary fw-medium">Schedule</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../api';

const route = useRoute();
const applicants = ref([]);
const loading = ref(true);

const showModal = ref(false);
const selectedApp = ref(null);
const interviewForm = ref({ date: '', link: '' });

const driveId = route.params.drive_id;

const fetchApplicants = async () => {
  loading.value = true;
  try {
    const res = await api.get(`/company/drive/${driveId}/applications`);
    applicants.value = res.data;
  } 
  catch (error) {
    console.error("Failed to fetch applicants:", error);
    alert("Could not load applicants.");
  } 
  finally {
    loading.value = false;
  }
};

const updateStatus = async (appId, newStatus) => {
  try {
    await api.put(`/company/application/${appId}`, { status: newStatus });
    const student = applicants.value.find(a => a.application_id === appId);
    if (student) student.status = newStatus;
  } 
  catch (error) {
    console.error("Error updating status:", error);
    alert("Failed to update student status.");
  }
};

const openScheduleModal = (app) => {
  selectedApp.value = app;
  interviewForm.value = { date: '', link: '' };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  selectedApp.value = null;
};

const submitInterview = async () => {
  if (!selectedApp.value) return;

  try {
    const formattedDate = new Date(interviewForm.value.date).toLocaleString('en-US', {
      dateStyle: 'medium', timeStyle: 'short'
    });

    await api.put(`/company/application/${selectedApp.value.application_id}`, { 
      status: 'Interview Scheduled',
      interview_date: formattedDate,
      interview_link: interviewForm.value.link
    });

    const student = applicants.value.find(a => a.application_id === selectedApp.value.application_id);
    if (student) {
      student.status = 'Interview Scheduled';
      student.interview_date = formattedDate;
      student.interview_link = interviewForm.value.link;
    }
    closeModal();
    
  } 
  catch (error) {
    console.error("Error scheduling interview:", error);
    alert("Failed to schedule interview.");
  }
};

const statusClass = (status) => {
  if (status === 'Hired') return 'bg-success-subtle text-success';
  if (status === 'Shortlisted' || status === 'Interview Scheduled') return 'bg-info-subtle text-info';
  if (status === 'Rejected') return 'bg-danger-subtle text-danger';
  return 'bg-warning-subtle text-warning';
};

onMounted(() => {
  fetchApplicants();
});
</script>

<style scoped>
.font-sans { 
  font-family: 'Inter', sans-serif; 
}

.sidebar { 
  width: 260px; 
  background-color: #111827; 
  z-index: 10; 
}

.tracking-wide { 
  letter-spacing: 0.5px; 
}

.nav-pills .nav-link { 
  border-radius: 8px; 
  padding: 12px 16px; 
  margin-bottom: 4px; 
  transition: all 0.2s ease; 
}
.nav-pills .nav-link:hover { 
  background-color: rgba(255, 255, 255, 0.05); 
  color: white !important; 
}

.bg-success-subtle { 
  background-color: #dcfce7 !important; 
  color: #15803d !important; 
}

.bg-danger-subtle { 
  background-color: #fee2e2 !important; 
  color: #b91c1c !important; 
}

.bg-warning-subtle { 
  background-color: #fef3c7 !important; 
  color: #d97706 !important; 
}

.bg-info-subtle { 
  background-color: #e0f2fe !important; 
  color: #0369a1 !important; 
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1050;
  backdrop-filter: blur(2px);
}
</style>