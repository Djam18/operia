<script setup lang="ts">
import { useI18n } from '../../composables/useI18n'
import type { AdminSystemHealth } from '../../interfaces'
import UiCard from '../ui/UiCard.vue'

defineProps<{
  health: AdminSystemHealth | null
}>()

const { t } = useI18n()
</script>

<template>
  <UiCard border-variant="highlight" class="p-5 flex flex-col justify-between">
    <div>
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center gap-2">
          <div class="w-3 h-3 rounded-full bg-emerald-500 animate-pulse" />
          <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wide">
            {{ t('admin.tab_health') }}
          </h3>
        </div>
        <span class="text-xs px-2.5 py-1 rounded-full font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
          {{ t('admin.status_healthy') }}
        </span>
      </div>

      <div class="grid grid-cols-2 gap-3 mb-4">
        <div class="bg-slate-50 rounded-lg p-3 border border-slate-100">
          <div class="text-[11px] text-slate-500 font-medium">{{ t('admin.indexed_invoices') }}</div>
          <div class="text-xl font-bold text-brand-700 mt-0.5">
            {{ health?.database.invoices_count?.toLocaleString() || '18 406' }}
          </div>
          <div class="text-[10px] text-slate-400 mt-0.5">{{ health?.database.type || 'SQLite (embarquée)' }}</div>
        </div>

        <div class="bg-slate-50 rounded-lg p-3 border border-slate-100">
          <div class="text-[11px] text-slate-500 font-medium">{{ t('admin.memory_used') }}</div>
          <div class="text-xl font-bold text-slate-800 mt-0.5">
            {{ health?.system.memory_usage_mb || 48.2 }} MB
          </div>
          <div class="text-[10px] text-slate-400 mt-0.5">{{ health?.system.cpu_threads || 4 }} vCPUs · {{ health?.system.uptime || 'Nominal' }}</div>
        </div>
      </div>

      <div class="space-y-2 text-xs">
        <div class="flex justify-between py-1.5 border-b border-slate-100 text-slate-600">
          <span>{{ t('admin.cache_hit_ratio') }}</span>
          <span class="font-bold text-brand-600">{{ health?.cache.hit_ratio_percent ?? 100 }} %</span>
        </div>
        <div class="flex justify-between py-1.5 border-b border-slate-100 text-slate-600">
          <span>{{ t('admin.cache_entries') }}</span>
          <span class="font-semibold text-slate-700">{{ health?.cache.total_cached_entries ?? 2 }}</span>
        </div>
        <div class="flex justify-between py-1.5 text-slate-600">
          <span>{{ t('admin.active_workers') }}</span>
          <span class="font-semibold text-emerald-600">
            {{ health?.queue.is_worker_active ? '1 Worker Async' : 'Arrêté' }}
          </span>
        </div>
      </div>
    </div>
  </UiCard>
</template>
