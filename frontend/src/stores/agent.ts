import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { StagedAction, DataSource, AuditLog, ConnectivityStatus, DashboardStats, OutboxEmail } from '../interfaces'
import { apiFetch, apiPath } from '../config/api'

export const useAgentStore = defineStore('agent', () => {
  const operations = ref<StagedAction[]>([])
  const outboxEmails = ref<OutboxEmail[]>([])
  const dataSources = ref<DataSource[]>([])
  const historyLogs = ref<AuditLog[]>([])
  const dashboardStats = ref<DashboardStats>({
    queries_count: 128,
    actions_count: 42,
    pending_count: 7,
    completed_count: 35,
  })
  const connectivity = ref<ConnectivityStatus>({
    mode: 'local',
    gemini_active: false,
    resend_active: false,
    database_type: 'SQLite (embarquée)',
    is_online: false
  })
  const isLoading = ref<boolean>(false)

  const pendingCount = computed<number>(() => {
    return operations.value.filter(op => op.status === 'PENDING').length
  })

  async function fetchConnectivity(): Promise<void> {
    try {
      const res = await apiFetch('/status/connectivity')
      if (res.ok) {
        connectivity.value = await res.json()
      }
    } catch {
      console.warn('Mode local autonome par défaut.')
    }
  }

  async function fetchOperations(status: string | null = null): Promise<void> {
    isLoading.value = true
    try {
      const path = status ? `/operations?status=${status}` : '/operations'
      const res = await apiFetch(path)
      if (res.ok) {
        operations.value = await res.json()
      }
    } catch (err) {
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }

  async function validateOperation(actionId: string): Promise<boolean> {
    try {
      const res = await apiFetch(`/operations/${actionId}/validate`, { method: 'POST' })
      if (res.ok) {
        const op = operations.value.find(o => o.action_id === actionId)
        if (op) op.status = 'COMPLETED'
        await fetchHistory()
        return true
      }
    } catch (err) {
      console.error(err)
    }
    return false
  }

  async function refuseOperation(actionId: string, reason: string | null = null): Promise<boolean> {
    try {
      const res = await apiFetch(`/operations/${actionId}/refuse`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reason })
      })
      if (res.ok) {
        const op = operations.value.find(o => o.action_id === actionId)
        if (op) op.status = 'REFUSED'
        await fetchHistory()
        return true
      }
    } catch (err) {
      console.error(err)
    }
    return false
  }

  async function batchValidate(actionIds: string[]): Promise<boolean> {
    try {
      const res = await apiFetch('/operations/batch-validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action_ids: actionIds })
      })
      if (res.ok) {
        await fetchOperations()
        await fetchHistory()
        return true
      }
    } catch (err) {
      console.error(err)
    }
    return false
  }

  async function fetchDataSources(): Promise<void> {
    try {
      const res = await apiFetch('/data-sources')
      if (res.ok) {
        dataSources.value = await res.json()
      }
    } catch (err) {
      console.error(err)
    }
  }

  async function refreshDataSources(): Promise<void> {
    try {
      const res = await apiFetch('/data-sources/refresh', { method: 'POST' })
      if (res.ok) {
        await fetchDataSources()
      }
    } catch (err) {
      console.error(err)
    }
  }

  async function fetchDashboardStats(): Promise<void> {
    try {
      const res = await apiFetch('/dashboard/stats')
      if (res.ok) {
        dashboardStats.value = await res.json()
      }
    } catch (err) {
      console.warn('Dashboard stats fallback:', err)
    }
  }

  async function fetchHistory(query: string = ''): Promise<void> {
    try {
      const path = query ? `/history?query=${encodeURIComponent(query)}` : '/history'
      const res = await apiFetch(path)
      if (res.ok) {
        historyLogs.value = await res.json()
      }
    } catch (err) {
      console.error(err)
    }
  }

  async function fetchOutbox(): Promise<void> {
    try {
      const res = await apiFetch('/operations/outbox')
      if (res.ok) {
        outboxEmails.value = await res.json()
      }
    } catch (err) {
      console.warn('Failed to fetch outbox:', err)
    }
  }

  return {
    operations,
    outboxEmails,
    dataSources,
    historyLogs,
    dashboardStats,
    connectivity,
    isLoading,
    pendingCount,
    fetchConnectivity,
    fetchOperations,
    fetchOutbox,
    fetchDashboardStats,
    validateOperation,
    refuseOperation,
    batchValidate,
    fetchDataSources,
    refreshDataSources,
    fetchHistory,
  }
})
