<template>
  <aside class="w-64 bg-white border-r border-slate-200 flex flex-col justify-between h-screen shrink-0 sticky top-0">
    <div class="p-4 flex flex-col gap-4 overflow-y-auto">
      <div class="flex items-center justify-between px-2">
        <router-link to="/" class="flex items-center gap-3 hover:opacity-90 transition" title="OpérIA Dashboard">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-600 to-brand-400 flex items-center justify-center text-white shadow-sm shadow-brand-500/20">
            <Bot class="w-5 h-5" />
          </div>
          <div>
            <div class="font-bold text-slate-900 text-base leading-tight">OpérIA</div>
            <div class="text-xs text-slate-400 font-medium">{{ t('nav.agent_operational') }}</div>
          </div>
        </router-link>
        <button type="button" @click="toggleLocale"
          class="px-2 py-1 rounded-lg text-[10px] font-bold border border-slate-200 bg-slate-50 text-slate-700 hover:bg-slate-100 active:scale-95 transition cursor-pointer"
          :title="locale === 'fr' ? 'Switch to English' : 'Passer en Français'">
          {{ locale.toUpperCase() }}
        </button>
      </div>

      <router-link :to="{ path: '/agent', query: { new: Date.now() } }"
        class="w-full py-2.5 px-4 bg-brand-600 hover:bg-brand-700 active:bg-brand-800 text-white rounded-xl text-sm font-medium flex items-center justify-center gap-2 transition shadow-sm shadow-brand-600/20 cursor-pointer">
        <Plus class="w-4 h-4" />
        <span>{{ t('nav.new_chat') }}</span>
      </router-link>

      <nav class="flex flex-col gap-1">
        <router-link v-for="item in navItems" :key="item.path" :to="item.path"
          class="flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition"
          :class="[$route.path === item.path ? 'bg-brand-50 text-brand-700 font-semibold' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900']">
          <div class="flex items-center gap-2.5">
            <component :is="item.icon" class="w-4 h-4" :class="$route.path === item.path ? 'text-brand-600' : 'text-slate-400'" />
            <span>{{ item.label }}</span>
          </div>
          <span v-if="item.badge && item.badge > 0" class="px-2 py-0.5 text-[10px] font-semibold rounded-full bg-amber-100 text-amber-800">
            {{ item.badge }}
          </span>
        </router-link>
        <div class="my-1.5 border-t border-slate-100"></div>
        <router-link to="/console" class="flex items-center gap-2.5 px-3 py-1.5 rounded-xl text-xs font-medium text-slate-500 hover:bg-slate-100 transition"
          :class="[$route.path === '/console' ? 'bg-slate-100 text-slate-900 font-semibold' : '']">
          <Terminal class="w-4 h-4 text-cyan-600" />
          <span>{{ t('nav.console') }}</span>
        </router-link>
      </nav>
    </div>

    <div class="p-3 border-t border-slate-100 flex flex-col gap-2">
      <router-link to="/settings" class="flex items-center gap-2 px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100/70 rounded-xl text-xs font-medium text-emerald-800 transition cursor-pointer"
        title="Voir les connexions et paramètres">
        <span class="relative flex h-2 w-2">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
        </span>
        <span>{{ t('nav.agent_operational') }}</span>
        <span class="text-[10px] text-emerald-600 font-normal ml-auto">
          {{ store.connectivity.mode === 'online' ? t('nav.mode_cloud') : t('nav.mode_local') }}
        </span>
      </router-link>

      <div class="flex items-center justify-between p-1.5 rounded-xl hover:bg-slate-50 transition">
        <router-link to="/settings" class="flex items-center gap-2.5 flex-1 min-w-0" title="Gérer le profil">
          <div class="w-7 h-7 rounded-full bg-slate-200 text-slate-700 font-bold text-xs flex items-center justify-center shrink-0">
            {{ userInitials }}
          </div>
          <div class="min-w-0 flex-1">
            <div class="text-xs font-semibold text-slate-900 leading-tight truncate">{{ userName }}</div>
            <div class="text-[10px] text-slate-500 truncate">{{ userDept }}</div>
          </div>
        </router-link>
        <button type="button" @click.stop="handleLogout" class="p-1 rounded-lg hover:bg-red-50 text-slate-400 hover:text-red-600 transition cursor-pointer" :title="t('login.logout')">
          <LogOut class="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed, onMounted, type Component } from 'vue'
import { useRouter } from 'vue-router'
import { LayoutDashboard, Bot, SlidersHorizontal, TrendingUp, BookOpen, FlaskConical, Database, History, Settings, ShieldCheck, Plus, Terminal, LogOut } from 'lucide-vue-next'
import { useAgentStore } from '../stores/agent'
import { useAuthStore } from '../stores/auth'
import { useI18n } from '../composables/useI18n'

interface NavItem { path: string; label: string; icon: Component; badge?: number }

const store = useAgentStore()
const auth = useAuthStore()
const router = useRouter()
const { t, locale, setLocale } = useI18n()

onMounted(() => {
  store.fetchConnectivity()
  store.fetchOperations()
  auth.fetchMe()
})

const toggleLocale = () => { setLocale(locale.value === 'fr' ? 'en' : 'fr') }
const handleLogout = () => { auth.logout(); router.push('/login') }
const userName = computed(() => auth.user?.full_name || 'Alex Martin')
const userDept = computed(() => auth.user?.department || t('nav.financial_dir'))
const userInitials = computed(() => (userName.value.split(' ').map((w: string) => w[0]).join('').slice(0, 2) || 'AM').toUpperCase())

const navItems = computed<NavItem[]>(() => [
  { path: '/', label: t('nav.dashboard'), icon: LayoutDashboard },
  { path: '/agent', label: t('nav.agent'), icon: Bot },
  { path: '/operations', label: t('nav.operations'), icon: SlidersHorizontal, badge: store.pendingCount || 0 },
  { path: '/analytics', label: t('nav.analytics'), icon: TrendingUp },
  { path: '/templates', label: t('nav.templates'), icon: BookOpen },
  { path: '/sandbox', label: t('nav.sandbox'), icon: FlaskConical },
  { path: '/data', label: t('nav.data'), icon: Database },
  { path: '/history', label: t('nav.history'), icon: History },
  { path: '/settings', label: t('nav.settings'), icon: Settings },
  { path: '/admin', label: t('nav.admin'), icon: ShieldCheck },
])
</script>
