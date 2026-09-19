<template>
  <div class="min-h-screen bg-slate-50 flex items-center justify-center p-6">
    <div class="max-w-2xl w-full flex flex-col gap-6">
      <!-- Steps Indicator -->
      <div class="flex items-center justify-between px-2">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-xl bg-brand-600 text-white font-bold flex items-center justify-center text-xs">
            {{ currentStep }}
          </div>
          <span class="text-sm font-bold text-slate-900">Étape {{ currentStep }} sur 3</span>
        </div>
        <button @click="finishOnboarding" class="text-xs text-slate-400 hover:text-slate-600 cursor-pointer">
          Passer l'introduction →
        </button>
      </div>

      <!-- Main Onboarding Card -->
      <UiCard class="p-8">
        <!-- Step 1: Connected Sources -->
        <div v-if="currentStep === 1" class="space-y-4">
          <div class="w-12 h-12 rounded-2xl bg-brand-50 text-brand-600 flex items-center justify-center">
            <Database class="w-6 h-6" />
          </div>
          <h2 class="text-lg font-bold text-slate-900">{{ t('onboarding.step1_title') }}</h2>
          <p class="text-xs text-slate-500 leading-relaxed">{{ t('onboarding.step1_desc') }}</p>

          <div class="p-4 rounded-xl bg-slate-50 border border-slate-200/80 space-y-2 text-xs">
            <div class="flex items-center justify-between text-slate-700">
              <span>ERP & Base Financière (5 ans d'historique)</span>
              <UiBadge variant="success">18 406 factures synchronisées</UiBadge>
            </div>
            <div class="flex items-center justify-between text-slate-700">
              <span>CRM Clients (Europe & Panafrique)</span>
              <UiBadge variant="success">4 820 comptes connectés</UiBadge>
            </div>
          </div>
        </div>

        <!-- Step 2: Natural Language & ReAct Engine -->
        <div v-else-if="currentStep === 2" class="space-y-4">
          <div class="w-12 h-12 rounded-2xl bg-cyan-50 text-cyan-600 flex items-center justify-center">
            <Bot class="w-6 h-6" />
          </div>
          <h2 class="text-lg font-bold text-slate-900">{{ t('onboarding.step2_title') }}</h2>
          <p class="text-xs text-slate-500 leading-relaxed">{{ t('onboarding.step2_desc') }}</p>

          <div class="p-4 rounded-xl bg-slate-900 text-white space-y-2.5 text-xs font-mono">
            <div class="text-slate-400"># Raisonnement ReAct autonome :</div>
            <div class="flex items-center gap-2">
              <UiBadge variant="secondary" class="bg-slate-800 text-cyan-300 text-[10px]">THINK</UiBadge>
              <span class="text-slate-300">Identifier les retards > 30j en zone UEMOA</span>
            </div>
            <div class="flex items-center gap-2">
              <UiBadge variant="secondary" class="bg-cyan-950 text-cyan-400 text-[10px]">TOOL</UiBadge>
              <span class="text-cyan-200">erp.factures.query(region="Afrique de l'Ouest", days>30)</span>
            </div>
            <div class="flex items-center gap-2">
              <UiBadge variant="secondary" class="bg-amber-950 text-amber-300 text-[10px]">STAGE</UiBadge>
              <span class="text-amber-200">Préparer action relance avec approbation</span>
            </div>
          </div>
        </div>

        <!-- Step 3: Human In The Loop & ROI Simulator -->
        <div v-else class="space-y-4">
          <div class="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center">
            <ShieldCheck class="w-6 h-6" />
          </div>
          <h2 class="text-lg font-bold text-slate-900">{{ t('onboarding.step3_title') }}</h2>
          <p class="text-xs text-slate-500 leading-relaxed">{{ t('onboarding.step3_desc') }}</p>

          <!-- Interactive ROI Calculator Widget -->
          <OnboardingRoiWidget />
        </div>

        <!-- Footer Actions -->
        <template #footer>
          <div class="flex items-center justify-between pt-2">
            <button
              v-if="currentStep > 1"
              @click="currentStep--"
              class="text-xs font-semibold text-slate-500 hover:text-slate-800 cursor-pointer"
            >
              ← Précédent
            </button>
            <div v-else></div>

            <UiButton v-if="currentStep < 3" @click="currentStep++">
              {{ t('onboarding.btn_next') }} →
            </UiButton>
            <UiButton v-else @click="finishOnboarding">
              {{ t('onboarding.btn_finish') }}
            </UiButton>
          </div>
        </template>
      </UiCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Database, Bot, ShieldCheck } from 'lucide-vue-next'
import UiCard from '../components/ui/UiCard.vue'
import UiBadge from '../components/ui/UiBadge.vue'
import UiButton from '../components/ui/UiButton.vue'
import OnboardingRoiWidget from '../components/onboarding/OnboardingRoiWidget.vue'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()
const router = useRouter()
const currentStep = ref<number>(1)

function finishOnboarding(): void {
  router.push('/')
}
</script>
