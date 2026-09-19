import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import AgentView from '../views/AgentView.vue'
import OperationsView from '../views/OperationsView.vue'
import DataView from '../views/DataView.vue'
import HistoryView from '../views/HistoryView.vue'
import SettingsView from '../views/SettingsView.vue'
import ConsoleView from '../views/ConsoleView.vue'
import AnalyticsView from '../views/AnalyticsView.vue'
import TemplatesView from '../views/TemplatesView.vue'
import SandboxView from '../views/SandboxView.vue'
import OnboardingView from '../views/OnboardingView.vue'
import AdminView from '../views/AdminView.vue'
import LoginView from '../views/LoginView.vue'

const routes: Array<RouteRecordRaw> = [
  { path: '/login', name: 'Login', component: LoginView, meta: { public: true } },
  { path: '/', name: 'Dashboard', component: DashboardView },
  { path: '/agent', name: 'Agent', component: AgentView },
  { path: '/operations', name: 'Operations', component: OperationsView },
  { path: '/analytics', name: 'Analytics', component: AnalyticsView },
  { path: '/templates', name: 'Templates', component: TemplatesView },
  { path: '/sandbox', name: 'Sandbox', component: SandboxView },
  { path: '/onboarding', name: 'Onboarding', component: OnboardingView },
  { path: '/data', name: 'Data', component: DataView },
  { path: '/history', name: 'History', component: HistoryView },
  { path: '/settings', name: 'Settings', component: SettingsView },
  { path: '/admin', name: 'Admin', component: AdminView },
  { path: '/console', name: 'Console', component: ConsoleView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Auth guard — redirect to /login if not authenticated
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('operia_token')
  if (!to.meta.public && !token) {
    next({ name: 'Login' })
  } else if (to.name === 'Login' && token) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
