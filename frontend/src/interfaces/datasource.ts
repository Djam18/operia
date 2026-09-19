export interface DataSource {
  id: string
  name: string
  type: string
  record_count: number
  last_synced_at: string
  status: 'COMPLETED' | 'IN_PROGRESS' | 'ERROR'
}
