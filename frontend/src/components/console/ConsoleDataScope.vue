<template>
  <div class="col-span-3 flex flex-col gap-5">
    <div class="border border-slate-800/90 rounded-2xl p-5 bg-[#0D121D] flex flex-col gap-4">
      <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400">{{ t('console.data_perimeter') }}</div>

      <div class="space-y-3">
        <div class="p-3 rounded-xl bg-[#111726] border border-slate-800">
          <div class="flex items-center gap-2 font-bold text-white">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            <span>{{ t('console.source_erp') }}</span>
          </div>
          <div class="text-[11px] text-slate-400 mt-0.5">{{ t('console.read_only') }}</div>
        </div>

        <div class="p-3 rounded-xl bg-[#111726] border border-slate-800">
          <div class="flex items-center gap-2 font-bold text-white">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            <span>{{ t('console.source_crm') }}</span>
          </div>
          <div class="text-[11px] text-slate-400 mt-0.5">{{ t('console.read_only') }}</div>
        </div>

        <div class="p-3 rounded-xl bg-[#111726] border border-slate-800">
          <div class="flex items-center gap-2 font-bold text-white">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            <span>{{ t('console.source_warehouse') }}</span>
          </div>
          <div class="text-[11px] text-slate-400 mt-0.5">{{ t('console.read_only') }}</div>
        </div>

        <div class="p-3 rounded-xl bg-[#111726] border border-slate-800">
          <div class="flex items-center gap-2 font-bold text-amber-400">
            <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
            <span>{{ t('console.source_outbound_msg') }}</span>
          </div>
          <div class="text-[11px] text-slate-400 mt-0.5">{{ t('console.write_validation_req') }}</div>
        </div>
      </div>

      <div class="text-[11px] text-slate-500 leading-relaxed pt-1">
        {{ t('console.guardrail_notice') }}
      </div>
    </div>

    <!-- Questions Fréquentes -->
    <div class="border border-slate-800/90 rounded-2xl p-5 bg-[#0D121D] flex flex-col gap-3">
      <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400">{{ t('console.faq_title') }}</div>
      <button @click="router.push({ path: '/agent', query: { prompt: t('console.faq_overdue_clients') } })"
        class="text-left p-3 rounded-xl bg-[#111726] hover:bg-[#161E31] border border-slate-800 text-slate-300 transition text-[11px] cursor-pointer">
        {{ t('console.faq_overdue_clients') }}
      </button>
      <button @click="router.push({ path: '/agent', query: { prompt: t('console.faq_margin_summary') } })"
        class="text-left p-3 rounded-xl bg-[#111726] hover:bg-[#161E31] border border-slate-800 text-slate-300 transition text-[11px] cursor-pointer">
        {{ t('console.faq_margin_summary') }}
      </button>
      <button @click="router.push({ path: '/agent', query: { prompt: t('console.faq_blocked_orders') } })"
        class="text-left p-3 rounded-xl bg-[#111726] hover:bg-[#161E31] border border-slate-800 text-slate-300 transition text-[11px] cursor-pointer">
        {{ t('console.faq_blocked_orders') }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useI18n } from '../../composables/useI18n'

const { t } = useI18n()
const router = useRouter()
</script>
