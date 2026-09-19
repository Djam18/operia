export interface Playbook {
  id: string
  title: string
  description?: string
  category: string
  source: string
  duration: string
  badgeVariant?: 'default' | 'secondary' | 'success' | 'warning' | 'destructive' | 'outline'
}
