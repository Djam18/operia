<template>
  <div class="bg-white rounded-2xl border border-amber-200/80 p-6 shadow-xs flex flex-col justify-between">
    <div>
      <div class="flex items-center gap-2 text-amber-900 text-xs font-bold uppercase tracking-wider mb-4">
        <Clock class="w-4 h-4 text-amber-600" />
        <span>{{ t('dashboard.pending_badge') }}</span>
      </div>
      <div class="text-xs text-slate-500 mb-4">{{ t('dashboard.pending_banner_sub') }}</div>

      <div class="p-4 rounded-xl border border-slate-100 bg-slate-50/50 mb-4">
        <div class="text-xs font-bold text-slate-900 mb-1">{{ title || t('dashboard.pending_action_default_title') }}</div>
        <div class="text-[11px] text-slate-500 mb-3">
          {{ t('dashboard.pending_action_sub', { count: targetCount || 8, amount: formattedAmount }) }}
        </div>

        <div class="p-2.5 rounded-lg bg-amber-50 border border-amber-200/60 text-[11px] text-amber-900 font-medium leading-relaxed">
          <strong>{{ t('operations.consequence_label') }}</strong> {{ t('dashboard.consequence_sample') }}
        </div>
      </div>
    </div>

    <div class="flex items-center gap-2 pt-2">
      <router-link
        to="/operations"
        class="flex-1 py-2 text-center text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition cursor-pointer"
      >
        {{ t('common.details') }}
      </router-link>
      <router-link
        to="/agent"
        class="flex-1 py-2 text-center text-xs font-semibold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow-xs transition cursor-pointer"
      >
        {{ t('common.examine') }}
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Clock } from 'lucide-vue-next'
import { formatCurrency } from '../../utils/currency'
import { useI18n } from '../../composables/useI18n'

const { t } = useI18n()

const props = withDefaults(
  defineProps<{
    title?: string
    targetCount?: number
    financialAmount?: number
    currency?: string
  }>(),
  {
    financialAmount: 42680,
    currency: 'EUR',
  }
)

const formattedAmount = computed(() => formatCurrency(props.financialAmount, props.currency))
</script>
