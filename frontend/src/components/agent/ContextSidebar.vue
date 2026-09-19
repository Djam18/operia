<template>
  <div class="w-64 border-l border-slate-200 bg-white p-5 flex flex-col gap-6 shrink-0 hidden xl:flex">
    <div>
      <h3 class="text-xs font-bold text-slate-900 mb-4">{{ t('agent.work_context') }}</h3>
      <div class="space-y-3">
        <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">{{ t('agent.active_sources') }}</div>

        <div class="flex items-center justify-between text-xs text-slate-700">
          <div class="flex items-center gap-2">
            <Database class="w-3.5 h-3.5 text-slate-400" />
            <span>{{ t('agent.database') }}</span>
          </div>
          <Check class="w-4 h-4 text-emerald-600" />
        </div>

        <div class="flex items-center justify-between text-xs text-slate-700">
          <div class="flex items-center gap-2">
            <Users class="w-3.5 h-3.5 text-slate-400" />
            <span>{{ t('agent.crm_clients') }}</span>
          </div>
          <Check class="w-4 h-4 text-emerald-600" />
        </div>

        <div class="flex items-center justify-between text-xs text-slate-700">
          <div class="flex items-center gap-2">
            <Mail class="w-3.5 h-3.5 text-slate-400" />
            <span>{{ t('agent.messaging') }}</span>
          </div>
          <Check class="w-4 h-4 text-emerald-600" />
        </div>
      </div>
    </div>

    <div class="border-t border-slate-100 pt-5 space-y-3">
      <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">{{ t('agent.scope') }}</div>
      <div class="text-xs font-bold text-slate-900">
        {{ selectedRegion === 'Toutes' ? t('agent.scope_international') : t('agent.scope_prefix', { region: selectedRegion }) }}
      </div>
      <div class="text-[11px] text-slate-400 flex items-center gap-1.5">
        <Clock class="w-3 h-3" />
        <span>{{ t('agent.updated_ago') }}</span>
      </div>
    </div>

    <div class="border-t border-slate-100 pt-5 space-y-2">
      <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">{{ t('agent.mcp_perf') }}</div>
      <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-100 text-[11px] font-mono text-slate-600 space-y-1">
        <div>{{ t('agent.mcp_sql_query') }} <strong class="text-emerald-700 font-bold">12ms</strong></div>
        <div>{{ t('agent.mcp_index_lookup') }} <strong class="text-emerald-700 font-bold">18ms</strong></div>
        <div>{{ t('agent.mcp_volume_records', { count: '18 406' }) }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Database, Users, Mail, Check, Clock } from 'lucide-vue-next'
import { useI18n } from '../../composables/useI18n'

const { t } = useI18n()

defineProps<{
  selectedRegion: string
}>()
</script>
