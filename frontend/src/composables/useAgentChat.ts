import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import type { Invoice, StagedAction, ChatMessage, Conversation, ToolExecution } from '../interfaces'
import { apiFetch } from '../config/api'

export type { ToolExecution, ChatMessage, Conversation }

const INITIAL_CONVERSATIONS: Conversation[] = [
  {
    id: 'conv-factures',
    title: 'Factures impayées',
    date: 'Aujourd’hui, 10:14',
    createdAt: Date.now() - 3600000,
    region: 'Toutes',
    messages: [
      {
        id: 'msg-init-1',
        sender: 'user',
        content: 'Donne-moi les factures impayées depuis plus de 30 jours.',
        timestamp: '10:14'
      },
      {
        id: 'msg-init-2',
        sender: 'assistant',
        content: "J'ai interrogé la base ERP et le CRM. 23 factures présentent un retard supérieur à 30 jours pour un encours total de 86 420 €. 4 comptes éligibles ont été isolés pour relance (Mali Coton Agro est automatiquement exclu en raison d'un litige ouvert).",
        timestamp: '10:14',
        tools: [
          { tool: 'erp.factures.query', status: 'ok', duration_ms: 12, summary: '18 406 factures analysées' },
          { tool: 'crm.comptes.enrich', status: 'ok', duration_ms: 18, summary: '12 comptes enrichis · 1 litige exclu' }
        ],
        invoices: [
          { id: 'FAC-2026-089', customer: 'Atelier N7', amount: 8450, currency: 'EUR', days_overdue: 39, region: 'Europe', status: 'impaye' },
          { id: 'FAC-2026-042', customer: 'Casablanca Tech Solutions', amount: 32000, currency: 'MAD', days_overdue: 38, region: 'Afrique du Nord', status: 'impaye' },
          { id: 'FAC-2026-104', customer: 'SOTRA Logistique Abidjan', amount: 24968000, currency: 'XOF', days_overdue: 35, region: 'Afrique de l\'Ouest', status: 'impaye' },
          { id: 'FAC-2026-015', customer: 'Nova Conseil', amount: 12800, currency: 'EUR', days_overdue: 34, region: 'Europe', status: 'impaye' },
          { id: 'FAC-2026-077', customer: 'Mali Coton Agro', amount: 14500000, currency: 'XOF', days_overdue: 44, region: 'Afrique de l\'Ouest', status: 'impaye' }
        ],
        stagedAction: {
          action_id: 'act-4821',
          action_type: 'RELANCE_EMAIL',
          criticality: 'SENSITIVE',
          status: 'PENDING',
          title: 'Relance de factures échues',
          description: 'Comptes éligibles identifiés sans litige (4 comptes).',
          consequence_warning: 'Les messages seront envoyés aux contacts financiers via SMTP Mailpit.',
          target_count: 4,
          financial_amount: 42680,
          currency: 'EUR',
          channel: 'Email',
          requested_by: 'Alex Martin'
        }
      }
    ]
  },
  {
    id: 'conv-export',
    title: 'Export clients actifs',
    date: 'Hier, 16:42',
    createdAt: Date.now() - 86400000,
    region: 'Europe',
    messages: [
      {
        id: 'msg-exp-1',
        sender: 'user',
        content: 'Prépare un export CSV des comptes clients actifs en Europe.',
        timestamp: 'Hier, 16:42'
      },
      {
        id: 'msg-exp-2',
        sender: 'assistant',
        content: "Export préparé pour 42 comptes clients actifs en zone Europe. L'opération a été préparée et nécessite votre validation pour générer le fichier CSV téléchargeable.",
        timestamp: 'Hier, 16:42',
        tools: [
          { tool: 'crm.comptes.enrich', status: 'ok', duration_ms: 14, summary: '42 comptes exportables' }
        ],
        stagedAction: {
          action_id: 'act-4820',
          action_type: 'EXPORT_CSV',
          criticality: 'SENSITIVE',
          status: 'COMPLETED',
          title: 'Export des comptes clients actifs',
          description: 'Extraction complète des comptes clients actifs (42 comptes).',
          consequence_warning: 'Fichier CSV téléchargeable.',
          target_count: 42,
          financial_amount: 0,
          currency: 'EUR',
          channel: 'CSV',
          requested_by: 'Sophie Bernard'
        }
      }
    ]
  },
  {
    id: 'conv-encours',
    title: 'Analyse des limites de crédit',
    date: '15 sept., 09:18',
    createdAt: Date.now() - 345600000,
    region: 'Europe',
    messages: [
      {
        id: 'msg-enc-1',
        sender: 'user',
        content: "Atelier N7 sollicite une révision de sa limite d'encours à 35 000 €.",
        timestamp: '15 sept., 09:18'
      },
      {
        id: 'msg-enc-2',
        sender: 'assistant',
        content: "Le client Atelier N7 a un historique de paiement favorable avec un taux de recouvrement supérieur à 92%. J'ai préparé l'ajustement du plafond de crédit à 35 000 €. Cette modification requiert votre confirmation formelle.",
        timestamp: '15 sept., 09:18',
        tools: [
          { tool: 'crm.comptes.enrich', status: 'ok', duration_ms: 16, summary: 'Scoring risque validé' }
        ],
        stagedAction: {
          action_id: 'act-4822',
          action_type: 'AJUSTEMENT_ENCOURS',
          criticality: 'SENSITIVE',
          status: 'PENDING',
          title: 'Ajustement limite de crédit Atelier N7',
          description: "Augmentation de la limite de crédit d'Atelier N7 à 35 000 €.",
          consequence_warning: 'Modification directe du paramètre dans le CRM.',
          target_count: 1,
          financial_amount: 35000,
          currency: 'EUR',
          channel: 'CRM',
          requested_by: 'Alex Martin'
        }
      }
    ]
  }
]

export function useAgentChat() {
  const route = useRoute()
  const conversations = ref<Conversation[]>(INITIAL_CONVERSATIONS)
  const activeConvId = ref<string>('conv-factures')
  const selectedRegion = ref<string>('Toutes')
  const inputQuery = ref<string>('')
  const showAll = ref<boolean>(false)
  const isStreaming = ref<boolean>(false)
  const isThinking = ref<boolean>(false)
  const thinkingMessage = ref<string>("Analyse de la demande en langage naturel...")
  const chatScrollRef = ref<HTMLElement | null>(null)

  const activeConvIdx = computed({
    get: () => {
      const idx = conversations.value.findIndex(c => c.id === activeConvId.value)
      return idx >= 0 ? idx : 0
    },
    set: (val: number) => {
      if (conversations.value[val]) {
        activeConvId.value = conversations.value[val].id
      }
    }
  })

  const activeConversation = computed(() => {
    return conversations.value.find(c => c.id === activeConvId.value) || conversations.value[0]
  })

  const currentMessages = computed(() => {
    return activeConversation.value?.messages || []
  })

  // Backward-compatibility properties for older component bindings
  const userPrompt = computed(() => {
    const msgs = currentMessages.value
    for (let i = msgs.length - 1; i >= 0; i--) {
      if (msgs[i].sender === 'user') return msgs[i].content
    }
    return ''
  })

  const assistantSummary = computed(() => {
    const msgs = currentMessages.value
    for (let i = msgs.length - 1; i >= 0; i--) {
      if (msgs[i].sender === 'assistant') return msgs[i].content
    }
    return ''
  })

  const displayedInvoices = computed<Invoice[]>(() => {
    const msgs = currentMessages.value
    for (let i = msgs.length - 1; i >= 0; i--) {
      if (msgs[i].invoices && msgs[i].invoices!.length > 0) return msgs[i].invoices!
    }
    return []
  })

  const invoiceCount = computed(() => displayedInvoices.value.length)

  const activeTools = computed<ToolExecution[]>(() => {
    const msgs = currentMessages.value
    for (let i = msgs.length - 1; i >= 0; i--) {
      if (msgs[i].tools && msgs[i].tools!.length > 0) return msgs[i].tools!
    }
    return []
  })

  const currentAction = computed<StagedAction | null>(() => {
    const msgs = currentMessages.value
    for (let i = msgs.length - 1; i >= 0; i--) {
      if (msgs[i].stagedAction) return msgs[i].stagedAction!
    }
    return null
  })

  function scrollToBottom(): void {
    nextTick(() => {
      if (chatScrollRef.value) {
        chatScrollRef.value.scrollTop = chatScrollRef.value.scrollHeight
      }
    })
  }

  function createNewConversation(): void {
    if (
      activeConversation.value &&
      activeConversation.value.messages.length === 0 &&
      activeConversation.value.title === 'Nouvelle conversation'
    ) {
      inputQuery.value = ''
      scrollToBottom()
      return
    }

    const newId = `conv-${Date.now()}`
    const newConv: Conversation = {
      id: newId,
      title: 'Nouvelle conversation',
      date: 'À l’instant',
      createdAt: Date.now(),
      region: selectedRegion.value,
      messages: []
    }
    conversations.value.unshift(newConv)
    activeConvId.value = newId
    inputQuery.value = ''
    scrollToBottom()
  }

  function resetChat(): void {
    createNewConversation()
  }

  async function selectConversation(id: string): Promise<void> {
    activeConvId.value = id
    const conv = conversations.value.find(c => c.id === id)
    if (conv && conv.messages.length === 0) {
      try {
        const res = await apiFetch(`/conversations/${id}/messages`)
        if (res.ok) {
          const list = await res.json()
          if (Array.isArray(list) && list.length > 0) {
            conv.messages = list.map((m: any) => ({
              id: m.id,
              sender: m.sender as 'user' | 'assistant',
              content: m.content,
              timestamp: m.created_at ? new Date(m.created_at).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }) : '',
              invoices: m.meta?.invoices,
              stagedAction: m.meta?.action,
              tools: m.meta?.tools
            }))
          }
        }
      } catch {
        // ignore
      }
    }
    scrollToBottom()
  }

  async function deleteConversation(id: string): Promise<void> {
    const idx = conversations.value.findIndex(c => c.id === id)
    if (idx === -1) return
    conversations.value.splice(idx, 1)

    try {
      await apiFetch(`/conversations/${id}`, { method: 'DELETE' })
    } catch {
      // ignore
    }

    if (conversations.value.length === 0) {
      createNewConversation()
    } else if (activeConvId.value === id) {
      await selectConversation(conversations.value[0].id)
    }
  }

  function handleSSE(event: string, data: any, assistantMsg: ChatMessage) {
    if (event === 'thinking') {
      isThinking.value = true
      assistantMsg.isThinking = true
      if (data.status) {
        thinkingMessage.value = data.status
        assistantMsg.thinkingMessage = data.status
      }
    } else if (event === 'tool_call_started') {
      isThinking.value = false
      assistantMsg.isThinking = false
      assistantMsg.tools = assistantMsg.tools || []
      const existing = assistantMsg.tools.find(t => t.tool === data.tool)
      if (!existing) {
        assistantMsg.tools.push({ tool: data.tool, status: 'en cours...', summary: 'Interrogation...' })
      }
    } else if (event === 'tool_call_completed') {
      assistantMsg.tools = assistantMsg.tools || []
      const idx = assistantMsg.tools.findIndex(t => t.tool === data.tool)
      const entry: ToolExecution = {
        tool: data.tool,
        status: data.status || 'ok',
        duration_ms: data.duration_ms || 15,
        summary: data.summary || 'Exécuté'
      }
      if (idx >= 0) {
        assistantMsg.tools[idx] = entry
      } else {
        assistantMsg.tools.push(entry)
      }
    } else if (event === 'content_delta') {
      isThinking.value = false
      assistantMsg.isThinking = false
      if (data.text) {
        assistantMsg.content += data.text
      }
    } else if (event === 'invoices_table') {
      try {
        const list = typeof data === 'string' ? JSON.parse(data) : data
        if (Array.isArray(list)) {
          assistantMsg.invoices = list
        }
      } catch (e) {
        console.error('Failed to parse invoices_table', e)
      }
    } else if (event === 'staged_action_created') {
      assistantMsg.stagedAction = data
    } else if (event === 'done') {
      isStreaming.value = false
      isThinking.value = false
      assistantMsg.isThinking = false
    }
    scrollToBottom()
  }

  async function sendCustomQuery(overrideText?: string): Promise<void> {
    const q = (overrideText || inputQuery.value).trim()
    if (!q || isStreaming.value) return

    let currentConv = activeConversation.value
    if (!currentConv) {
      createNewConversation()
      currentConv = activeConversation.value!
    }

    // Auto-update conversation title if default
    if (currentConv.title === 'Nouvelle conversation' || currentConv.messages.length === 0) {
      currentConv.title = q.length > 35 ? q.slice(0, 35) + '...' : q
    }

    const nowStr = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
    currentConv.date = 'À l’instant'

    // Add user message
    const userMsg: ChatMessage = {
      id: `msg-user-${Date.now()}`,
      sender: 'user',
      content: q,
      timestamp: nowStr
    }
    currentConv.messages.push(userMsg)
    inputQuery.value = ''

    // Add placeholder assistant message
    const assistantMsg: ChatMessage = {
      id: `msg-asst-${Date.now()}`,
      sender: 'assistant',
      content: '',
      timestamp: nowStr,
      isThinking: true,
      thinkingMessage: 'Analyse de la demande en langage naturel...',
      tools: []
    }
    currentConv.messages.push(assistantMsg)

    isStreaming.value = true
    isThinking.value = true
    thinkingMessage.value = 'Analyse de la demande en langage naturel...'
    scrollToBottom()

    try {
      const res = await apiFetch('/agent/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: q,
          conversation_id: currentConv.id
        })
      })

      if (!res.ok || !res.body) {
        assistantMsg.isThinking = false
        assistantMsg.content = "Erreur de connexion à l'agent."
        return
      }

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })

        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        let currentEvent = 'message'
        for (const line of lines) {
          const trimmed = line.trim()
          if (trimmed.startsWith('event:')) {
            currentEvent = trimmed.slice(6).trim()
          } else if (trimmed.startsWith('data:')) {
            const dataStr = trimmed.slice(5).trim()
            if (!dataStr) continue
            try {
              const parsed = JSON.parse(dataStr)
              handleSSE(currentEvent, parsed, assistantMsg)
            } catch {
              // ignore
            }
          }
        }
      }
    } catch (err) {
      console.error('SSE Error:', err)
      assistantMsg.isThinking = false
      assistantMsg.content = "Impossible de joindre l'agent en direct. Vérifiez que le backend FastAPI est actif."
    } finally {
      isStreaming.value = false
      isThinking.value = false
      assistantMsg.isThinking = false
      scrollToBottom()
    }
  }

  function triggerQuery(): void {
    const region = selectedRegion.value
    if (region === 'Toutes') {
      sendCustomQuery("Donne-moi les factures impayées depuis plus de 30 jours.")
    } else {
      sendCustomQuery(`Donne-moi les factures impayées en ${region}`)
    }
  }

  async function loadRemoteConversations() {
    try {
      const res = await apiFetch('/conversations')
      if (res.ok) {
        const list = await res.json()
        if (Array.isArray(list) && list.length > 0) {
          for (const item of list) {
            const exists = conversations.value.find(c => c.id === item.id)
            if (!exists) {
              conversations.value.push({
                id: item.id,
                title: item.title,
                date: item.updated_at ? new Date(item.updated_at).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' }) : 'Récent',
                createdAt: item.created_at ? new Date(item.created_at).getTime() : Date.now(),
                region: 'Toutes',
                messages: []
              })
            }
          }
        }
      }
    } catch {
      // offline/fallback
    }
  }

  onMounted(() => {
    loadRemoteConversations()
    if (route && route.query) {
      if (route.query.prompt) {
        sendCustomQuery(route.query.prompt as string)
      } else if (route.query.new) {
        resetChat()
      }
    }
  })

  watch(() => route?.query, (q) => {
    if (q?.prompt) {
      sendCustomQuery(q.prompt as string)
    } else if (q?.new) {
      resetChat()
    }
  })

  return {
    conversations,
    activeConvId,
    activeConvIdx,
    activeConversation,
    currentMessages,
    selectedRegion,
    inputQuery,
    showAll,
    isStreaming,
    isThinking,
    thinkingMessage,
    chatScrollRef,
    userPrompt,
    displayedInvoices,
    invoiceCount,
    assistantSummary,
    activeTools,
    currentAction,
    createNewConversation,
    selectConversation,
    deleteConversation,
    triggerQuery,
    sendCustomQuery,
    resetChat,
    scrollToBottom,
  }
}
