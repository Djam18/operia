<template>
  <div class="p-8 max-w-6xl mx-auto flex flex-col gap-6">
    <div>
      <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Historique</h1>
      <p class="text-sm text-slate-500 mt-0.5">Une trace complète, de la demande jusqu'au résultat.</p>
    </div>

    <!-- Lifecycle Process Breadcrumbs -->
    <div class="bg-white border border-slate-200/90 rounded-2xl p-4 flex items-center justify-between text-xs font-semibold shadow-xs">
      <div class="flex items-center gap-2 text-brand-600">
        <span class="w-6 h-6 rounded-full bg-brand-50 flex items-center justify-center font-bold">1</span>
        <span>Requête</span>
      </div>
      <ArrowRight class="w-4 h-4 text-slate-300" />
      <div class="flex items-center gap-2 text-brand-600">
        <span class="w-6 h-6 rounded-full bg-brand-50 flex items-center justify-center font-bold">2</span>
        <span>Analyse</span>
      </div>
      <ArrowRight class="w-4 h-4 text-slate-300" />
      <div class="flex items-center gap-2 text-brand-600">
        <span class="w-6 h-6 rounded-full bg-brand-50 flex items-center justify-center font-bold">3</span>
        <span>Action préparée</span>
      </div>
      <ArrowRight class="w-4 h-4 text-slate-300" />
      <div class="flex items-center gap-2 text-amber-600">
        <span class="w-6 h-6 rounded-full bg-amber-50 flex items-center justify-center font-bold">4</span>
        <span>Validation</span>
      </div>
      <ArrowRight class="w-4 h-4 text-slate-300" />
      <div class="flex items-center gap-2 text-emerald-600">
        <span class="w-6 h-6 rounded-full bg-emerald-50 flex items-center justify-center font-bold">5</span>
        <span>Exécution</span>
      </div>
    </div>

    <div class="bg-white rounded-2xl border border-slate-200/90 overflow-hidden shadow-xs">
      <div class="p-4 border-b border-slate-100 flex flex-wrap items-center justify-between gap-4">
        <div class="relative flex-1 min-w-[200px] max-w-md">
          <Search class="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
          <input v-model="search" type="text" placeholder="Rechercher dans l'historique..."
            class="w-full pl-9 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-brand-500" />
        </div>

        <div class="flex items-center gap-1.5">
          <button v-for="st in statusFilters" :key="st.value" @click="selectedStatus = st.value"
            class="px-2.5 py-1 rounded-lg text-xs font-medium transition cursor-pointer"
            :class="selectedStatus === st.value ? 'bg-brand-50 text-brand-700 font-bold border border-brand-200' : 'bg-slate-50 hover:bg-slate-100 text-slate-600 border border-slate-200'">
            {{ st.label }}
          </button>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-50/80 text-slate-400 font-semibold border-b border-slate-100 uppercase tracking-wider text-[10px]">
            <tr>
              <th class="px-5 py-3">Date</th>
              <th class="px-5 py-3">Utilisateur</th>
              <th class="px-5 py-3">Demande</th>
              <th class="px-5 py-3">Outil</th>
              <th class="px-5 py-3">Action</th>
              <th class="px-5 py-3 text-right">Statut</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-slate-700">
            <tr v-for="item in displayedLogs" :key="item.id" class="hover:bg-slate-50/50 transition">
              <td class="px-5 py-4 text-slate-400 font-medium">{{ item.timestamp }}</td>
              <td class="px-5 py-4 font-bold text-slate-900">{{ item.user }}</td>
              <td class="px-5 py-4 text-slate-800 font-medium">{{ item.query }}</td>
              <td class="px-5 py-4 text-slate-500 font-mono text-[11px]">{{ item.tool }}</td>
              <td class="px-5 py-4 font-medium text-slate-700">{{ item.action }}</td>
              <td class="px-5 py-4 text-right">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold"
                  :class="[
                    item.status === 'PENDING' ? 'bg-amber-100 text-amber-800' :
                    item.status === 'COMPLETED' ? 'bg-emerald-100 text-emerald-800' :
                    'bg-rose-100 text-rose-800'
                  ]">
                  <component :is="item.status === 'PENDING' ? Clock : item.status === 'COMPLETED' ? Check : AlertCircle" class="w-3 h-3" />
                  {{ item.status === 'PENDING' ? 'En attente' : item.status === 'COMPLETED' ? 'Terminé' : 'Échec' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="p-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
        <div>{{ displayedLogs.length }} résultat(s)</div>
        <div>Page 1 sur 1</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ArrowRight, Search, Clock, Check, AlertCircle } from 'lucide-vue-next'
import { useAgentStore } from '../stores/agent'

const store = useAgentStore()
const search = ref<string>('')
const selectedStatus = ref<string>('all')

const statusFilters = [
  { label: 'Tous', value: 'all' },
  { label: 'En attente', value: 'PENDING' },
  { label: 'Terminé', value: 'COMPLETED' },
  { label: 'Échec', value: 'FAILED' },
]

onMounted(() => { store.fetchHistory() })

const defaultLogs = [
  { id: '1', timestamp: '17 sept. · 10:14', user: 'Alex Martin', query: 'Factures > 30 jours', tool: 'Finance + CRM', action: 'Relance email', status: 'PENDING' as const },
  { id: '2', timestamp: '17 sept. · 09:58', user: 'Sophie Bernard', query: 'Clients actifs T3', tool: 'CRM', action: 'Export CSV', status: 'PENDING' as const },
  { id: '3', timestamp: '16 sept. · 16:42', user: 'Marc Leroy', query: 'Résumé du pipeline', tool: 'CRM', action: 'Rapport généré', status: 'COMPLETED' as const },
  { id: '4', timestamp: '16 sept. · 14:20', user: 'Alex Martin', query: 'Commandes en retard', tool: 'ERP', action: 'Analyse', status: 'COMPLETED' as const },
  { id: '5', timestamp: '15 sept. · 11:06', user: 'Sophie Bernard', query: 'Contacts sans activité', tool: 'CRM', action: 'Liste segmentée', status: 'FAILED' as const },
]

const displayedLogs = computed(() => {
  let list = store.historyLogs.length ? store.historyLogs : defaultLogs
  if (selectedStatus.value !== 'all') {
    list = list.filter(l => l.status === selectedStatus.value)
  }
  if (!search.value) return list
  const q = search.value.toLowerCase()
  return list.filter(l =>
    l.user.toLowerCase().includes(q) ||
    l.query.toLowerCase().includes(q) ||
    l.action.toLowerCase().includes(q)
  )
})
</script>
