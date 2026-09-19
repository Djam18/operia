import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { setActivePinia, createPinia } from 'pinia'
import AdminSystemHealthCard from '../src/components/admin/AdminSystemHealthCard.vue'
import AdminModelConfigCard from '../src/components/admin/AdminModelConfigCard.vue'
import AdminGuardrailsCard from '../src/components/admin/AdminGuardrailsCard.vue'
import AdminQueueMonitor from '../src/components/admin/AdminQueueMonitor.vue'
import { useAdminStore } from '../src/stores/admin'
import type { AdminSystemHealth, AdminAgentConfig, QueueStats, QueueTask } from '../src/interfaces'

describe('Admin Panel Components & Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.restoreAllMocks()
  })

  const mockHealth: AdminSystemHealth = {
    status: 'healthy',
    app_version: '1.0.0',
    database: {
      type: 'SQLite (embarquée)',
      invoices_count: 18406,
      staged_actions_count: 42,
      audit_logs_count: 128,
      data_sources_count: 5
    },
    system: {
      memory_usage_mb: 48.5,
      cpu_threads: 8,
      uptime: 'Nominal'
    },
    cache: {
      hits: 15,
      misses: 2,
      hit_ratio_percent: 88.2,
      active_keys_count: 2,
      total_cached_entries: 2
    },
    queue: {
      total_tasks: 4,
      queued: 0,
      processing: 0,
      completed: 4,
      failed: 0,
      avg_duration_ms: 302.5,
      is_worker_active: true
    }
  }

  const mockConfig: AdminAgentConfig = {
    model_name: 'gemini-1.5-pro',
    temperature: 0.2,
    hitl_financial_threshold: 5000,
    allowed_channels: ['Email', 'SMS', 'Webhook'],
    auto_enrich_crm: true,
    strict_guardrails: true
  }

  const mockStats: QueueStats = {
    total_tasks: 2,
    queued: 0,
    processing: 0,
    completed: 2,
    failed: 0,
    avg_duration_ms: 250,
    is_worker_active: true
  }

  const mockTasks: QueueTask[] = [
    {
      id: 'task-1',
      name: 'batch_sync_crm',
      status: 'COMPLETED',
      payload: {},
      queued_at: new Date().toISOString(),
      started_at: new Date().toISOString(),
      completed_at: new Date().toISOString(),
      duration_ms: 280,
      error: null
    }
  ]

  it('renders AdminSystemHealthCard with metrics', () => {
    const wrapper = mount(AdminSystemHealthCard, {
      props: { health: mockHealth }
    })
    expect(wrapper.text()).toContain('18')
    expect(wrapper.text()).toContain('MB')
    expect(wrapper.text()).toContain('88.2 %')
  })

  it('renders AdminModelConfigCard and emits update', async () => {
    const wrapper = mount(AdminModelConfigCard, {
      props: { config: mockConfig, isSaving: false }
    })
    const select = wrapper.find('select')
    expect(select.exists()).toBe(true)
    await select.setValue('gemini-1.5-flash')
    expect(wrapper.emitted('update:config')).toBeTruthy()
  })

  it('renders AdminGuardrailsCard and handles toggle', async () => {
    const wrapper = mount(AdminGuardrailsCard, {
      props: { config: mockConfig, isSaving: false }
    })
    const input = wrapper.find('input[type="number"]')
    expect(input.exists()).toBe(true)
    const checkbox = wrapper.find('input[type="checkbox"]')
    await checkbox.trigger('change')
    expect(wrapper.emitted('update:config')).toBeTruthy()
  })

  it('renders AdminQueueMonitor and emits flush and retry events', async () => {
    const wrapper = mount(AdminQueueMonitor, {
      props: { stats: mockStats, tasks: mockTasks }
    })
    expect(wrapper.text()).toContain('batch_sync_crm')
    const buttons = wrapper.findAll('button')
    await buttons[0].trigger('click')
    expect(wrapper.emitted('flush-cache')).toBeTruthy()
  })

  it('manages state in useAdminStore', async () => {
    const store = useAdminStore()
    expect(store.config.model_name).toBe('gemini-1.5-pro')
    expect(store.queueStats.is_worker_active).toBe(true)
  })
})
