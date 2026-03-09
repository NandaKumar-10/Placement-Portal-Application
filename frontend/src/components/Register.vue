<template>
  <div class="container-fluid min-vh-100 d-flex p-0 font-sans">
    <div class="row w-100 m-0">
      
      <div class="col-md-6 d-none d-md-flex flex-column justify-content-center align-items-center bg-primary text-white text-center position-fixed h-100" style="left: 0;">
        <i class="bi bi-mortarboard-fill display-1 mb-3"></i>
        <h1 class="fw-bold">University Placement</h1>
        <p class="fs-5 text-white-50">Start your career journey with us today.</p>
      </div>

      <div class="col-md-6 offset-md-6 d-flex justify-content-center align-items-center bg-white py-5">
        <div class="login-box w-100 px-4" style="max-width: 500px;">
          
          <h3 class="fw-bold mb-1">Create an Account</h3>
          <p class="text-muted mb-4">Please fill in the details to register.</p>

          <div class="d-flex bg-light p-1 rounded-pill mb-4 border">
            <button 
              class="btn flex-fill rounded-pill fw-semibold" 
              :class="role === 'Student' ? 'btn-primary' : 'btn-light text-muted border-0'"
              @click="role = 'Student'" type="button">
              <i class="bi bi-person me-2"></i>Student
            </button>
            <button 
              class="btn flex-fill rounded-pill fw-semibold" 
              :class="role === 'Company' ? 'btn-primary' : 'btn-light text-muted border-0'"
              @click="role = 'Company'" type="button">
              <i class="bi bi-building me-2"></i>Company
            </button>
          </div>

          <form @submit.prevent="handleRegister">
            
            <div class="mb-3">
              <label class="form-label fw-semibold">{{ role === 'Company' ? 'Company Name' : 'Full Name' }}</label>
              <input type="text" class="form-control" v-model="name" required>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Email Address</label>
              <input type="email" class="form-control" v-model="email" required>
            </div>

            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label fw-semibold">Password</label>
                <input type="password" class="form-control" v-model="password" required>
              </div>
              <div class="col-md-6">
                <label class="form-label fw-semibold">Confirm Password</label>
                <input type="password" class="form-control" v-model="confirmPassword" required>
              </div>
            </div>

            <div v-if="role === 'Student'" class="row mb-4 bg-light p-3 rounded-3 border mx-0">
              <h6 class="fw-bold mb-3 px-0 text-primary">Academic Details</h6>
              <div class="col-md-6 px-1 mb-2">
                <label class="form-label small fw-semibold">Branch</label>
                <input type="text" class="form-control form-control-sm" v-model="studentData.branch" placeholder="e.g. Computer Science" required>
              </div>
              <div class="col-md-6 px-1 mb-2">
                <label class="form-label small fw-semibold">Graduation Year</label>
                <input type="number" class="form-control form-control-sm" v-model="studentData.year" placeholder="2025" required>
              </div>
              <div class="col-md-6 px-1">
                <label class="form-label small fw-semibold">CGPA</label>
                <input type="number" step="0.01" class="form-control form-control-sm" v-model="studentData.cgpa" placeholder="e.g. 8.5" required>
              </div>
              <div class="col-md-6 px-1">
                <label class="form-label small fw-semibold">Resume URL (Google Drive / Dropbox)</label>
                <input type="url" class="form-control form-control-sm" v-model="studentData.resume" placeholder="https://..." required>
              </div>
            </div>

            <div v-if="role === 'Company'" class="row mb-4 bg-light p-3 rounded-3 border mx-0">
              <h6 class="fw-bold mb-3 px-0 text-primary">Company Details</h6>
              <div class="col-md-6 px-1 mb-2">
                <label class="form-label small fw-semibold">HR Contact</label>
                <input type="text" class="form-control form-control-sm" v-model="companyData.hrContact" placeholder="Name or Phone" required>
              </div>
              <div class="col-md-6 px-1 mb-2">
                <label class="form-label small fw-semibold">Website</label>
                <input type="text" class="form-control form-control-sm" v-model="companyData.website" placeholder="https://..." required>
              </div>
            </div>

            <div v-if="errorMessage" class="alert alert-danger py-2 text-center small" role="alert">
              {{ errorMessage }}
            </div>
            <div v-if="successMessage" class="alert alert-success py-2 text-center small" role="alert">
              {{ successMessage }}
            </div>

            <button type="submit" :disabled="loading" class="btn btn-primary w-100 py-2 fw-bold mt-2">
              {{ loading ? 'Creating Account...' : 'Sign Up' }}
            </button>

            <div class="text-center mt-3">
              <span class="text-muted small">Already have an account? </span>
              <router-link to="/" class="text-primary text-decoration-none fw-bold small">Sign In</router-link>
            </div>
          </form>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const router = useRouter();

const role = ref('Student');
const name = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');

const studentData = ref({ branch: '', year: '', cgpa: '',resume: '' });
const companyData = ref({ hrContact: '', website: '' });

const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const handleRegister = async () => {
  errorMessage.value = '';
  successMessage.value = '';

  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Passwords do not match!";
    return;
  }

  loading.value = true;

  try {
    const payload = {
      name: name.value,
      email: email.value,
      password: password.value,
      role: role.value,
    };

    if (role.value === 'Student') {
      payload.branch = studentData.value.branch;
      payload.year = studentData.value.year;
      payload.cgpa = studentData.value.cgpa;
      payload.resume = studentData.value.resume;
    } else {
      payload.hrContact = companyData.value.hrContact;
      payload.website = companyData.value.website;
    }

    const response = await api.post('/register', payload);

    successMessage.value = "Registration successful! Redirecting to login...";
    
    setTimeout(() => {
      router.push('/');
    }, 1500);

  } 
  catch (error) {
    console.error(error);
    if (error.response && error.response.data && error.response.data.message) {
      errorMessage.value = error.response.data.message;
    } else {
      errorMessage.value = "Registration failed. Please try again.";
    }
  } 
  finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.font-sans { 
  font-family: sans-serif; 
}

.bg-primary { 
  background-color: #2563EB !important; 
}

.text-primary { 
  color: #2563EB !important; 
}

.btn-primary { 
  background-color: #2563EB; 
  border-color: #2563EB; 
}

.btn-primary:hover { 
  background-color: #1d4ed8; 
}
</style>