import type { AgingBucket } from './invoice'

export interface DashboardStats {
  queries_count: number
  actions_count: number
  pending_count: number
  completed_count: number
}

export interface RegionalSplit {
  region: string
  percentage: number
  count: number
}

export interface AnalyticsOverview {
  recovered_amount_eur: number
  hours_saved: number
  hitl_approval_rate: number
  avg_review_time_seconds: number
  pending_operations_count: number
  aging_buckets: AgingBucket[]
  regional_split: RegionalSplit[]
}

export interface DsoMetrics {
  current_dso_days: number
  prior_dso_days: number
  target_dso_days: number
  cash_freed_eur: number
  days_reduced: number
  average_overdue_days: number
  unpaid_total_amount: number
}

export interface ParetoDecile {
  decile_label: string
  clients_count: number
  amount_eur: number
  percentage_of_total: number
  cumulative_percentage: number
}

export interface TopRiskClient {
  name: string
  amount: number
  cumulative_percentage: number
  invoices_count: number
}

export interface AdvancedAnalytics {
  dso: DsoMetrics
  pareto: ParetoDecile[]
  top_risk_clients: TopRiskClient[]
  pareto_insight: string
}

