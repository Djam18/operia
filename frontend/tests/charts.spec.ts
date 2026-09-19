import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import CashflowRecoveryChart from '../src/components/charts/CashflowRecoveryChart.vue'
import OverdueAgingChart from '../src/components/charts/OverdueAgingChart.vue'
import RegionalDistributionChart from '../src/components/charts/RegionalDistributionChart.vue'
import OnboardingRoiWidget from '../src/components/onboarding/OnboardingRoiWidget.vue'
import AnalyticsDsoCard from '../src/components/analytics/AnalyticsDsoCard.vue'
import AnalyticsParetoChart from '../src/components/analytics/AnalyticsParetoChart.vue'

describe('Charts & Visualizations Suite', () => {
  it('renders CashflowRecoveryChart with default and custom total', () => {
    const wrapper = mount(CashflowRecoveryChart, {
      props: {
        totalRecovered: 120500,
        currency: 'EUR',
      },
    })

    expect(wrapper.text()).toContain('120')
    expect(wrapper.find('svg').exists()).toBe(true)
    expect(wrapper.find('polyline').exists()).toBe(true)
  })

  it('renders OverdueAgingChart with localized buckets', () => {
    const wrapper = mount(OverdueAgingChart, {
      props: {
        currency: 'EUR',
      },
    })

    expect(wrapper.text()).toContain('1 - 30')
    expect(wrapper.text()).toContain('31 - 60')
    expect(wrapper.text()).toContain('61 - 90')
    expect(wrapper.findAll('.h-full.rounded-full').length).toBe(4)
  })

  it('renders RegionalDistributionChart with 18,406 invoices and donut slices', () => {
    const wrapper = mount(RegionalDistributionChart)

    expect(wrapper.text()).toContain('18 406')
    expect(wrapper.text()).toContain('45%')
    expect(wrapper.text()).toContain('30%')
    expect(wrapper.findAll('circle').length).toBe(5) // background + 4 regions
  })

  it('renders OnboardingRoiWidget and calculates live metrics with currency toggle', async () => {
    const wrapper = mount(OnboardingRoiWidget)

    expect(wrapper.text()).toContain('Simulateur de ROI Opérationnel')
    expect(wrapper.text()).toContain('h / mois')
    expect(wrapper.text()).toContain('ETP réalloué')

    // Click on FCFA currency button
    const fcfaBtn = wrapper.findAll('button').find(b => b.text().includes('FCFA'))
    if (fcfaBtn) {
      await fcfaBtn.trigger('click')
      expect(wrapper.text()).toContain('FCFA')
    }
  })

  it('renders AnalyticsDsoCard with DSO metrics and progress bar', () => {
    const wrapper = mount(AnalyticsDsoCard, {
      props: {
        dso: {
          current_dso_days: 48.2,
          prior_dso_days: 64.5,
          target_dso_days: 30.0,
          cash_freed_eur: 86420,
          days_reduced: 16.3,
          average_overdue_days: 103.6,
          unpaid_total_amount: 3592732.0,
        },
        currency: 'EUR',
      },
    })

    expect(wrapper.text()).toContain('48.2j')
    expect(wrapper.text()).toContain('64.5j')
    expect(wrapper.text()).toContain('30j')
    expect(wrapper.text()).toContain('-16.3')
    expect(wrapper.text()).toContain('103.6')
  })

  it('renders AnalyticsParetoChart with deciles and 80/20 threshold badge', () => {
    const wrapper = mount(AnalyticsParetoChart, {
      props: {
        deciles: [
          { decile_label: '0 - 20% (Top)', clients_count: 6, amount_eur: 3145000, percentage_of_total: 87.5, cumulative_percentage: 87.5 },
          { decile_label: '20 - 40%', clients_count: 6, amount_eur: 423000, percentage_of_total: 11.7, cumulative_percentage: 99.2 },
        ],
        insight: 'Règle 80/20 confirmée : 6 clients concentrent 87.5% du volume des créances impayées.',
      },
    })

    expect(wrapper.text()).toContain('0 - 20% (Top)')
    expect(wrapper.text()).toContain('87.5%')
    expect(wrapper.text()).toContain('99.2%')
    expect(wrapper.text()).toContain('Règle 80/20 confirmée')
  })
})

