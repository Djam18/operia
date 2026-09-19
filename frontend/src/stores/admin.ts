import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AdminSystemHealth, AdminAgentConfig, QueueStats, QueueTask } from '../interfaces'
import { apiFetch } from '../config/api'

export const useAdminStore = defineStore('admin', () => {
  const health = ref<AdminSystemHealth | null>(null)
  const config = ref<AdminAgentConfig>({
    model_name: 'gemini-1.5-pro',
    temperature: 0.2,
    hitl_financial_threshold: 5000,
    allowed_channels: ['Email', 'SMS', 'Webhook'],
    auto_enrich_crm: true,
    strict_guardrails: true
  })
  const queueStats = ref<QueueStats>({
    total_tasks: 0,
    queued: 0,
    processing: 0,
    completed: 0,
    failed: 0,
    avg_duration_ms: 0,
    is_worker_active: true
  })
  const recentTasks = ref<QueueTask[]>([])
  const isLoading = ref<boolean>(false)
  const isSaving = ref<boolean>(false)

  async function fetchHealth(): Promise<void> {
    try {
      const res = await apiFetch('/admin/health')
      if (res.ok) {
        health.value = await res.json()
      }
    } catch (err) {
      console.error('Failed to fetch admin health:', err)
    }
  }

  async function fetchConfig(): Promise<void> {
    try {
      const res = await apiFetch('/admin/config')
      if (res.ok) {
        config.value = await res.json()
      }
    } catch (err) {
      console.error('Failed to fetch admin config:', err)
    }
  }

  async function updateConfig(updatedConfig: AdminAgentConfig): Promise<boolean> {
    isSaving.value = true
    try {
      const res = await apiFetch('/admin/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedConfig)
      })
      if (res.ok) {
        config.value = await res.json()
        return true
      }
      return false
    } catch (err) {
      console.error('Failed to update admin config:', err)
      return false
    } finally {
      isSaving.value = false
    }
  }

  async function fetchQueue(): Promise<void> {
    try {
      const res = await apiFetch('/admin/queue')
      if (res.ok) {
        const data = await res.json()
        queueStats.value = data.stats
        recentTasks.value = data.recent_tasks
      }
    } catch (err) {
      console.error('Failed to fetch queue:', err)
    }
  }

  async function flushCache(): Promise<boolean> {
    try {
      const res = await apiFetch('/admin/cache/flush', { method: 'POST' })
      if (res.ok) {
        await fetchHealth()
        return true
      }
      return false
    } catch (err) {
      console.error('Failed to flush cache:', err)
      return false
    }
  }

  async function retryFailedTasks(): Promise<number> {
    try {
      const res = await apiFetch('/admin/queue/retry', { method: 'POST' })
      if (res.ok) {
        const data = await res.json()
        await fetchQueue()
        return data.retried_count || 0
      }
      return 0
    } catch (err) {
      console.error('Failed to retry tasks:', err)
      return 0
    }
  }

  async function enqueueDemoTask(taskName: string): Promise<boolean> {
    try {
      const res = await apiFetch('/admin/queue/enqueue-demo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task_name: taskName })
      })
      if (res.ok) {
        await fetchQueue()
        return true
      }
      return false
    } catch (err) {
      console.error('Failed to enqueue demo task:', err)
      return false
    }
  }

  async function loadAll(): Promise<void> {
    isLoading.value = true
    try {
      await Promise.all([fetchHealth(), fetchConfig(), fetchQueue()])
    } finally {
      isLoading.value = false
    }
  }

  return {
    health,
    config,
    queueStats,
    recentTasks,
    isLoading,
    isSaving,
    fetchHealth,
    fetchConfig,
    updateConfig,
    fetchQueue,
    flushCache,
    retryFailedTasks,
    enqueueDemoTask,
    loadAll
  }
})
