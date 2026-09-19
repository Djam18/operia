<template>
  <div class="col-span-6 border border-slate-800/90 rounded-2xl p-6 bg-[#0D121D] flex flex-col justify-between">
    <div class="flex items-center justify-between border-b border-slate-800/80 pb-4 mb-4">
      <div class="flex items-center gap-2 font-bold text-slate-300 uppercase tracking-wider text-[10px]">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        <span>{{ t('console.nl_query_title') }}</span>
      </div>
      <span class="text-slate-500 font-mono text-[10px]">session #4821</span>
    </div>

    <div class="space-y-4 overflow-y-auto pr-1">
      <div class="flex justify-end">
        <div class="bg-[#192338] border border-slate-700/60 p-3.5 rounded-xl max-w-md text-white text-xs">
          {{ t('console.chat_query_1') }}
        </div>
      </div>

      <div class="space-y-2 font-mono text-[11px]">
        <div class="bg-[#090D15] border border-slate-800/80 p-3 rounded-xl text-slate-300">
          <div class="flex items-center justify-between">
            <span class="text-cyan-400">▸ erp.factures.query</span>
            <span class="text-emerald-400">ok · 142ms</span>
          </div>
          <div class="text-[10px] text-slate-500 mt-1">{{ t('console.mcp_trace_erp') }}</div>
        </div>

        <div class="bg-[#090D15] border border-slate-800/80 p-3 rounded-xl text-slate-300">
          <div class="flex items-center justify-between">
            <span class="text-cyan-400">▸ crm.comptes.enrich</span>
            <span class="text-amber-400">partial · 210ms</span>
          </div>
          <div class="text-[10px] text-slate-500 mt-1">{{ t('console.mcp_trace_crm') }}</div>
        </div>
      </div>

      <div class="text-slate-200 text-xs leading-relaxed bg-[#0F1626] p-4 rounded-xl border border-slate-800">
        {{ t('console.chat_response_1', { amount: formatCurrency(84210, 'EUR') }) }}
      </div>

      <div class="flex justify-end">
        <div class="bg-[#192338] border border-slate-700/60 p-3.5 rounded-xl max-w-md text-white text-xs">
          {{ t('console.chat_query_2') }}
        </div>
      </div>

      <div class="text-slate-200 text-xs leading-relaxed bg-[#0F1626] p-4 rounded-xl border border-slate-800 space-y-2">
        <p>{{ t('console.chat_response_2') }}</p>
        <div class="p-2 rounded-lg bg-[#070A0F] border border-amber-500/30 text-amber-400 font-mono text-[11px]">
          {{ t('console.chat_action_staged') }}
        </div>
      </div>
    </div>

    <div class="pt-4 border-t border-slate-800/80 mt-4">
      <input
        v-model="inputQuery"
        @keydown.enter="submitQuery"
        type="text"
        :placeholder="t('console.input_placeholder')"
        class="w-full bg-[#080C14] border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white placeholder:text-slate-500 focus:outline-none focus:border-cyan-500"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from '../../composables/useI18n'
import { formatCurrency } from '../../utils/currency'

const { t } = useI18n()
const router = useRouter()
const inputQuery = ref('')

function submitQuery(): void {
  const q = inputQuery.value.trim()
  if (!q) return
  router.push({ path: '/agent', query: { prompt: q } })
}
</script>
