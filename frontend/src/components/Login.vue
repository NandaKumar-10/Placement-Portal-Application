<template>
  <div class="container-fluid min-vh-100 d-flex p-0">
    <div class="row w-100 m-0">
      <div class="col-md-6 d-none d-md-flex flex-column justify-content-center align-items-center bg-primary text-white text-center">
        <i class="bi bi-mortarboard-fill display-1 mb-3"></i>
        <h1 class="fw-bold">Placement Portal</h1>
        <p class="fs-5 text-white-50">Manage your career journey efficiently.</p>
      </div>

      <div class="col-md-6 d-flex justify-content-center align-items-center bg-white">
        <div class="login-box w-75" style="max-width: 400px;">
          
          <h3 class="fw-bold mb-1">Welcome</h3>
          <p class="text-muted mb-4">Please enter your details to sign in.</p>

          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label class="form-label fw-semibold">Email Address</label>
              <input type="email" class="form-control" placeholder="username@university.edu.in" v-model="email" required>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Password</label>
              <input type="password" class="form-control" placeholder="Enter your password" v-model="password" required>
            </div>

            <div class="d-grid gap-3">
              <button type="submit" class="btn btn-primary w-100 py-2 fw-bold">Sign In</button>
              <a href="/register" class="btn btn-primary w-100 py-2 fw-bold">Register</a>
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
import api from "../api"; 

const email = ref("");
const password = ref("");
const loading = ref(false);
const router = useRouter();

const handleLogin = async () => {
  if (!email.value || !password.value) return alert("Missing fields");

  loading.value = true;
  try {
    const res = await api.post("/login", {
      email: email.value, 
      password: password.value
    });

    localStorage.setItem("token", res.data.token);
    localStorage.setItem("role", res.data.role); 
    window.dispatchEvent(new Event("auth-changed"));
    
    if (res.data.role === "admin") {
      router.push("/admin");
    }
    else if (res.data.role === 'Company'){
      router.push("/company/dashboard");
    }
    else {
      router.push("/student/dashboard");
    }

  } 
  catch (error) {
    alert("Login failed. Check credentials.");
  } 
  finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.bg-primary {
  background-color: #2563EB !important;
}

.btn-primary {
  background-color: #2563EB;
  border-color: #2563EB;
}

.btn-primary:hover {
  background-color: #1d4ed8;
}
</style>