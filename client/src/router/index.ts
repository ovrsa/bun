import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import EmailVerify from '@/components/EmailVerify.vue'
import NotFound from "@/views/404.vue";
import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue"
import Signup from "@/views/Signup.vue"
import store from '../store';

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup
  },
  {
    path: '/verify-email/:token',
    name: 'EmailVerify',
    component: EmailVerify,
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFound,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


router.beforeEach(async (to, from, next) => {
  console.log(`Navigating to: ${to.path}, from: ${from.path}`);

  if (store.state.isAuthenticated === null) {
    console.log('Checking authentication status...');
    await store.dispatch('checkAuth');
  }

  console.log(`Route requires auth: ${to.meta.requiresAuth}`);
  console.log(`User is authenticated: ${store.state.isAuthenticated}`);

  if (to.meta.requiresAuth) {
    if (store.state.isAuthenticated) {
      next();
    } else {
      console.log('Redirecting to /login');
      next('/login');
    }
  } else {
    next();
  }
});


export default router;
