<template>
  <div class="bg-white border border-slate-200/90 rounded-2xl overflow-hidden shadow-xs">
    <div class="px-4 py-3 border-b border-slate-100 flex items-center justify-between text-xs">
      <div class="flex items-center gap-2 font-bold text-slate-900">
        <FileSpreadsheet class="w-4 h-4 text-brand-600" />
        <span>{{ t('agent.invoices_identified', { count: totalCount }) }}</span>
      </div>
      <span class="text-[11px] text-slate-400">{{ t('agent.ordered_by_amount') }}</span>
    </div>

    <div class="divide-y divide-slate-100 text-xs">
      <div
        v-for="inv in invoices"
        :key="inv.id"
        class="px-4 py-3 flex items-center justify-between hover:bg-slate-50/60 transition"
      >
        <div class="flex items-center gap-4">
          <span class="font-bold text-slate-900 w-44 truncate">{{ inv.customer }}</span>
          <span class="text-[11px] font-mono text-slate-400">{{ inv.id }}</span>
          <span v-if="inv.region" class="text-[10px] px-2 py-0.5 rounded-md bg-slate-100 text-slate-600">
            {{ inv.region }}
          </span>
        </div>

        <div class="flex items-center gap-6">
          <span class="font-bold text-slate-900">
            {{ formatCurrency(inv.amount, inv.currency) }}
          </span>
          <span class="text-amber-700 font-semibold text-[11px] w-16 text-right">
            {{ inv.days_overdue }} {{ t('common.days') }}
          </span>
        </div>
      </div>
    </div>

    <div class="px-4 py-2.5 bg-slate-50 border-t border-slate-100 text-right">
      <button
        @click="$emit('toggleShowAll')"
        class="text-xs font-semibold text-brand-600 hover:text-brand-700 cursor-pointer"
      >
        {{ showAll ? t('agent.reduce_invoices') : t('agent.see_all_invoices') }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FileSpreadsheet } from 'lucide-vue-next'
import type { Invoice } from '../../types'
import { formatCurrency } from '../../utils/currency'
import { useI18n } from '../../composables/useI18n'

const { t } = useI18n()

defineProps<{
  invoices: Invoice[]
  totalCount: number
  showAll: boolean
}>()

defineEmits<{
  (e: 'toggleShowAll'): void
}>()
</script>
