<template>
  <div class="p-8 max-w-6xl mx-auto flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Données</h1>
        <p class="text-sm text-slate-500 mt-0.5">Sources métier accessibles à l'agent, avec leur niveau d'actualisation.</p>
      </div>

      <button @click="onRefresh" :disabled="isRefreshing"
        class="px-4 py-2.5 bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 rounded-xl text-xs font-semibold flex items-center gap-2 shadow-xs transition cursor-pointer">
        <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': isRefreshing }" />
        <span>Actualiser</span>
      </button>
    </div>

    <div class="bg-blue-50/70 border border-blue-200/60 rounded-2xl p-4 flex items-center gap-3 text-xs text-blue-900 font-medium">
      <Database class="w-4 h-4 text-blue-600 shrink-0" />
      <span><strong>{{ displayedSources.length }} sources métier connectées</strong> · 18 406 factures et données CRM synchronisées en direct</span>
    </div>

    <div class="bg-white rounded-2xl border border-slate-200/90 overflow-hidden shadow-xs">
      <div class="p-4 border-b border-slate-100 flex flex-wrap items-center justify-between gap-4">
        <div class="relative flex-1 min-w-[200px] max-w-md">
          <Search class="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
          <input v-model="search" type="text" placeholder="Rechercher une source..."
            class="w-full pl-9 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-brand-500" />
        </div>

        <div class="flex items-center gap-1.5">
          <button v-for="t in ['Tous', 'CRM', 'ERP', 'Base financière', 'Messagerie']" :key="t"
            @click="selectedType = t"
            class="px-2.5 py-1 rounded-lg text-xs font-medium transition cursor-pointer"
            :class="selectedType === t ? 'bg-brand-50 text-brand-700 font-bold border border-brand-200' : 'bg-slate-50 hover:bg-slate-100 text-slate-600 border border-slate-200'">
            {{ t }}
          </button>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-50/80 text-slate-400 font-semibold border-b border-slate-100 uppercase tracking-wider text-[10px]">
            <tr>
              <th class="px-5 py-3">Source</th>
              <th class="px-5 py-3">Type</th>
              <th class="px-5 py-3">Enregistrements</th>
              <th class="px-5 py-3">Mise à jour</th>
              <th class="px-5 py-3 text-right">État</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-slate-700">
            <tr v-for="s in displayedSources" :key="s.id" class="hover:bg-slate-50/50 transition">
              <td class="px-5 py-4 font-bold text-slate-900">{{ s.name }}</td>
              <td class="px-5 py-4 text-slate-500">{{ s.type }}</td>
              <td class="px-5 py-4 font-mono font-medium">{{ s.record_count.toLocaleString('fr-FR') }}</td>
              <td class="px-5 py-4 text-slate-500">{{ s.last_synced_at }}</td>
              <td class="px-5 py-4 text-right">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold"
                  :class="s.status === 'COMPLETED' ? 'bg-emerald-100 text-emerald-800' : 'bg-blue-100 text-blue-800'">
                  <component :is="s.status === 'COMPLETED' ? Check : RefreshCw" class="w-3 h-3" :class="{ 'animate-spin': s.status === 'IN_PROGRESS' }" />
                  {{ s.status === 'COMPLETED' ? 'Terminé' : 'En cours' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="p-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
        <div>{{ displayedSources.length }} résultat(s)</div>
        <div class="flex items-center gap-2">
          <span>Page 1 sur 1</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RefreshCw, Database, Search, Check } from 'lucide-vue-next'
import { useAgentStore } from '../stores/agent'

const store = useAgentStore()
const search = ref<string>('')
const selectedType = ref<string>('Tous')
const isRefreshing = ref<boolean>(false)

onMounted(() => { store.fetchDataSources() })

const defaultSources = [
  { id: 'src-crm', name: 'Clients', type: 'CRM', record_count: 4820, last_synced_at: 'Il y a 4 min', status: 'COMPLETED' as const },
  { id: 'src-fin', name: 'Factures', type: 'Base financière', record_count: 18406, last_synced_at: 'Il y a 2 min', status: 'COMPLETED' as const },
  { id: 'src-erp', name: 'Commandes', type: 'ERP', record_count: 32104, last_synced_at: 'Il y a 12 min', status: 'COMPLETED' as const },
  { id: 'src-msg', name: 'Messages commerciaux', type: 'Messagerie', record_count: 7892, last_synced_at: 'Il y a 1 h', status: 'IN_PROGRESS' as const },
  { id: 'src-ref', name: 'Catalogue produits', type: 'Référentiel', record_count: 684, last_synced_at: 'Hier, 18:10', status: 'COMPLETED' as const },
]

const displayedSources = computed(() => {
  let list = store.dataSources.length ? store.dataSources : defaultSources
  if (selectedType.value !== 'Tous') {
    list = list.filter(s => s.type === selectedType.value)
  }
  if (!search.value) return list
  return list.filter(s => s.name.toLowerCase().includes(search.value.toLowerCase()))
})

async function onRefresh(): Promise<void> {
  isRefreshing.value = true
  await store.refreshDataSources()
  isRefreshing.value = false
}
</script>
