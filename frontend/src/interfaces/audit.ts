export interface AuditLog {
  id: string
  timestamp: string
  user: string
  query: string
  tool: string
  action: string
  status: 'PENDING' | 'COMPLETED' | 'FAILED' | 'REFUSED'
  details?: Record<string, any>
}
