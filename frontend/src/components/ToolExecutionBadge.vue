<template>
  <div class="border border-slate-200 bg-white rounded-xl overflow-hidden my-3 shadow-xs">
    <button
      @click="isOpen = !isOpen"
      class="w-full px-4 py-2.5 flex items-center justify-between text-xs font-medium text-slate-700 hover:bg-slate-50 transition cursor-pointer"
    >
      <div class="flex items-center gap-2">
        <Wrench class="w-3.5 h-3.5 text-slate-400" />
        <span>{{ t('agent.tools_used') }} <strong class="font-semibold text-slate-900">{{ title || 'ERP + CRM' }}</strong></span>
      </div>
      <div class="flex items-center gap-2">
        <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700">
          <CheckCircle2 class="w-3 h-3" />
          <span class="sr-only">Completed</span>
          <span>{{ status || t('operations.tab_completed') }}</span>
        </span>
        <ChevronDown class="w-4 h-4 text-slate-400 transition transform" :class="{ 'rotate-180': isOpen }" />
      </div>
    </button>

    <div v-if="isOpen" class="px-4 py-3 border-t border-slate-100 bg-slate-50 flex flex-col gap-2 font-mono text-[11px]">
      <template v-if="tools && tools.length > 0">
        <div v-for="(t_item, idx) in tools" :key="idx" class="border-b border-slate-100 pb-2 last:border-0 last:pb-0">
          <div class="flex items-center justify-between text-slate-700 font-semibold">
            <span>▸ {{ t_item.tool }}</span>
            <div class="flex items-center gap-2">
              <span :class="t_item.status === 'ok' ? 'text-emerald-600' : 'text-amber-600'">{{ t_item.status }}</span>
              <span v-if="t_item.duration_ms" class="text-slate-400">·</span>
              <span v-if="t_item.duration_ms">{{ t_item.duration_ms }}ms</span>
            </div>
          </div>
          <div v-if="t_item.summary" class="text-[10px] text-slate-500 pl-3 mt-0.5">
            {{ t_item.summary }}
          </div>
        </div>
      </template>

      <template v-else>
        <div class="flex items-center justify-between text-slate-600">
          <span>{{ t('agent.tool_erp_indexed') }}</span>
          <div class="flex items-center gap-2">
            <span class="text-emerald-600 font-bold">ok</span>
            <span class="text-slate-400">·</span>
            <span>12ms</span>
          </div>
        </div>
        <div class="text-[10px] text-slate-500 pl-3">
          {{ t('agent.tool_erp_params') }}
        </div>

        <div class="border-t border-slate-200/60 my-1"></div>

        <div class="flex items-center justify-between text-slate-600">
          <span>▸ crm.comptes.enrich</span>
          <div class="flex items-center gap-2">
            <span class="text-amber-600 font-bold">partial</span>
            <span class="text-slate-400">·</span>
            <span>18ms</span>
          </div>
        </div>
        <div class="text-[10px] text-slate-500 pl-3">
          {{ t('agent.tool_crm_enrich') }}
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Wrench, CheckCircle2, ChevronDown } from 'lucide-vue-next'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()

defineProps<{
  title?: string
  status?: string
  tools?: Array<any>
}>()

const isOpen = ref<boolean>(false)
</script>
