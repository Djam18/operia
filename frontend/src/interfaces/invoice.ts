export interface Invoice {
  id: string
  customer: string
  amount: number
  currency?: string
  region?: string
  days_overdue: number
  status?: string
}

export interface AgingBucket {
  label: string
  amount: number
  percentage: number
  color?: string
}
