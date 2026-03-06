<template>
  <div class="container-fluid p-0 d-flex bg-light min-vh-100 font-sans">
    <div class="sidebar d-flex flex-column p-3 text-white">
      <div class="d-flex align-items-center mb-5 mt-2 px-2">
        <i class="bi bi-mortarboard-fill fs-3 me-2"></i>
        <h4 class="mb-0 fw-bold tracking-wide">Placement</h4>
      </div>
      
      <ul class="nav nav-pills flex-column mb-auto gap-2">
        <li class="nav-item">
          <a href="/admin" class="nav-link active d-flex align-items-center">
            <i class="bi bi-graph-up me-3 fs-5"></i> Dashboard
          </a>
        </li>
        <li>
          <a href="/admin/companies" class="nav-link text-white d-flex align-items-center">
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
        <h2 class="fw-bold mb-0 text-dark">Admin Dashboard</h2>
        
        <div class="d-flex align-items-center gap-4">
          <button class="btn btn-outline-primary border-0 bg-white shadow-sm rounded-circle p-2 position-relative">
            <i class="bi bi-bell text-primary"></i>
            <span class="position-absolute top-0 start-100 translate-middle p-1 bg-danger border border-light rounded-circle"></span>
          </button>
          
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
      </div>

      <div class="row g-4 mb-5" v-if="stats.overview">
        <div class="col-md-4">
          <div class="card border-0 shadow-sm rounded-4 h-100 p-3 py-4">
            <div class="card-body d-flex justify-content-between align-items-center p-0">
              <div>
                <h6 class="text-muted fw-semibold mb-2">Total Companies</h6>
                <h1 class="fw-bold mb-0 text-dark">{{ stats.overview.total_companies }}</h1>
              </div>
              <div class="icon-box bg-blue-light text-primary rounded-3 d-flex justify-content-center align-items-center">
                <i class="bi bi-building fs-4"></i>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card border-0 shadow-sm rounded-4 h-100 p-3 py-4">
            <div class="card-body d-flex justify-content-between align-items-center p-0">
              <div>
                <h6 class="text-muted fw-semibold mb-2">Registered Students</h6>
                <h1 class="fw-bold mb-0 text-dark">{{ stats.overview.total_students }}</h1>
              </div>
              <div class="icon-box bg-blue-light text-primary rounded-3 d-flex justify-content-center align-items-center">
                <i class="bi bi-people-fill fs-4"></i>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card border-0 shadow-sm rounded-4 h-100 p-3 py-4">
            <div class="card-body d-flex justify-content-between align-items-center p-0">
              <div>
                <h6 class="text-muted fw-semibold mb-2">Placed Students</h6>
                <h1 class="fw-bold mb-0 text-dark">{{ stats.placement_performance?.placed_students || 0 }}</h1>
              </div>
              <div class="icon-box bg-green-light text-success rounded-3 d-flex justify-content-center align-items-center">
                <i class="bi bi-check-circle-fill fs-4"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card border-0 shadow-sm rounded-4 p-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h5 class="fw-bold mb-0">Upcoming Placement Drives</h5>
          <button class="btn btn-primary fw-semibold px-3 py-2 rounded-3">
            <i class="bi bi-plus-lg me-1"></i> Add New Drive
          </button>
        </div>

        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="text-muted" style="border-bottom: 2px solid #f4f4f4;">
              <tr>
                <th class="fw-semibold pb-3 border-0">Company Name</th>
                <th class="fw-semibold pb-3 border-0">Role</th>
                <th class="fw-semibold pb-3 border-0">Date</th>
                <th class="fw-semibold pb-3 border-0">Status</th>
                <th class="fw-semibold pb-3 border-0 text-center">Action</th>
              </tr>
            </thead>
            <tbody v-if="drives.length > 0">
              <tr v-for="drive in drives" :key="drive.drive_id">
                <td class="py-3 border-light fw-bold text-dark">{{ drive.company_name }}</td>
                <td class="py-3 border-light text-secondary">{{ drive.job_title }}</td>
                <td class="py-3 border-light text-secondary">
                  {{ new Date(drive.deadline).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) }}
                </td>
                <td class="py-3 border-light text-center">
                <button v-if="drive.status === 'Pending'" 
                        @click="updateDriveStatus(drive.drive_id, 'Approved')" 
                        class="btn btn-sm btn-success me-1 rounded-pill px-2 shadow-sm" title="Approve Drive">
                  <i class="bi bi-check-lg"></i>
                </button>
                
                <button v-if="drive.status === 'Pending'" 
                        @click="updateDriveStatus(drive.drive_id, 'Rejected')" 
                        class="btn btn-sm btn-danger me-2 rounded-pill px-2 shadow-sm" title="Reject Drive">
                  <i class="bi bi-x-lg"></i>
                </button>

                <button @click="viewDriveDetails(drive.drive_id)" class="btn btn-sm btn-outline-primary rounded-pill px-3 fw-semibold">
                  Details
                </button>
              </td>
                <!-- <td class="py-3 border-light">
                  <span class="badge rounded-pill fw-medium" 
                        :class="drive.status === 'Approved' ? 'bg-success-subtle text-success' : 'bg-warning-subtle text-warning'">
                    {{ drive.status === 'Approved' ? 'Active' : drive.status }}
                  </span>
                </td>
                <td class="py-3 border-light text-center">
                  <button @click="viewDriveDetails(drive.drive_id)" class="btn btn-sm btn-outline-primary rounded-pill px-3 fw-semibold">Details</button>
                </td> -->
              </tr>
            </tbody>
            <tbody v-else>
              <tr>
                <td colspan="5" class="text-center py-5 text-muted">No upcoming placement drives found.</td>
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
const stats = ref({});
const drives = ref([]);

const fetchData = async () => {
  try {
    const statsRes = await api.get('/admin/statistics');
    stats.value = statsRes.data;

    const drivesRes = await api.get('/admin/placement-drives');
    drives.value = drivesRes.data.slice(0, 5); 
  } catch (err) {
    console.error("Error fetching data:", err);
    if (err.response && err.response.status === 401) {
      handleLogout();
    }
  }
};

const viewDriveDetails = (driveId) => {
  router.push(`/admin/drive/${driveId}`);
};

const updateDriveStatus = async (driveId, newStatus) => {
  if (!confirm(`Are you sure you want to mark this drive as ${newStatus}?`)) return;

  try {
    await api.put(`/admin/drive/${driveId}`, { status: newStatus });
    await fetchData();
  } 
  catch (err) {
    console.error("Error updating drive status:", err);
    alert("Failed to update drive status.");
  }
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.dispatchEvent(new Event("auth-changed"));
  router.push('/'); 
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
    .font-sans {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
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
    left: -16px;
    top: 10%;
    height: 80%;
    width: 4px;
    background-color: #3b82f6;
    border-radius: 0 4px 4px 0;
    }

    .icon-box {
    width: 50px;
    height: 50px;
    }
    .bg-blue-light {
    background-color: #eff6ff;
    }
    .bg-green-light {
    background-color: #f0fdf4;
    }

    .table th {
    text-transform: capitalize;
    font-size: 0.9rem;
    }
    .table td {
    font-size: 0.95rem;
    }
    .btn-outline-primary {
    border-color: #e5e7eb;
    color: #3b82f6;
    }
    .btn-outline-primary:hover {
    background-color: #eff6ff;
    border-color: #3b82f6;
    }
    
    .bg-success-subtle {
    background-color: #dcfce7 !important;
    }
    .bg-warning-subtle {
    background-color: #fef3c7 !important;
    color: #d97706 !important;
    }
</style>