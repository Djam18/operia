<script setup lang="ts">
import { useI18n } from '../../composables/useI18n'
import type { AdminAgentConfig } from '../../interfaces'
import UiCard from '../ui/UiCard.vue'

const props = defineProps<{
  config: AdminAgentConfig
  isSaving: boolean
}>()

const emit = defineEmits<{
  (e: 'update:config', value: AdminAgentConfig): void
  (e: 'save'): void
}>()

const { t } = useI18n()

function updateModel(e: Event) {
  const val = (e.target as HTMLSelectElement).value
  emit('update:config', { ...props.config, model_name: val })
}

function updateTemp(e: Event) {
  const val = parseFloat((e.target as HTMLInputElement).value)
  emit('update:config', { ...props.config, temperature: val })
}
</script>

<template>
  <UiCard class="p-5 flex flex-col justify-between">
    <div>
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wide">
          {{ t('admin.tab_model') }}
        </h3>
        <span class="text-xs px-2 py-0.5 rounded bg-brand-50 text-brand-700 font-semibold border border-brand-200">
          Dual-Mode Ready
        </span>
      </div>

      <div class="space-y-4 text-xs">
        <div>
          <label class="block font-medium text-slate-700 mb-1.5">{{ t('admin.model_selection') }}</label>
          <select
            :value="config.model_name"
            class="w-full text-xs rounded-lg border-slate-300 bg-white p-2 border focus:ring-2 focus:ring-brand-500 focus:outline-none"
            @change="updateModel"
          >
            <option value="gemini-1.5-pro">Gemini 1.5 Pro (Raisonnement & Finance Avancée)</option>
            <option value="gemini-1.5-flash">Gemini 1.5 Flash (Haute Vitesse & Faible Latence)</option>
            <option value="local-autonomous">Local Autonomous (Règles Métier · Mode Déconnecté)</option>
          </select>
        </div>

        <div>
          <div class="flex justify-between font-medium text-slate-700 mb-1">
            <span>{{ t('admin.temperature_label') }}</span>
            <span class="font-bold text-brand-600">{{ config.temperature.toFixed(2) }}</span>
          </div>
          <input
            type="range"
            min="0.0"
            max="1.0"
            step="0.05"
            :value="config.temperature"
            class="w-full accent-brand-600 cursor-pointer"
            @input="updateTemp"
          >
          <p class="text-[11px] text-slate-400 mt-1">{{ t('admin.temperature_hint') }}</p>
        </div>
      </div>
    </div>

    <div class="mt-5 pt-3 border-t border-slate-100 flex justify-end">
      <button
        class="text-xs px-3.5 py-2 bg-brand-600 hover:bg-brand-700 text-white font-medium rounded-lg shadow-sm transition disabled:opacity-50"
        :disabled="isSaving"
        @click="emit('save')"
      >
        {{ isSaving ? '...' : t('admin.save_config_btn') }}
      </button>
    </div>
  </UiCard>
</template>
