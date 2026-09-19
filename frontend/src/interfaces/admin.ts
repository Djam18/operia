export interface DatabaseMetrics {
  type: string
  invoices_count: number
  staged_actions_count: number
  audit_logs_count: number
  data_sources_count: number
}

export interface SystemMetrics {
  memory_usage_mb: number
  cpu_threads: number
  uptime: string
}

export interface CacheStats {
  hits: number
  misses: number
  hit_ratio_percent: number
  active_keys_count: number
  total_cached_entries: number
}

export interface QueueStats {
  total_tasks: number
  queued: number
  processing: number
  completed: number
  failed: number
  avg_duration_ms: number
  is_worker_active: boolean
}

export interface QueueTask {
  id: string
  name: string
  status: 'QUEUED' | 'PROCESSING' | 'COMPLETED' | 'FAILED'
  payload: Record<string, unknown>
  queued_at: string
  started_at: string | null
  completed_at: string | null
  duration_ms: number
  error: string | null
}

export interface AdminSystemHealth {
  status: string
  app_version: string
  database: DatabaseMetrics
  system: SystemMetrics
  cache: CacheStats
  queue: QueueStats
}

export interface AdminAgentConfig {
  model_name: string
  temperature: number
  hitl_financial_threshold: number
  allowed_channels: string[]
  auto_enrich_crm: boolean
  strict_guardrails: boolean
}
