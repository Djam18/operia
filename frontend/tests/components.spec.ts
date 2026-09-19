import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import StagedActionCard from '../src/components/StagedActionCard.vue'
import ToolExecutionBadge from '../src/components/ToolExecutionBadge.vue'
import type { StagedAction } from '../src/types'

describe('Frontend UI Components (TypeScript)', () => {
  it('renders StagedActionCard with warning consequences and buttons', () => {
    setActivePinia(createPinia())

    const action: StagedAction = {
      action_id: 'act-4821',
      action_type: 'RELANCE_EMAIL',
      criticality: 'SENSITIVE',
      status: 'PENDING',
      title: 'Envoyer une relance à 8 clients',
      consequence_warning: 'Les messages seront envoyés aux contacts financiers.',
      target_count: 8,
      financial_amount: 42680,
      channel: 'Email',
      requested_by: 'Alex Martin'
    }

    const wrapper = mount(StagedActionCard, {
      props: { action }
    })

    expect(wrapper.text().toLowerCase()).toContain('action à valider')
    expect(wrapper.text()).toContain('Envoyer une relance à 8 clients')
    expect(wrapper.text()).toContain('8 contacts')
    expect(wrapper.text()).toContain('Conséquence :')
    expect(wrapper.text()).toContain('Valider et exécuter')
    expect(wrapper.text()).toContain('Refuser')
  })

  it('renders ToolExecutionBadge and toggles tool traces', async () => {
    const wrapper = mount(ToolExecutionBadge, {
      props: {
        title: 'CRM et base de données'
      }
    })

    expect(wrapper.text()).toContain('Outils utilisés :')
    expect(wrapper.text()).toContain('CRM et base de données')
    expect(wrapper.text()).toContain('Completed')

    // Initial state: details closed
    expect(wrapper.find('.font-mono').exists()).toBe(false)

    // Click to expand
    await wrapper.find('button').trigger('click')
    expect(wrapper.find('.font-mono').exists()).toBe(true)
    expect(wrapper.text()).toContain('erp.factures.query')
    expect(wrapper.text()).toContain('crm.comptes.enrich')
  })

  it('StagedActionCard button clicks: validate and refuse trigger status update and emit', async () => {
    setActivePinia(createPinia())
    const { useAgentStore } = await import('../src/stores/agent')
    const store = useAgentStore()
    store.validateOperation = vi.fn().mockResolvedValue(true)
    store.refuseOperation = vi.fn().mockResolvedValue(true)

    const action: StagedAction = {
      action_id: 'act-btn-test',
      action_type: 'RELANCE_EMAIL',
      criticality: 'SENSITIVE',
      status: 'PENDING',
      title: 'Action test boutons',
      consequence_warning: 'Avertissement',
      target_count: 3,
      channel: 'Email',
      requested_by: 'Alex'
    }

    const wrapper = mount(StagedActionCard, {
      props: { action }
    })

    // Click Validate button
    const validateBtn = wrapper.findAll('button').find(b => b.text().includes('Valider et exécuter'))
    expect(validateBtn).toBeDefined()
    await validateBtn?.trigger('click')

    expect(store.validateOperation).toHaveBeenCalledWith('act-btn-test')
    expect(action.status).toBe('COMPLETED')
    expect(wrapper.emitted('validated')?.[0]).toEqual(['act-btn-test'])
  })

  it('InvoiceTableCard button toggles showAll emit', async () => {
    const InvoiceTableCard = (await import('../src/components/agent/InvoiceTableCard.vue')).default
    const invoices = [
      { id: 'F1', customer: 'Client A', amount: 1000, currency: 'EUR', days_overdue: 35, region: 'Europe', status: 'impaye' },
      { id: 'F2', customer: 'Client B', amount: 2000, currency: 'EUR', days_overdue: 40, region: 'Europe', status: 'impaye' }
    ]

    const wrapper = mount(InvoiceTableCard, {
      props: {
        invoices,
        totalCount: 2,
        showAll: false
      }
    })

    const toggleBtn = wrapper.find('button')
    expect(toggleBtn.exists()).toBe(true)
    await toggleBtn.trigger('click')
    expect(wrapper.emitted('toggleShowAll')).toBeTruthy()
  })

  it('ChatMessageBubble renders user and assistant bubbles and handles show-all toggle', async () => {
    setActivePinia(createPinia())
    const ChatMessageBubble = (await import('../src/components/agent/ChatMessageBubble.vue')).default

    // Test User Message
    const userMsg = {
      id: 'm-1',
      sender: 'user' as const,
      content: 'Bonjour OpérIA',
      timestamp: '10:00'
    }
    const userWrapper = mount(ChatMessageBubble, { props: { message: userMsg } })
    expect(userWrapper.text()).toContain('Bonjour OpérIA')
    expect(userWrapper.text()).toContain('10:00')

    // Test Assistant Message with Invoices
    const asstMsg = {
      id: 'm-2',
      sender: 'assistant' as const,
      content: 'Voici vos factures',
      timestamp: '10:01',
      invoices: [
        { id: 'F1', customer: 'Client A', amount: 1000, currency: 'EUR', days_overdue: 35, region: 'Europe', status: 'impaye' }
      ]
    }
    const asstWrapper = mount(ChatMessageBubble, { props: { message: asstMsg } })
    expect(asstWrapper.text()).toContain('OpérIA')
    expect(asstWrapper.text()).toContain('Voici vos factures')
    expect(asstWrapper.text()).toContain('Client A')

    // Test show-all button inside ChatMessageBubble
    const seeAllBtn = asstWrapper.find('button')
    expect(seeAllBtn.exists()).toBe(true)
    await seeAllBtn.trigger('click')
    // Local state toggled
    expect(asstWrapper.vm.isShowingAll).toBe(true)
  })
})
