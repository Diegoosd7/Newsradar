import AccountView from '@/components/account/AccountView.vue'
import AdminView from '@/components/admin/AdminView.vue'
import AlertsView from '@/components/alerts/AlertsView.vue'
import LoginView from '@/components/login/LoginView.vue'
import NotificationsView from '@/components/notifications/NotificationsView.vue'
import SourcesRssView from '@/components/sources-rss/SourcesRssView.vue'
import StatsView from '@/components/stats/StatsView.vue'
import WordCloudView from '@/components/word-cloud/WordCloudView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
      meta: { public: true },
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: { requiresGestor: true },
    },
    {
      path: '/estadisticas',
      name: 'estadisticas',
      component: StatsView,
    },
    {
      path: '/nube-de-palabras',
      name: 'nube-de-palabras',
      component: WordCloudView,
    },
    {
      path: '/fuentes-y-rss',
      name: 'fuentes-y-rss',
      component: SourcesRssView,
      // meta: { requiresGestor: true },
    },
    {
      path: '/alertas',
      name: 'alertas',
      component: AlertsView,
      // meta: { requiresGestor: true },
    },
    {
      path: '/notificaciones',
      name: 'notificaciones',
      component: NotificationsView,
    },
    {
      path: '/cuenta',
      name: 'cuenta',
      component: AccountView,
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: () => import('@/components/login/ResetPasswordView.vue'),
      meta: { public: true } // Esto permite que se acceda sin estar logueado
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  // Redirigir a estadísticas si ya está logueado e intenta ir al login
  if (to.meta.public && auth.isAuthenticated) {
    return { name: 'estadisticas' }
  }

  // Redirigir al login si no está autenticado
  if (!to.meta.public && !auth.isAuthenticated) {
    return { name: 'login' }
  }

  // Redirigir a estadísticas si LECTOR intenta acceder a rutas de GESTOR
  if (to.meta.requiresGestor && auth.role !== 'GESTOR') {
    return { name: 'estadisticas' }
  }
})

export default router
