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

function updateThreshold(e: Event) {
  const val = parseFloat((e.target as HTMLInputElement).value) || 0
  emit('update:config', { ...props.config, hitl_financial_threshold: val })
}

function toggleChannel(channel: string) {
  const current = [...props.config.allowed_channels]
  const idx = current.indexOf(channel)
  if (idx >= 0) {
    if (current.length > 1) current.splice(idx, 1)
  } else {
    current.push(channel)
  }
  emit('update:config', { ...props.config, allowed_channels: current })
}

function toggleStrict() {
  emit('update:config', { ...props.config, strict_guardrails: !props.config.strict_guardrails })
}
</script>

<template>
  <UiCard class="p-5 flex flex-col justify-between">
    <div>
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wide">
          {{ t('admin.tab_guardrails') }}
        </h3>
        <span class="text-xs px-2 py-0.5 rounded bg-amber-50 text-amber-700 font-semibold border border-amber-200">
          HITL Strict
        </span>
      </div>

      <div class="space-y-4 text-xs">
        <div>
          <label class="block font-medium text-slate-700 mb-1">
            {{ t('admin.hitl_financial_threshold') }}
          </label>
          <div class="relative">
            <input
              type="number"
              step="500"
              :value="config.hitl_financial_threshold"
              class="w-full text-xs rounded-lg border-slate-300 p-2 pr-8 border focus:ring-2 focus:ring-brand-500 focus:outline-none"
              @input="updateThreshold"
            >
            <span class="absolute right-3 top-2 text-slate-400 font-semibold">€</span>
          </div>
          <p class="text-[11px] text-slate-400 mt-1">{{ t('admin.hitl_threshold_hint') }}</p>
        </div>

        <div>
          <label class="block font-medium text-slate-700 mb-1.5">{{ t('admin.allowed_channels') }}</label>
          <div class="flex gap-2">
            <button
              v-for="ch in ['Email', 'SMS', 'Webhook']"
              :key="ch"
              type="button"
              class="px-2.5 py-1 rounded-md text-xs font-medium border transition"
              :class="config.allowed_channels.includes(ch) ? 'bg-brand-50 border-brand-300 text-brand-700' : 'bg-slate-50 border-slate-200 text-slate-400'"
              @click="toggleChannel(ch)"
            >
              {{ ch }}
            </button>
          </div>
        </div>

        <div class="pt-2 border-t border-slate-100 flex items-center justify-between">
          <span class="text-slate-700 font-medium">{{ t('admin.strict_guardrails') }}</span>
          <input
            type="checkbox"
            :checked="config.strict_guardrails"
            class="w-4 h-4 accent-brand-600 rounded cursor-pointer"
            @change="toggleStrict"
          >
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
