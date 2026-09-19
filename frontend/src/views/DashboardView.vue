<template>
  <div class="p-8 max-w-7xl mx-auto flex flex-col gap-8">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">{{ t('dashboard.welcome') }}</h1>
        <p class="text-sm text-slate-500 mt-0.5">{{ t('dashboard.subtitle') }}</p>
      </div>

      <router-link
        to="/agent"
        class="px-4 py-2.5 bg-brand-600 hover:bg-brand-700 active:bg-brand-800 text-white rounded-xl text-sm font-semibold flex items-center gap-2 shadow-sm shadow-brand-600/20 transition"
      >
        <MessageSquare class="w-4 h-4" />
        <span>{{ t('dashboard.interrogate_agent') }}</span>
      </router-link>
    </div>

    <!-- 4 KPIs Grid Component -->
    <MetricCardGrid :pending-count="store.pendingCount" :stats="store.dashboardStats" />

    <!-- Main 2-Column Section -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
      <RecentActivityList :items="recentActivity" />
      <PendingActionWidget />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { MessageSquare } from 'lucide-vue-next'
import { useAgentStore } from '../stores/agent'
import { useI18n } from '../composables/useI18n'
import { apiFetch } from '../config/api'
import MetricCardGrid from '../components/dashboard/MetricCardGrid.vue'
import RecentActivityList from '../components/dashboard/RecentActivityList.vue'
import PendingActionWidget from '../components/dashboard/PendingActionWidget.vue'

const store = useAgentStore()
const { t } = useI18n()

interface ActivityItem {
  title: string
  subtitle: string
  time: string
  status: string
}

const recentActivity = ref<ActivityItem[]>([])

onMounted(async () => {
  store.fetchOperations()
  store.fetchDashboardStats()

  // Fetch real activity from audit logs
  try {
    const res = await apiFetch('/history')
    if (res.ok) {
      const logs = await res.json()
      recentActivity.value = logs.slice(0, 5).map((l: any) => ({
        title: l.action || l.query,
        subtitle: `${l.tool || '—'} · ${l.query}`,
        time: l.timestamp,
        status: l.status === 'COMPLETED' ? t('common.completed') : l.status === 'PENDING' ? t('common.pending') : l.status,
      }))
    }
  } catch {
    // Fallback if API unreachable
  }
})
</script>
