<template>
  <div class="w-full flex flex-col gap-2">
    <div class="flex items-center justify-between text-xs">
      <span class="font-bold text-slate-900">
        {{ t('analytics.total_recovered') }} : {{ formattedTotal }}
      </span>
      <span class="text-emerald-600 font-semibold">{{ t('analytics.recovered_growth') }}</span>
    </div>

    <!-- SVG Area Spline Chart -->
    <div class="relative w-full h-44 bg-slate-50/50 rounded-xl border border-slate-100 p-2 overflow-hidden">
      <svg class="w-full h-full" viewBox="0 0 500 150" preserveAspectRatio="none">
        <defs>
          <linearGradient id="cashflowGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#4f46e5" stop-opacity="0.35" />
            <stop offset="100%" stop-color="#4f46e5" stop-opacity="0.0" />
          </linearGradient>
        </defs>

        <line x1="0" y1="35" x2="500" y2="35" stroke="#e2e8f0" stroke-dasharray="4" stroke-width="1" />
        <line x1="0" y1="75" x2="500" y2="75" stroke="#e2e8f0" stroke-dasharray="4" stroke-width="1" />
        <line x1="0" y1="115" x2="500" y2="115" stroke="#e2e8f0" stroke-dasharray="4" stroke-width="1" />

        <polygon
          points="0,140 0,110 80,105 160,85 240,90 320,60 400,45 500,20 500,140"
          fill="url(#cashflowGrad)"
        />

        <polyline
          points="0,110 80,105 160,85 240,90 320,60 400,45 500,20"
          fill="none"
          stroke="#4f46e5"
          stroke-width="3"
          stroke-linecap="round"
          stroke-linejoin="round"
        />

        <circle cx="80" cy="105" r="4" fill="#ffffff" stroke="#4f46e5" stroke-width="2" />
        <circle cx="160" cy="85" r="4" fill="#ffffff" stroke="#4f46e5" stroke-width="2" />
        <circle cx="240" cy="90" r="4" fill="#ffffff" stroke="#4f46e5" stroke-width="2" />
        <circle cx="320" cy="60" r="4" fill="#ffffff" stroke="#4f46e5" stroke-width="2" />
        <circle cx="400" cy="45" r="4" fill="#ffffff" stroke="#4f46e5" stroke-width="2" />
        <circle cx="500" cy="20" r="5" fill="#4f46e5" stroke="#ffffff" stroke-width="2" />
      </svg>
    </div>

    <!-- X-Axis Labels -->
    <div class="flex items-center justify-between text-[10px] text-slate-400 font-medium px-1">
      <span>{{ t('analytics.week_1') }}</span>
      <span>{{ t('analytics.week_2') }}</span>
      <span>{{ t('analytics.week_3') }}</span>
      <span>{{ t('analytics.week_4') }}</span>
      <span>{{ t('analytics.week_5') }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { formatCurrency } from '../../utils/currency'
import { useI18n } from '../../composables/useI18n'

const { t } = useI18n()

const props = withDefaults(
  defineProps<{
    totalRecovered?: number
    currency?: string
  }>(),
  {
    totalRecovered: 86420,
    currency: 'EUR',
  }
)

const formattedTotal = computed(() => {
  return formatCurrency(props.totalRecovered, props.currency)
})
</script>
