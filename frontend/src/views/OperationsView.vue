<template>
  <div class="p-8 max-w-6xl mx-auto flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">{{ t('operations.title') }}</h1>
        <p class="text-sm text-slate-500 mt-0.5">{{ t('operations.subtitle') }}</p>
      </div>
      <button v-if="activeTab !== 'outbox'" @click="onBatchValidate" :disabled="selectedIds.length === 0"
        class="px-5 py-2.5 bg-brand-600 hover:bg-brand-700 disabled:opacity-50 text-white rounded-xl text-sm font-semibold flex items-center gap-2 shadow-sm transition cursor-pointer">
        <CheckSquare class="w-4 h-4" />
        <span>{{ t('operations.validate_selection') }} ({{ selectedIds.length }})</span>
      </button>
    </div>

    <div class="flex items-center gap-2">
      <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
        class="px-4 py-2 rounded-xl text-xs font-semibold transition cursor-pointer"
        :class="[activeTab === tab.id ? 'bg-brand-600 text-white shadow-xs' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200']">
        {{ tab.label }} <span v-if="tab.count !== undefined" class="ml-1 opacity-80">({{ tab.count }})</span>
      </button>
    </div>

    <OperationsOutboxList v-if="activeTab === 'outbox'" :emails="store.outboxEmails" />

    <div v-else class="bg-white rounded-2xl border border-slate-200/90 divide-y divide-slate-100 shadow-xs overflow-hidden">
      <div v-for="op in filteredOperations" :key="op.action_id" class="p-5 hover:bg-slate-50/50 transition">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <input v-if="op.status === 'PENDING'" type="checkbox" :value="op.action_id" v-model="selectedIds"
              class="w-4 h-4 rounded text-brand-600 focus:ring-brand-500 border-slate-300 cursor-pointer" />
            <div v-else class="w-4" />
            <div>
              <div class="flex items-center gap-2 mb-1">
                <span class="font-bold text-slate-900 text-sm">{{ op.title }}</span>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold"
                  :class="op.criticality === 'SENSITIVE' ? 'bg-amber-50 text-amber-700 border border-amber-200' : 'bg-slate-100 text-slate-600'">
                  {{ op.criticality === 'SENSITIVE' ? t('operations.sensitive') : t('operations.standard') }}
                </span>
              </div>
              <div class="text-xs text-slate-500">{{ op.description }}</div>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <template v-if="op.status === 'PENDING'">
              <button @click="store.validateOperation(op.action_id)"
                class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-semibold flex items-center gap-1 transition cursor-pointer">
                <Check class="w-3.5 h-3.5" /> <span>Valider</span>
              </button>
              <button @click="store.refuseOperation(op.action_id)"
                class="px-3 py-1.5 bg-slate-100 hover:bg-rose-50 hover:text-rose-600 text-slate-600 rounded-lg text-xs font-semibold transition cursor-pointer">
                <span>Refuser</span>
              </button>
            </template>
            <span v-else class="px-2.5 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5"
              :class="op.status === 'COMPLETED' ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'">
              <component :is="op.status === 'COMPLETED' ? Check : AlertCircle" class="w-3.5 h-3.5" />
              {{ op.status === 'COMPLETED' ? t('operations.tab_completed') : t('operations.refuse') }}
            </span>
            <button @click="expandedId = expandedId === op.action_id ? null : op.action_id"
              class="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition cursor-pointer" title="Détails">
              <ChevronDown class="w-4 h-4 transition-transform" :class="{ 'rotate-180': expandedId === op.action_id }" />
            </button>
          </div>
        </div>

        <div v-if="expandedId === op.action_id" class="mt-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200/80 text-xs text-slate-600 space-y-1">
          <div class="font-medium text-slate-900">Avertissement : {{ op.consequence_warning }}</div>
          <div v-if="op.financial_amount" class="text-brand-700 font-semibold">Montant concerné : {{ op.financial_amount.toLocaleString('fr-FR') }} {{ op.currency || 'EUR' }}</div>
          <div>Canal : {{ op.channel }} · Cibles : {{ op.target_count }} contact(s)</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { CheckSquare, Check, AlertCircle, ChevronDown } from 'lucide-vue-next'
import { useAgentStore } from '../stores/agent'
import { useI18n } from '../composables/useI18n'
import type { StagedAction } from '../types'
import OperationsOutboxList from '../components/operations/OperationsOutboxList.vue'

const { t } = useI18n()
const store = useAgentStore()
const activeTab = ref<'all' | 'pending' | 'completed' | 'outbox'>('all')
const selectedIds = ref<string[]>([])
const expandedId = ref<string | null>(null)

onMounted(() => { store.fetchOperations(); store.fetchOutbox() })

const tabs = computed(() => [
  { id: 'all' as const, label: t('operations.tab_all'), count: store.operations.length },
  { id: 'pending' as const, label: t('operations.tab_pending'), count: store.pendingCount },
  { id: 'completed' as const, label: t('operations.tab_completed') },
  { id: 'outbox' as const, label: "Boîte d'envoi locale", count: store.outboxEmails.length },
])

const filteredOperations = computed<StagedAction[]>(() => {
  if (activeTab.value === 'pending') return store.operations.filter(o => o.status === 'PENDING')
  if (activeTab.value === 'completed') return store.operations.filter(o => o.status === 'COMPLETED')
  return store.operations
})

async function onBatchValidate(): Promise<void> {
  if (selectedIds.value.length === 0) return
  await store.batchValidate(selectedIds.value)
  selectedIds.value = []
  await store.fetchOutbox()
}
</script>
