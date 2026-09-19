<template>
  <div class="col-span-3 border border-slate-800/90 rounded-2xl p-5 bg-[#0D121D] flex flex-col gap-4">
    <div class="flex items-center justify-between border-b border-slate-800 pb-3">
      <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400">{{ t('console.validation_queue') }}</div>
      <span class="text-amber-400 font-semibold text-[11px]">{{ pendingOps.length }} {{ t('operations.tab_pending').toLowerCase() }}</span>
    </div>

    <div class="space-y-4 overflow-y-auto">
      <div v-if="pendingOps.length === 0" class="p-6 text-center text-slate-500 font-mono text-xs">
        Aucune action en attente.
      </div>
      <div v-for="op in pendingOps" :key="op.action_id" class="p-4 rounded-xl bg-[#111726] border border-slate-800 space-y-2">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-1.5">
            <span class="px-2 py-0.5 rounded-md bg-slate-800 text-[10px] text-slate-300 font-semibold">{{ op.action_type }}</span>
            <span class="px-2 py-0.5 rounded-md bg-rose-950/80 text-rose-400 text-[10px] font-semibold">{{ op.criticality }}</span>
          </div>
          <span class="text-[10px] text-amber-400 font-semibold">PENDING</span>
        </div>

        <div class="font-bold text-white text-xs">{{ op.title }}</div>
        <div class="text-[10px] text-slate-400 leading-tight">{{ op.description }}</div>

        <div class="font-mono text-[10px] text-slate-400 space-y-0.5 pt-1">
          <div>Cible : {{ op.target_count }} contact(s) · {{ op.channel }}</div>
          <div class="text-rose-400">{{ op.consequence_warning }}</div>
        </div>

        <div class="flex items-center gap-2 pt-2">
          <button @click="store.validateOperation(op.action_id)"
            class="flex-1 py-1.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black font-bold text-xs transition cursor-pointer">
            {{ t('operations.validate_and_execute') }}
          </button>
          <button @click="store.refuseOperation(op.action_id)"
            class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs transition cursor-pointer">
            {{ t('operations.refuse') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useI18n } from '../../composables/useI18n'
import { useAgentStore } from '../../stores/agent'

const { t } = useI18n()
const store = useAgentStore()

onMounted(() => {
  store.fetchOperations()
})

const pendingOps = computed(() => store.operations.filter(o => o.status === 'PENDING'))
</script>
