export type OperationCriticality = 'SENSITIVE' | 'STANDARD'
export type OperationStatus = 'PENDING' | 'COMPLETED' | 'REFUSED' | 'FAILED'

export interface StagedAction {
  action_id: string
  action_type: string
  criticality: OperationCriticality
  status: OperationStatus
  title: string
  description?: string
  consequence_warning: string
  target_count: number
  financial_amount?: number
  currency?: string
  channel: string
  requested_by: string
  payload?: Record<string, any>
}

export interface OperationFilter {
  status?: OperationStatus | 'ALL'
  criticality?: OperationCriticality
  search?: string
}

export interface BatchValidationRequest {
  action_ids: string[]
}

export interface OutboxEmail {
  id: string
  recipient_email: string
  recipient_name: string
  subject: string
  body_html: string
  amount?: number
  currency?: string
  delivery_mode: string
  status: string
  created_at?: string
}

