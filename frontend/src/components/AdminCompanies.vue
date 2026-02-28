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
        <li class="nav-item">
          <a href="/admin/companies" class="nav-link active d-flex align-items-center">
            <i class="bi bi-building me-3 fs-5"></i> Companies
          </a>
        </li>
        <li>
          <a href="/admin/students" class="nav-link text-white d-flex align-items-center">
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
        <h2 class="fw-bold mb-0 text-dark">Manage Companies</h2>
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
          <h5 class="fw-bold mb-0">Registered Companies</h5>
          
          <div class="input-group" style="max-width: 300px;">
            <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
            <input type="text" class="form-control border-start-0 ps-0" placeholder="Search companies...">
          </div>
        </div>

        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="text-muted mt-2">Loading companies...</p>
        </div>

        <div class="table-responsive" v-else>
          <table class="table table-hover align-middle mb-0">
            <thead class="text-muted" style="border-bottom: 2px solid #f4f4f4;">
              <tr>
                <th class="fw-semibold pb-3 border-0">Company Name</th>
                <th class="fw-semibold pb-3 border-0">HR Contact</th>
                <th class="fw-semibold pb-3 border-0">Website</th>
                <th class="fw-semibold pb-3 border-0">Status</th>
                <th class="fw-semibold pb-3 border-0 text-end">Actions</th>
              </tr>
            </thead>
            <tbody v-if="companies.length > 0">
              <tr v-for="company in companies" :key="company.company_id">
                <td class="py-3 border-light fw-bold text-dark">
                  <div class="d-flex align-items-center">
                    <div class="bg-blue-light text-primary rounded d-flex justify-content-center align-items-center me-3" style="width: 40px; height: 40px;">
                      <i class="bi bi-building"></i>
                    </div>
                    {{ company.company_name }}
                  </div>
                </td>
                <td class="py-3 border-light text-secondary">{{ company.hr_contact }}</td>
                <td class="py-3 border-light">
                  <a :href="company.website" target="_blank" class="text-decoration-none text-primary">
                    {{ company.website }} <i class="bi bi-box-arrow-up-right small"></i>
                  </a>
                </td>
                <td class="py-3 border-light">
                  <span class="badge rounded-pill fw-medium" 
                        :class="company.approval_status === 'Approved' ? 'bg-success-subtle text-success' : 'bg-warning-subtle text-warning'">
                    {{ company.approval_status }}
                  </span>
                </td>
                <td class="py-3 border-light text-end">
                  
                  <button v-if="company.approval_status !== 'Approved'" 
                          @click="updateStatus(company.company_id, true)" 
                          class="btn btn-sm btn-success me-2 rounded-3" title="Approve">
                    <i class="bi bi-check-lg"></i>
                  </button>
                  
                  <button v-if="company.approval_status === 'Approved'" 
                          @click="updateStatus(company.company_id, false)" 
                          class="btn btn-sm btn-warning me-2 rounded-3 text-white" title="Revoke Approval">
                    <i class="bi bi-x-lg"></i>
                  </button>

                  <button @click="deleteCompany(company.company_id)" class="btn btn-sm btn-outline-danger rounded-3" title="Delete">
                    <i class="bi bi-trash3"></i>
                  </button>
                </td>
              </tr>
            </tbody>
            <tbody v-else>
              <tr>
                <td colspan="5" class="text-center py-5 text-muted">No companies registered yet.</td>
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
const companies = ref([]);
const loading = ref(true);

// 1. Fetch all companies
const fetchCompanies = async () => {
  loading.value = true;
  try {
    const response = await api.get('/admin/companies');
    companies.value = response.data;
  } catch (error) {
    console.error("Error fetching companies:", error);
    if (error.response?.status === 401) handleLogout();
  } finally {
    loading.value = false;
  }
};

// 2. Approve or Reject a company
const updateStatus = async (companyId, newStatus) => {
  try {
    await api.put('/admin/company-reg', {
      company_id: companyId,
      approval_status: newStatus // Backend expects boolean or matching string based on your model
    });
    // Refresh the list to show new status
    await fetchCompanies();
  } catch (error) {
    console.error("Error updating status:", error);
    alert("Failed to update status.");
  }
};

// 3. Delete a company
const deleteCompany = async (companyId) => {
  if (!confirm("Are you sure you want to delete this company? This action cannot be undone.")) return;
  
  try {
    await api.delete(`/admin/company/${companyId}`);
    // Remove it from the local array so the UI updates instantly without a full reload
    companies.value = companies.value.filter(c => c.company_id !== companyId);
  } catch (error) {
    console.error("Error deleting company:", error);
    alert("Failed to delete company.");
  }
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.dispatchEvent(new Event("auth-changed"));
  router.push('/'); 
};

onMounted(() => {
  fetchCompanies();
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

    .bg-success-subtle { background-color: #dcfce7 !important; }
    .bg-warning-subtle { background-color: #fef3c7 !important; color: #d97706 !important; }
</style>