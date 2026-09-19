import type { Invoice } from './invoice'
import type { StagedAction } from './operation'

export interface ConnectivityStatus {
  mode: 'local' | 'online'
  gemini_active: boolean
  resend_active: boolean
  database_type: string
  is_online: boolean
}

export interface ToolExecution {
  name?: string
  tool?: string
  duration_ms?: number
  status: string
  summary?: string
}

export interface ChatMessage {
  id: string
  sender: 'user' | 'assistant'
  content: string
  timestamp: string
  invoices?: Invoice[]
  stagedAction?: StagedAction
  toolExecuted?: ToolExecution
  tools?: ToolExecution[]
  isThinking?: boolean
  thinkingMessage?: string
}

export interface Conversation {
  id: string
  title: string
  date: string
  createdAt?: number
  updatedAt?: number
  region: string
  messages: ChatMessage[]
}
