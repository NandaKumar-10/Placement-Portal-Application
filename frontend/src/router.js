import { createRouter, createWebHistory } from "vue-router";

import Login from "./components/Login.vue"

import AdminDashboard from "./components/AdminDashboard.vue";
import AdminCompanies from "./components/AdminCompanies.vue";
import AdminStudents from "./components/AdminStudents.vue";
import Register from "./components/Register.vue";
import StudentDasboard from "./components/StudentDasboard.vue";
import StudentEditProfile from "./components/StudentEditProfile.vue";
import Studentdrive from "./components/Studentdrive.vue";
import CompanyDashboard from "./components/CompanyDashboard.vue";
import AdminDriveDetails from "./components/AdminDriveDetails.vue";

const routes =[
    {path:'/', component:Login},
    {path:'/register', component:Register},
    {path:'/login', component:Login},
    {path:'/admin', component:AdminDashboard},
    {path:'/admin/companies', component:AdminCompanies},
    {path:'/admin/students', component:AdminStudents},
    {path:'/student/dashboard', component:StudentDasboard},
    {path:'/student/edit-profile',component:StudentEditProfile},
    {path:'/student/drive',component:Studentdrive},
    {path:'/company/dashboard', component:CompanyDashboard},
    {path: '/admin/drive/:id', component: AdminDriveDetails}
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;