import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import MetricCardGrid from '../src/components/dashboard/MetricCardGrid.vue'
import PendingActionWidget from '../src/components/dashboard/PendingActionWidget.vue'
import RecentActivityList from '../src/components/dashboard/RecentActivityList.vue'

describe('Dashboard Components Suite', () => {
  it('renders MetricCardGrid with fallback values', () => {
    setActivePinia(createPinia())
    const wrapper = mount(MetricCardGrid, {
      props: {
        pendingCount: 7,
      },
    })

    expect(wrapper.text()).toContain('128')
    expect(wrapper.text()).toContain('42')
    expect(wrapper.text()).toContain('7')
    expect(wrapper.text()).toContain('35')
  })

  it('renders MetricCardGrid with live dynamic stats from props', () => {
    setActivePinia(createPinia())
    const wrapper = mount(MetricCardGrid, {
      props: {
        pendingCount: 3,
        stats: {
          queries_count: 310,
          actions_count: 85,
          pending_count: 12,
          completed_count: 73,
        },
      },
    })

    expect(wrapper.text()).toContain('310')
    expect(wrapper.text()).toContain('85')
    expect(wrapper.text()).toContain('12')
    expect(wrapper.text()).toContain('73')
  })

  it('renders PendingActionWidget with default and custom amounts', () => {
    const wrapper = mount(PendingActionWidget, {
      props: {
        title: 'Relance spéciale Q3',
        targetCount: 15,
        financialAmount: 64200,
        currency: 'EUR',
      },
      global: {
        stubs: ['router-link'],
      },
    })

    expect(wrapper.text()).toContain('Relance spéciale Q3')
    expect(wrapper.text()).toContain('15')
    expect(wrapper.text()).toContain('64')
  })

  it('renders RecentActivityList with activity items and badges', () => {
    const items = [
      { title: 'Export clients', subtitle: 'CRM', time: '5m', status: 'En attente' },
      { title: 'Audit clôturé', subtitle: 'ERP', time: '12m', status: 'Terminé' },
    ]

    const wrapper = mount(RecentActivityList, {
      props: { items },
      global: {
        stubs: ['router-link'],
      },
    })

    expect(wrapper.text()).toContain('Export clients')
    expect(wrapper.text()).toContain('Audit clôturé')
    expect(wrapper.text()).toContain('En attente')
    expect(wrapper.text()).toContain('Terminé')
  })
})
