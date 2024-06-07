import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/components/HomePage.vue';
import SurvivorProfile from '@/components/SurvivorProfile.vue';
import RegisterSurvivor from '@/components/RegisterSurvivor.vue';

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/profile/:uniqueCode',
    name: 'SurvivorProfile',
    component: SurvivorProfile,
  },
  {
    path: '/register',
    name: 'RegisterSurvivor',
    component: RegisterSurvivor,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
