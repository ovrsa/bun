import EmailVerify from '@/pages/EmailVerify.vue'
import Home from '@/pages/Home.vue'
import Login from '@/pages/Login.vue'
import Signup from '@/pages/Signup.vue'
import store, { RootState } from '@/store'
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { Store } from 'vuex'

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
    path: '/auth/verify-email/:token',
    name: 'EmailVerify',
    component: EmailVerify,
    meta: { requiresAuth: false },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  if (
    to.path === '/' &&
    (store as Store<RootState>).state.auth.isAuthenticated === null
  ) {
    await (store as Store<RootState>).dispatch('auth/checkAuth')
  }

  const isAuthenticated = (store as Store<RootState>).state.auth.isAuthenticated
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !isAuthenticated) {
    return next('/login')
  }

  next()
})

export default router
