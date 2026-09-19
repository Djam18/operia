<template>
  <div class="p-5 rounded-2xl bg-white border border-slate-200/80 shadow-xs flex flex-col justify-between">
    <div>
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2">
          <div class="p-2 rounded-xl bg-blue-50 text-blue-600">
            <Clock class="w-4 h-4" />
          </div>
          <div>
            <h4 class="text-sm font-bold text-slate-900">{{ t('analytics.dso_title') }}</h4>
            <p class="text-xs text-slate-400">{{ t('analytics.dso_sub') }}</p>
          </div>
        </div>
        <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200/60">
          -{{ dso.days_reduced }} {{ t('analytics.dso_days') }}
        </span>
      </div>

      <!-- Formula hint -->
      <div class="text-[11px] font-mono text-slate-400 bg-slate-50 px-2.5 py-1 rounded-lg mb-4 border border-slate-100">
        {{ t('analytics.dso_formula') }}
      </div>

      <!-- DSO Progression Bar -->
      <div class="space-y-2 mb-4">
        <div class="flex justify-between text-xs font-semibold">
          <span class="text-slate-400">{{ t('analytics.dso_prior') }}: {{ dso.prior_dso_days }}j</span>
          <span class="text-blue-600 font-bold">{{ t('analytics.dso_current') }}: {{ dso.current_dso_days }}j</span>
          <span class="text-emerald-600">{{ t('analytics.dso_target') }}: {{ dso.target_dso_days }}j</span>
        </div>

        <div class="relative w-full h-3 bg-slate-100 rounded-full overflow-hidden flex">
          <div
            class="h-full bg-linear-to-r from-blue-500 to-emerald-500 rounded-full transition-all duration-700"
            :style="{ width: `${progressPercent}%` }"
          />
        </div>
      </div>
    </div>

    <!-- Bottom KPI Highlights -->
    <div class="grid grid-cols-2 gap-3 pt-3 border-t border-slate-100">
      <div class="bg-emerald-50/50 p-2.5 rounded-xl border border-emerald-100/80">
        <div class="text-[11px] font-medium text-emerald-700">{{ t('analytics.dso_cash_freed') }}</div>
        <div class="text-base font-bold text-emerald-900 mt-0.5">
          +{{ formattedCashFreed }}
        </div>
      </div>
      <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
        <div class="text-[11px] font-medium text-slate-500">Moyenne retard</div>
        <div class="text-base font-bold text-slate-800 mt-0.5">
          {{ dso.average_overdue_days }} {{ t('analytics.dso_days') }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Clock } from 'lucide-vue-next'
import type { DsoMetrics } from '../../interfaces/analytics'
import { formatCurrency, type CurrencyCode } from '../../utils/currency'
import { useI18n } from '../../composables/useI18n'

const props = withDefaults(
  defineProps<{
    dso: DsoMetrics
    currency?: CurrencyCode
  }>(),
  {
    currency: 'EUR'
  }
)

const { t } = useI18n()

const progressPercent = computed(() => {
  const range = props.dso.prior_dso_days - props.dso.target_dso_days
  if (range <= 0) return 100
  const gain = props.dso.prior_dso_days - props.dso.current_dso_days
  return Math.min(100, Math.max(10, Math.round((gain / range) * 100)))
})

const formattedCashFreed = computed(() => {
  return formatCurrency(props.dso.cash_freed_eur, props.currency)
})
</script>
