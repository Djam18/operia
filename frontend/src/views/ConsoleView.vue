<template>
  <div class="min-h-screen bg-[#070A0F] text-slate-200 font-sans text-xs flex flex-col selection:bg-cyan-500 selection:text-black">
    <ConsoleHeader />

    <div class="px-8 py-6 border-b border-slate-800/60 flex items-start justify-between bg-[#090D14]">
      <div class="max-w-3xl">
        <h1 class="text-xl font-bold text-white tracking-tight mb-1">Console d'interrogation</h1>
        <p class="text-xs text-slate-400 leading-relaxed">
          Posez vos questions métier en langage naturel. Atlas prépare les relances, exports et résumés, puis attend votre validation avant toute action sensible.
        </p>
      </div>

      <div class="flex items-center gap-4">
        <div class="border border-slate-800 bg-[#0E131F] px-5 py-3 rounded-xl">
          <div class="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Requêtes traitées</div>
          <div class="text-2xl font-black text-white mt-0.5">{{ store.dashboardStats?.queries_count || 148 }}</div>
        </div>
        <div class="border border-slate-800 bg-[#0E131F] px-5 py-3 rounded-xl">
          <div class="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Actions validées</div>
          <div class="text-2xl font-black text-white mt-0.5">{{ store.dashboardStats?.completed_count || 35 }}</div>
        </div>
      </div>
    </div>

    <div class="flex-1 p-8 grid grid-cols-12 gap-6 overflow-hidden">
      <ConsoleDataScope />
      <ConsoleExecutionFeed />
      <ConsoleStagedPanel />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import ConsoleHeader from '../components/console/ConsoleHeader.vue'
import ConsoleDataScope from '../components/console/ConsoleDataScope.vue'
import ConsoleExecutionFeed from '../components/console/ConsoleExecutionFeed.vue'
import ConsoleStagedPanel from '../components/console/ConsoleStagedPanel.vue'
import { useAgentStore } from '../stores/agent'

const store = useAgentStore()
onMounted(() => {
  store.fetchDashboardStats()
})
</script>
