import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import RegisterSurvivor from '../components/RegisterSurvivor.vue';
import LoginPage from '../components/LoginPage.vue';
import SurvivorProfile from '../components/SurvivorProfile.vue';
import UpdateLocation from '../components/UpdateLocation.vue';
import ReportInfection from '../components/ReportInfection.vue';
import TradeItems from '../components/TradeItems.vue';
import DashboardPage from '@/components/DashboardPage.vue';
import ReportsPage from '@/components/ReportsPage.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/register', component: RegisterSurvivor },
  { path: '/login', component: LoginPage },
  { path: '/profile/:uniqueCode', component: SurvivorProfile },
  { path: '/dashboard/:name', name: 'Dashboard', component: DashboardPage }, 
  { path: '/update-location', component: UpdateLocation },
  { path: '/report-infection', component: ReportInfection },
  { path: '/trade-items', component: TradeItems },
  { path: '/reports', component: ReportsPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
