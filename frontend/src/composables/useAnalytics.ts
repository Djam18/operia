import { ref, computed } from 'vue'
import { formatCurrency, type CurrencyCode } from '../utils/currency'
import type { AgingBucket } from '../components/charts/OverdueAgingChart.vue'
import type { AdvancedAnalytics } from '../interfaces/analytics'
import { apiFetch } from '../config/api'

export function useAnalytics(t: (key: string) => string) {
  const selectedCurrency = ref<CurrencyCode>('EUR')
  const isLoading = ref(false)

  const defaultAdvanced: AdvancedAnalytics = {
    dso: {
      current_dso_days: 48.2,
      prior_dso_days: 64.5,
      target_dso_days: 30.0,
      cash_freed_eur: 86420,
      days_reduced: 16.3,
      average_overdue_days: 103.6,
      unpaid_total_amount: 3592732.0,
    },
    pareto: [
      { decile_label: '0 - 20% (Top)', clients_count: 6, amount_eur: 3145000, percentage_of_total: 87.5, cumulative_percentage: 87.5 },
      { decile_label: '20 - 40%', clients_count: 6, amount_eur: 423000, percentage_of_total: 11.7, cumulative_percentage: 99.2 },
      { decile_label: '40 - 60%', clients_count: 6, amount_eur: 21000, percentage_of_total: 0.6, cumulative_percentage: 99.8 },
      { decile_label: '60 - 80%', clients_count: 6, amount_eur: 5000, percentage_of_total: 0.1, cumulative_percentage: 99.9 },
      { decile_label: '80 - 100%', clients_count: 7, amount_eur: 3732, percentage_of_total: 0.1, cumulative_percentage: 100.0 },
    ],
    top_risk_clients: [
      { name: 'SOTRA Logistique Abidjan', amount: 617390, cumulative_percentage: 17.2, invoices_count: 42 },
      { name: 'Dakar Port Terminal', amount: 547309, cumulative_percentage: 32.4, invoices_count: 38 },
      { name: 'Mali Coton Agro', amount: 524878, cumulative_percentage: 47.0, invoices_count: 35 },
    ],
    pareto_insight: 'Règle 80/20 confirmée : 6 clients concentrent 87.5% du volume des créances impayées.'
  }

  const advancedData = ref<AdvancedAnalytics>(defaultAdvanced)
  const overviewData = ref<{
    recovered_amount_eur: number
    hours_saved: number
    hitl_approval_rate: number
    avg_review_time_seconds: number
  }>({
    recovered_amount_eur: 86420,
    hours_saved: 46,
    hitl_approval_rate: 96.4,
    avg_review_time_seconds: 84
  })

  async function fetchAdvancedAnalytics(): Promise<void> {
    isLoading.value = true
    try {
      const [resAdv, resOverview] = await Promise.all([
        apiFetch('/analytics/advanced'),
        apiFetch('/analytics')
      ])
      if (resAdv.ok) {
        advancedData.value = await resAdv.json()
      }
      if (resOverview.ok) {
        overviewData.value = await resOverview.json()
      }
    } catch {
      // Fallback kept
    } finally {
      isLoading.value = false
    }
  }

  const supportedCurrencies = [
    { code: 'EUR' as CurrencyCode, label: 'EUR (€)' },
    { code: 'XOF' as CurrencyCode, label: 'FCFA (XOF)' },
    { code: 'MAD' as CurrencyCode, label: 'MAD (DH)' },
    { code: 'KES' as CurrencyCode, label: 'KES' },
  ]

  const currencyTotals: Record<CurrencyCode, number> = {
    EUR: 86420,
    XOF: 56680000,
    XAF: 24500000,
    MAD: 924000,
    KES: 12400000,
    USD: 94000,
  }

  const currentRecoveredAmount = computed(() => {
    if (selectedCurrency.value === 'EUR') {
      return overviewData.value.recovered_amount_eur || 86420
    }
    return currencyTotals[selectedCurrency.value] || 86420
  })

  const currentAgingBuckets = computed<AgingBucket[]>(() => {
    const mult = currentRecoveredAmount.value / 86420
    return [
      { label: t('analytics.aging_normal'), amount: Math.round(124500 * mult), percentage: 55, color: 'bg-emerald-500' },
      { label: t('analytics.aging_n1'), amount: Math.round(86420 * mult), percentage: 38, color: 'bg-brand-500' },
      { label: t('analytics.aging_n2'), amount: Math.round(34100 * mult), percentage: 15, color: 'bg-amber-500' },
      { label: t('analytics.aging_dispute'), amount: Math.round(11060 * mult), percentage: 5, color: 'bg-rose-500' },
    ]
  })

  const kpiMetrics = computed(() => [
    {
      id: 'recovered',
      label: t('analytics.kpi_recovered'),
      value: formatCurrency(currentRecoveredAmount.value, selectedCurrency.value),
      subtitle: t('analytics.kpi_recovered_sub'),
      variant: 'highlight' as const,
      positive: true,
    },
    {
      id: 'hours_saved',
      label: t('analytics.kpi_hours_saved'),
      value: `${overviewData.value.hours_saved} h`,
      subtitle: t('analytics.kpi_hours_saved_sub'),
      positive: false,
    },
    {
      id: 'hitl_rate',
      label: t('analytics.kpi_hitl_rate'),
      value: `${overviewData.value.hitl_approval_rate.toLocaleString('fr-FR', { minimumFractionDigits: 1 })} %`,
      subtitle: t('analytics.kpi_hitl_rate_sub'),
      positive: true,
    },
    {
      id: 'review_time',
      label: t('analytics.kpi_avg_review_time'),
      value: `${Math.floor(overviewData.value.avg_review_time_seconds / 60)}m ${overviewData.value.avg_review_time_seconds % 60}s`,
      subtitle: t('analytics.kpi_avg_review_time_sub'),
      positive: false,
    },
  ])

  return {
    selectedCurrency,
    supportedCurrencies,
    currentRecoveredAmount,
    currentAgingBuckets,
    kpiMetrics,
    advancedData,
    isLoading,
    fetchAdvancedAnalytics,
  }
}
