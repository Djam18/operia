<template>
  <div class="p-5 rounded-2xl bg-white border border-slate-200/80 shadow-xs flex flex-col gap-4">
    <!-- Header -->
    <div class="flex items-start justify-between">
      <div>
        <div class="flex items-center gap-2">
          <h4 class="text-sm font-bold text-slate-900">{{ t('analytics.pareto_title') }}</h4>
          <span class="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200/60">
            {{ t('analytics.pareto_rule_badge') }}
          </span>
        </div>
        <p class="text-xs text-slate-400 mt-0.5">{{ t('analytics.pareto_sub') }}</p>
      </div>

      <!-- 80% Threshold Badge -->
      <div class="text-right">
        <span class="text-xs font-mono font-bold text-brand-600 bg-brand-50 px-2.5 py-1 rounded-lg border border-brand-100">
          {{ t('analytics.pareto_threshold') }}
        </span>
      </div>
    </div>

    <!-- Deciles Visualization Bars with Cumulative % -->
    <div class="space-y-2.5">
      <div
        v-for="decile in deciles"
        :key="decile.decile_label"
        class="group"
      >
        <div class="flex items-center justify-between text-xs mb-1">
          <span class="font-medium text-slate-700 flex items-center gap-1.5">
            {{ decile.decile_label }}
            <span class="text-[10px] text-slate-400">({{ decile.clients_count }} clients)</span>
          </span>
          <div class="flex items-center gap-3">
            <span class="font-mono text-slate-500">{{ decile.percentage_of_total }}%</span>
            <span class="font-mono font-semibold text-xs" :class="decile.cumulative_percentage <= 80 ? 'text-amber-600' : 'text-slate-700'">
              Cumul: {{ decile.cumulative_percentage }}%
            </span>
          </div>
        </div>

        <div class="relative w-full h-3 bg-slate-100 rounded-full overflow-hidden flex items-center">
          <div
            class="h-full rounded-full transition-all duration-500"
            :class="decile.cumulative_percentage <= 80 ? 'bg-linear-to-r from-amber-500 to-rose-500' : 'bg-slate-300'"
            :style="{ width: `${Math.min(100, decile.cumulative_percentage)}%` }"
          />
          <!-- 80% marker line -->
          <div class="absolute left-[80%] top-0 bottom-0 w-0.5 bg-rose-500/80 z-10" />
        </div>
      </div>
    </div>

    <!-- AI Prescriptive Insight -->
    <div class="p-3 bg-amber-50/60 rounded-xl border border-amber-200/60 flex items-start gap-2.5">
      <Sparkles class="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
      <div class="text-xs text-amber-900 leading-relaxed">
        <span class="font-bold">Constat Data Analyst : </span>
        {{ insight }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Sparkles } from 'lucide-vue-next'
import type { ParetoDecile } from '../../interfaces/analytics'
import { useI18n } from '../../composables/useI18n'

withDefaults(
  defineProps<{
    deciles: ParetoDecile[]
    insight: string
  }>(),
  {
    deciles: () => [],
    insight: 'Concentration élevée du risque sur le premier décile.'
  }
)

const { t } = useI18n()
</script>
