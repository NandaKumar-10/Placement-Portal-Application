import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:5000/admin', // Adjust port if needed
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  // --- Dashboard Stats ---
  getStatistics() {
    return apiClient.get('/statistics');
  },

  // --- Company Management ---
  getCompanies() {
    return apiClient.get('/companies');
  },
  approveRejectCompany(companyId, status) {
    // status should be true (Approve) or false (Reject)
    return apiClient.put('/company-reg', { 
      company_id: companyId, 
      approval_status: status 
    });
  },
  deleteCompany(companyId) {
    return apiClient.delete(`/company/${companyId}`);
  },

  // --- Student Management ---
  getStudents() {
    return apiClient.get('/students');
  },
  deleteStudent(studentId) {
    return apiClient.delete(`/student/${studentId}`);
  },

  // --- Placement Drives ---
  getDrives() {
    return apiClient.get('/placement-drives');
  },
  updateDriveStatus(driveId, status) {
    // status: "Approved" or "Rejected"
    return apiClient.put('/placement-drive', { 
      drive_id: driveId, 
      status: status 
    });
  },

  // --- Search & Blacklist ---
  search(query) {
    return apiClient.get(`/search?q=${query}`);
  },
  blacklistUser(userId, action) {
    // action: "block" or "unblock"
    return apiClient.post('/blacklist', { 
      user_id: userId, 
      action: action 
    });
  }
};