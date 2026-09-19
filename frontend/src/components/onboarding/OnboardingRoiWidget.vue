<template>
  <div class="space-y-4 p-5 rounded-2xl bg-gradient-to-br from-brand-50/50 to-indigo-50/30 border border-brand-100">
    <div class="flex items-center justify-between">
      <div class="text-xs font-bold uppercase tracking-wider text-brand-700">
        {{ t('onboarding.roi_simulator_title') }}
      </div>
      <!-- Currency selector pill buttons -->
      <div class="flex items-center gap-1 bg-white/80 p-0.5 rounded-lg border border-brand-200/60">
        <button
          v-for="code in availableCurrencies"
          :key="code"
          @click="selectCurrency(code)"
          type="button"
          class="px-2 py-0.5 text-[10px] font-bold rounded-md transition cursor-pointer"
          :class="activeCurrency === code ? 'bg-brand-600 text-white shadow-2xs' : 'text-slate-500 hover:text-slate-800'"
        >
          {{ CURRENCY_PRESETS[code].symbol }}
        </button>
      </div>
    </div>

    <!-- Sliders -->
    <div class="space-y-3">
      <div>
        <div class="flex items-center justify-between text-xs text-slate-700 font-medium mb-1">
          <span>{{ t('onboarding.invoices_per_month') }}</span>
          <span class="font-bold text-brand-700 font-mono">{{ monthlyInvoices.toLocaleString() }}</span>
        </div>
        <input
          v-model.number="monthlyInvoices"
          type="range"
          min="50"
          max="2500"
          step="50"
          class="w-full accent-brand-600 cursor-pointer h-1.5 bg-slate-200 rounded-lg"
        />
      </div>

      <div>
        <div class="flex items-center justify-between text-xs text-slate-700 font-medium mb-1">
          <span>{{ t('onboarding.avg_amount_per_invoice') }}</span>
          <span class="font-bold text-brand-700 font-mono">{{ formatCurrency(avgAmount, activeCurrency) }}</span>
        </div>
        <input
          v-model.number="avgAmount"
          type="range"
          :min="currentPreset.min"
          :max="currentPreset.max"
          :step="currentPreset.step"
          class="w-full accent-brand-600 cursor-pointer h-1.5 bg-slate-200 rounded-lg"
        />
      </div>
    </div>

    <!-- Live Calculated Results -->
    <div class="grid grid-cols-2 gap-3 pt-2">
      <div class="p-3 bg-white rounded-xl border border-brand-200/60 shadow-2xs">
        <div class="text-[10px] text-slate-400 uppercase font-semibold">{{ t('onboarding.operator_time_saved') }}</div>
        <div class="text-xl font-black text-slate-900 mt-0.5">{{ hoursSaved }} {{ t('onboarding.hours_per_month') }}</div>
        <div class="text-[10px] text-emerald-600 font-medium mt-0.5">≈ {{ fteEquiv }} {{ t('onboarding.fte_reallocated') }}</div>
      </div>

      <div class="p-3 bg-white rounded-xl border border-brand-200/60 shadow-2xs">
        <div class="text-[10px] text-slate-400 uppercase font-semibold">{{ t('onboarding.unlocked_cashflow') }}</div>
        <div class="text-xl font-black text-brand-700 mt-0.5">{{ formatCurrency(recoveredCash, activeCurrency) }}</div>
        <div class="text-[10px] text-emerald-600 font-medium mt-0.5">{{ t('onboarding.dso_acceleration') }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { CURRENCY_PRESETS, formatCurrency, type CurrencyCode } from '../../utils/currency'
import { useI18n } from '../../composables/useI18n'

const { t } = useI18n()

const availableCurrencies: CurrencyCode[] = ['EUR', 'XOF', 'MAD', 'KES']
const activeCurrency = ref<CurrencyCode>('EUR')

const currentPreset = computed(() => CURRENCY_PRESETS[activeCurrency.value])

const monthlyInvoices = ref<number>(450)
const avgAmount = ref<number>(CURRENCY_PRESETS.EUR.typicalAvg)

function selectCurrency(code: CurrencyCode): void {
  activeCurrency.value = code
  avgAmount.value = CURRENCY_PRESETS[code].typicalAvg
}

const hoursSaved = computed(() => {
  return Math.round((monthlyInvoices.value * 12) / 60)
})

const fteEquiv = computed(() => {
  return (hoursSaved.value / 140).toFixed(1)
})

const recoveredCash = computed(() => {
  const totalVolume = monthlyInvoices.value * avgAmount.value
  return Math.round(totalVolume * 0.18)
})
</script>
