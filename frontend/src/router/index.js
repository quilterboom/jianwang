import { createRouter, createWebHistory } from 'vue-router'
import { getProfile } from '@/api/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { guest: true }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 只有访问需要认证的页面才检查登录状态
  if (to.matched.some(record => record.meta.requiresAuth)) {
    try {
      await getProfile()
      next()
    } catch (error) {
      next('/login')
    }
  } else if (to.matched.some(record => record.meta.guest)) {
    // 游客页面（登录/注册）不检查登录状态，直接放行
    next()
  } else {
    next()
  }
})

export default router
