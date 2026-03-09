<template>
  <div class="container-fluid p-0 d-flex bg-light min-vh-100 font-sans">
    
    <div class="sidebar d-flex flex-column p-3 text-white">
      <div class="d-flex align-items-center mb-5 mt-2 px-2">
        <i class="bi bi-mortarboard-fill fs-3 me-2"></i>
        <h4 class="mb-0 fw-bold tracking-wide">Placement</h4>
      </div>
      <ul class="nav nav-pills flex-column mb-auto gap-2">
        <li class="nav-item">
          <router-link to="/student/dashboard" class="nav-link text-white d-flex align-items-center">
            <i class="bi bi-arrow-left-short me-2 fs-4"></i>Dashboard
          </router-link>
        </li>
      </ul>
    </div>

    <div class="main-content flex-grow-1 p-4 px-md-5">
      <h2 class="fw-bold mb-4 mt-2 text-dark">Edit Profile</h2>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
      </div>

      <div v-else class="card border-0 shadow-sm rounded-4 p-4" style="max-width: 800px;">
        <form @submit.prevent="saveProfile">
          
          <h5 class="fw-bold text-primary mb-3">Personal Information</h5>
          <div class="mb-4">
            <label class="form-label fw-semibold text-muted small">Full Name</label>
            <input type="text" class="form-control bg-light" v-model="formData.name" required>
          </div>

          <h5 class="fw-bold text-primary mb-3">Academic Information</h5>
          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <label class="form-label fw-semibold text-muted small">Branch</label>
              <input type="text" class="form-control bg-light" v-model="formData.branch" placeholder="e.g. Computer Science" required>
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold text-muted small">Graduation Year</label>
              <input type="number" class="form-control bg-light" v-model="formData.year" required>
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold text-muted small">Current CGPA</label>
              <input type="number" step="0.01" class="form-control bg-light" v-model="formData.cgpa" required>
            </div>
          </div>

          <hr class="text-muted opacity-25 mb-4">

          <h5 class="fw-bold text-primary mb-3">Documents</h5>
          <div class="mb-4">
            <label class="form-label fw-semibold text-muted small">Resume URL (Google Drive / Dropbox)</label>
            <input type="url" class="form-control bg-light" v-model="formData.resume_url" placeholder="https://...">
            <div class="form-text small text-warning"><i class="bi bi-info-circle me-1"></i>Ensure link permissions are set to 'Anyone with the link can view'.</div>
          </div>

          <div v-if="errorMessage" class="alert alert-danger py-2">{{ errorMessage }}</div>
          <div v-if="successMessage" class="alert alert-success py-2">{{ successMessage }}</div>

          <div class="d-flex justify-content-end gap-3 mt-4">
            <router-link to="/student" class="btn btn-light px-4 fw-semibold">Cancel</router-link>
            <button type="submit" class="btn btn-primary px-4 fw-semibold shadow-sm" :disabled="saving">
              {{ saving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const router = useRouter();
const loading = ref(true);
const saving = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const formData = ref({
  name: '',
  branch: '',
  year: '',
  cgpa: '',
  resume_url: ''
});

const fetchProfileData = async () => {
  try {
    const res = await api.get('/student/edit-profile');
    formData.value = res.data;

  } 
  catch (error) {
    console.error("Failed to load profile:", error);
    errorMessage.value = "Could not load profile data.";
  }

  finally {
    loading.value = false;
  }
};

const saveProfile = async () => {
  saving.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    await api.put('/student/edit-profile', formData.value);
    successMessage.value = "Profile updated successfully!";
    setTimeout(() => {
      router.push('/student/dashboard');
    }, 1000);
  } catch (error) {
    errorMessage.value = "Failed to update profile. Please try again.";
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  fetchProfileData();
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

.form-control:focus { 
  box-shadow: none; 
  border-color: #3b82f6; 
}
</style>