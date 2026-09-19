import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAgentStore } from '../src/stores/agent'
import { useAgentChat } from '../src/composables/useAgentChat'

vi.mock('vue-router', () => ({
  useRoute: () => ({ query: {} })
}))

describe('Agent Store (TypeScript)', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.restoreAllMocks()
  })

  it('computes pendingCount correctly from operations list', () => {
    const store = useAgentStore()
    expect(store.pendingCount).toBe(0)

    store.operations = [
      {
        action_id: 'act-1',
        action_type: 'RELANCE_EMAIL',
        criticality: 'SENSITIVE',
        status: 'PENDING',
        title: 'Relance 1',
        consequence_warning: 'Warning',
        target_count: 5,
        channel: 'Email',
        requested_by: 'Alex Martin'
      },
      {
        action_id: 'act-2',
        action_type: 'EXPORT_CSV',
        criticality: 'SENSITIVE',
        status: 'COMPLETED',
        title: 'Export 1',
        consequence_warning: 'Warning',
        target_count: 100,
        channel: 'CSV',
        requested_by: 'Sophie Bernard'
      },
      {
        action_id: 'act-3',
        action_type: 'RELANCE_EMAIL',
        criticality: 'SENSITIVE',
        status: 'PENDING',
        title: 'Relance 2',
        consequence_warning: 'Warning',
        target_count: 3,
        channel: 'Email',
        requested_by: 'Alex Martin'
      }
    ]

    expect(store.pendingCount).toBe(2)
  })

  it('handles successful operation validation', async () => {
    const store = useAgentStore()
    store.operations = [
      {
        action_id: 'act-4821',
        action_type: 'RELANCE_EMAIL',
        criticality: 'SENSITIVE',
        status: 'PENDING',
        title: 'Relance 12 comptes',
        consequence_warning: 'Envoi irréversible',
        target_count: 12,
        channel: 'Email',
        requested_by: 'Alex Martin'
      }
    ]

    // Mock global fetch
    global.fetch = vi.fn().mockImplementation((url: string) => {
      if (url.includes('/validate')) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ status: 'COMPLETED' }) })
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve([]) })
    })

    const success = await store.validateOperation('act-4821')
    expect(success).toBe(true)
    expect(store.operations[0].status).toBe('COMPLETED')
  })

  it('handles operation refusal and status transition', async () => {
    const store = useAgentStore()
    store.operations = [
      {
        action_id: 'act-4817',
        action_type: 'RELANCE_EMAIL',
        criticality: 'SENSITIVE',
        status: 'PENDING',
        title: 'Relance Abidjan',
        consequence_warning: 'Envoi irréversible',
        target_count: 4,
        channel: 'Email',
        requested_by: 'Alex Martin'
      }
    ]

    global.fetch = vi.fn().mockImplementation((url: string) => {
      if (url.includes('/refuse')) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ status: 'REFUSED' }) })
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve([]) })
    })

    const success = await store.refuseOperation('act-4817', 'Client régularisé')
    expect(success).toBe(true)
    expect(store.operations[0].status).toBe('REFUSED')
  })
})

describe('Agent Chat Composable & Sidebar Interactions', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.restoreAllMocks()
  })

  it('manages multi-turn conversation switching and creation', () => {
    const {
      conversations,
      activeConvId,
      activeConversation,
      currentMessages,
      createNewConversation,
      selectConversation,
      deleteConversation
    } = useAgentChat()

    expect(conversations.value.length).toBeGreaterThanOrEqual(3)
    expect(activeConvId.value).toBe('conv-factures')
    expect(activeConversation.value?.title).toBe('Factures impayées')
    expect(currentMessages.value.length).toBe(2)

    // Switch conversation
    selectConversation('conv-export')
    expect(activeConvId.value).toBe('conv-export')
    expect(activeConversation.value?.title).toBe('Export clients actifs')
    expect(currentMessages.value.length).toBe(2)

    // Create new conversation
    createNewConversation()
    expect(conversations.value.length).toBeGreaterThanOrEqual(4)
    expect(activeConversation.value?.title).toBe('Nouvelle conversation')
    expect(currentMessages.value.length).toBe(0)

    // Delete current conversation
    const newId = activeConvId.value
    deleteConversation(newId)
    expect(conversations.value.some(c => c.id === newId)).toBe(false)
  })

  it('ConversationSidebar filters conversations and emits events', async () => {
    const { mount } = await import('@vue/test-utils')
    const ConversationSidebar = (await import('../src/components/agent/ConversationSidebar.vue')).default

    const dummyConvs = [
      { id: 'c-1', title: 'Factures impayées', date: 'Aujourd’hui', createdAt: 1, region: 'Toutes', messages: [] },
      { id: 'c-2', title: 'Export clients', date: 'Hier', createdAt: 2, region: 'Europe', messages: [] }
    ]

    const wrapper = mount(ConversationSidebar, {
      props: {
        conversations: dummyConvs,
        modelValue: 'c-1'
      }
    })

    expect(wrapper.text()).toContain('Factures impayées')
    expect(wrapper.text()).toContain('Export clients')

    // Click new conversation
    const newBtn = wrapper.find('button[title="Nouvelle conversation"]')
    expect(newBtn.exists()).toBe(true)
    await newBtn.trigger('click')
    expect(wrapper.emitted('new-conversation')).toBeTruthy()

    // Select second conversation
    const convItems = wrapper.findAll('.group')
    expect(convItems.length).toBe(2)
    await convItems[1].trigger('click')
    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['c-2'])

    // Filter by search query
    const searchInput = wrapper.find('input')
    await searchInput.setValue('export')
    expect(wrapper.text()).toContain('Export clients')
    expect(wrapper.text()).not.toContain('Factures impayées')

    // Click clear search button (✕)
    const clearBtn = wrapper.findAll('button').find(b => b.text().includes('✕'))
    expect(clearBtn).toBeDefined()
    await clearBtn?.trigger('click')
    expect(wrapper.text()).toContain('Factures impayées')

    // Click Delete button on hover
    const deleteBtn = wrapper.find('button[title="Supprimer la conversation"]')
    expect(deleteBtn.exists()).toBe(true)
    await deleteBtn.trigger('click')
    expect(wrapper.emitted('delete-conversation')?.[0]).toEqual(['c-1'])
  })

  it('AgentView renders prompt buttons and triggers query', async () => {
    const { mount } = await import('@vue/test-utils')
    const AgentView = (await import('../src/views/AgentView.vue')).default

    const wrapper = mount(AgentView)
    expect(wrapper.text()).toContain('Factures impayées')

    // Find input and send button
    const input = wrapper.find('input[placeholder*="Demandez une analyse"]')
    expect(input.exists()).toBe(true)
    const sendBtn = wrapper.find('button.bg-brand-600')
    expect(sendBtn.exists()).toBe(true)
  })
})
