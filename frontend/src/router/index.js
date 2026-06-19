import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import pinia from '../stores'

const routes = [
  {
    path: '/',
    name: 'chat',
    component: () => import('../views/ChatView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('../views/AdminView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore(pinia)
  
  // Restaura tokens do localStorage caso a store esteja vazia (ex: F5)
  if (!authStore.user && authStore.token) {
    await authStore.restoreSession()
  }

  // Verifica rotas protegidas
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      return next({ name: 'login', query: { redirect: to.fullPath } })
    }
    
    // Verifica nível administrativo
    if (to.meta.requiresAdmin && !authStore.user?.is_admin) {
      return next({ name: 'chat' })
    }
  }

  // Se logado e acessando login/registro, redireciona pro chat
  if (authStore.isAuthenticated && (to.name === 'login' || to.name === 'register')) {
    return next({ name: 'chat' })
  }

  next()
})

export default router
