import { createRouter, createWebHistory } from "vue-router";

import Login from "./components/Login.vue"

import AdminDashboard from "./components/AdminDashboard.vue";
import AdminCompanies from "./components/AdminCompanies.vue";
import AdminStudents from "./components/AdminStudents.vue";

const routes =[
    {path:'/', component:Login},
    {path:'/login', component:Login},
    {path:'/admin', component:AdminDashboard},
    {path:'/admin/companies', component:AdminCompanies},
    {path:'/admin/students', component:AdminStudents} 
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;