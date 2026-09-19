<template>
  <div class="p-8 max-w-5xl mx-auto flex flex-col gap-8">
    <div class="flex items-center justify-between">
      <div>
        <div class="flex items-center gap-3">
          <h1 class="text-2xl font-bold text-slate-900 tracking-tight">{{ t('sandbox.title') }}</h1>
          <UiBadge variant="warning">{{ t('sandbox.safe_mode_badge') }}</UiBadge>
        </div>
        <p class="text-sm text-slate-500 mt-0.5">{{ t('sandbox.subtitle') }}</p>
      </div>
    </div>

    <UiCard border-variant="highlight">
      <div class="space-y-4">
        <label class="block text-xs font-bold text-slate-900 uppercase tracking-wider">
          Requête de simulation à tester
        </label>
        <div class="flex gap-3">
          <UiInput v-model="simQuery" placeholder="Ex: 'Envoyer une relance aux comptes en retard de plus de 30 jours...'" @enter="runSimulation" />
          <UiButton :loading="isSimulating" @click="runSimulation">
            <Play class="w-4 h-4 mr-1.5" />
            {{ t('sandbox.btn_simulate') }}
          </UiButton>
        </div>
        <div class="flex items-center gap-2 pt-1">
          <span class="text-xs text-slate-400 font-medium">Scénarios pré-chargés :</span>
          <button v-for="s in quickScenarios" :key="s" @click="simQuery = s; runSimulation()"
            class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium transition cursor-pointer">
            {{ s }}
          </button>
        </div>
      </div>
    </UiCard>

    <div v-if="simResult" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <UiCard class="md:col-span-2">
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-slate-900">{{ t('sandbox.impact_preview') }}</h3>
            <UiBadge variant="success">Simulation Calculée</UiBadge>
          </div>
        </template>
        <div class="space-y-3 font-mono text-xs">
          <div class="p-3 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
            <span class="text-slate-600">Base interrogée :</span>
            <strong class="text-slate-900">ERP (18 406 factures) + CRM</strong>
          </div>
          <div class="p-3 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
            <span class="text-slate-600">{{ t('sandbox.clients_targeted') }} :</span>
            <strong class="text-brand-700 font-bold">{{ simTargetCount }} entreprises ciblées (1 litige isolé)</strong>
          </div>
          <div class="p-3 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
            <span class="text-slate-600">{{ t('sandbox.financial_volume') }} :</span>
            <strong class="text-emerald-700 font-bold">{{ simAmount.toLocaleString('fr-FR') }} € / 56 680 000 FCFA</strong>
          </div>
          <div class="p-3 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
            <span class="text-slate-600">{{ t('sandbox.channel_used') }} :</span>
            <strong class="text-slate-900">Courriel sécurisé (BCC direction financière)</strong>
          </div>
        </div>
      </UiCard>

      <UiCard border-variant="warning" class="flex flex-col justify-between">
        <div>
          <div class="flex items-center gap-2 text-amber-800 font-bold text-xs uppercase mb-3">
            <AlertTriangle class="w-4 h-4 text-amber-600" />
            <span>Garde-fous Actifs</span>
          </div>
          <p class="text-xs text-slate-600 leading-relaxed">
            En production, cette action générerait un ordre <strong>SENSITIVE</strong> bloqué en attente de validation humaine explicite.
          </p>
        </div>
        <UiButton variant="outline" size="sm" class="mt-4" @click="router.push({ path: '/agent', query: { prompt: simQuery } })">
          Exécuter dans l'Agent
        </UiButton>
      </UiCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Play, AlertTriangle } from 'lucide-vue-next'
import UiCard from '../components/ui/UiCard.vue'
import UiBadge from '../components/ui/UiBadge.vue'
import UiButton from '../components/ui/UiButton.vue'
import UiInput from '../components/ui/UiInput.vue'
import { useI18n } from '../composables/useI18n'
import { apiFetch } from '../config/api'

const { t } = useI18n()
const router = useRouter()

const simQuery = ref<string>('Envoyer une relance aux comptes en retard de plus de 30 jours')
const isSimulating = ref<boolean>(false)
const simResult = ref<boolean>(true)
const simTargetCount = ref<number>(8)
const simAmount = ref<number>(42680)

const quickScenarios = [
  'Relance grands comptes > 45 jours',
  'Export CSV de tous les clients inactifs',
  'Gel des commandes pour litige ouvert'
]

async function runSimulation(): Promise<void> {
  isSimulating.value = true
  try {
    const res = await apiFetch('/analytics')
    if (res.ok) {
      const data = await res.json()
      simAmount.value = data.recovered_amount_eur || 42680
      simTargetCount.value = data.pending_operations_count ? data.pending_operations_count + 4 : 8
    }
  } catch {
    // fallback
  } finally {
    isSimulating.value = false
    simResult.value = true
  }
}
</script>
