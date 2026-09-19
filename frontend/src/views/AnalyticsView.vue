<template>
  <div class="p-8 max-w-7xl mx-auto flex flex-col gap-8">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">{{ t('analytics.title') }}</h1>
        <p class="text-sm text-slate-500 mt-0.5">{{ t('analytics.subtitle') }}</p>
      </div>

      <div class="flex items-center gap-3">
        <!-- Currency / Region Switcher -->
        <div class="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200/80">
          <button
            v-for="curr in supportedCurrencies"
            :key="curr.code"
            @click="selectedCurrency = curr.code"
            type="button"
            class="px-2.5 py-1 text-xs font-semibold rounded-lg transition cursor-pointer"
            :class="selectedCurrency === curr.code ? 'bg-white text-brand-700 shadow-xs' : 'text-slate-500 hover:text-slate-800'"
          >
            {{ curr.label }}
          </button>
        </div>

        <UiButton variant="outline" size="sm" @click="refreshData">
          <RefreshCw class="w-3.5 h-3.5 mr-1.5" />
          {{ t('common.refresh') }}
        </UiButton>
      </div>
    </div>

    <!-- Impact KPI Grid -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <ImpactMetricCard
        v-for="kpi in kpiMetrics"
        :key="kpi.id"
        :label="kpi.label"
        :value="kpi.value"
        :subtitle="kpi.subtitle"
        :variant="kpi.variant"
        :positive="kpi.positive"
      />
    </div>

    <!-- Data Analyst Deep-Dive: DSO & Pareto 80/20 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <AnalyticsDsoCard :dso="advancedData.dso" :currency="selectedCurrency" />
      <AnalyticsParetoChart :deciles="advancedData.pareto" :insight="advancedData.pareto_insight" />
    </div>

    <!-- Charts Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <UiCard class="lg:col-span-2">
        <template #header>
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-sm font-bold text-slate-900">{{ t('analytics.cashflow_title') }}</h3>
              <p class="text-xs text-slate-400">{{ t('analytics.cashflow_sub') }}</p>
            </div>
            <UiBadge variant="success">Flux Actif · {{ selectedCurrency }}</UiBadge>
          </div>
        </template>
        <CashflowRecoveryChart :total-recovered="currentRecoveredAmount" :currency="selectedCurrency" />
      </UiCard>

      <UiCard>
        <template #header>
          <div>
            <h3 class="text-sm font-bold text-slate-900">{{ t('analytics.regional_title') }}</h3>
            <p class="text-xs text-slate-400">{{ t('analytics.regional_sub') }}</p>
          </div>
        </template>
        <RegionalDistributionChart />
      </UiCard>
    </div>

    <!-- Overdue Aging Chart Bar -->
    <UiCard>
      <template #header>
        <div>
          <h3 class="text-sm font-bold text-slate-900">{{ t('analytics.aging_title') }}</h3>
          <p class="text-xs text-slate-400">{{ t('analytics.aging_sub') }} ({{ selectedCurrency }})</p>
        </div>
      </template>
      <OverdueAgingChart :buckets="currentAgingBuckets" :currency="selectedCurrency" />
    </UiCard>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { RefreshCw } from 'lucide-vue-next'
import UiButton from '../components/ui/UiButton.vue'
import UiBadge from '../components/ui/UiBadge.vue'
import UiCard from '../components/ui/UiCard.vue'
import ImpactMetricCard from '../components/analytics/ImpactMetricCard.vue'
import AnalyticsDsoCard from '../components/analytics/AnalyticsDsoCard.vue'
import AnalyticsParetoChart from '../components/analytics/AnalyticsParetoChart.vue'
import CashflowRecoveryChart from '../components/charts/CashflowRecoveryChart.vue'
import RegionalDistributionChart from '../components/charts/RegionalDistributionChart.vue'
import OverdueAgingChart from '../components/charts/OverdueAgingChart.vue'
import { useI18n } from '../composables/useI18n'
import { useAnalytics } from '../composables/useAnalytics'

const { t } = useI18n()
const {
  selectedCurrency,
  supportedCurrencies,
  currentRecoveredAmount,
  currentAgingBuckets,
  kpiMetrics,
  advancedData,
  fetchAdvancedAnalytics,
} = useAnalytics(t)

onMounted(() => {
  fetchAdvancedAnalytics()
})

function refreshData(): void {
  fetchAdvancedAnalytics()
}
</script>

