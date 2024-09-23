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
  console.log(`to: ${to.path}, from: ${from.path}`);

  // 認証状態が未確認の場合、checkAuth を実行して完了を待つ
  if (store.state.isAuthenticated === null) {
    console.log('認証状態を確認中...');
    await store.dispatch('checkAuth');
  }

  if (to.meta.requiresAuth && !store.state.isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});


export default router;
