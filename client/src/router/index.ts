import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import EmailVerify from '@/components/EmailVerify.vue';
import NotFound from '@/views/404.vue';
import Home from '@/views/Home.vue';
import Login from '@/views/Login.vue';
import Signup from '@/views/Signup.vue';
import store from '../store';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
    meta: { requiresAuth: false },
  },
  {
    path: '/verify-email/:token',
    name: 'EmailVerify',
    component: EmailVerify,
    meta: { requiresAuth: false },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { requiresAuth: false },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  console.log(`Navigating to: ${to.path}`);

  if (store.state.auth.isAuthenticated === null) {
    await store.dispatch('auth/checkAuth');
  }

  const isAuthenticated = store.state.auth.isAuthenticated;
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth && !isAuthenticated) {
    console.log('Redirecting to /login');
    return next('/login');
  }

  next();
});

export default router;