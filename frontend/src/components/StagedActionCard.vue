<template>
  <div class="border border-amber-200 bg-amber-50/40 rounded-2xl p-5 my-4 shadow-sm">
    <!-- Header -->
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-2">
        <ShieldAlert class="w-4 h-4 text-amber-600" />
        <span class="text-xs font-bold uppercase tracking-wider text-amber-900">{{ t('operations.action_to_validate') }}</span>
      </div>
      <span
        class="px-2.5 py-1 rounded-full text-xs font-semibold"
        :class="[
          action.status === 'COMPLETED'
            ? 'bg-emerald-100 text-emerald-800'
            : action.status === 'REFUSED'
            ? 'bg-rose-100 text-rose-800'
            : 'bg-amber-100 text-amber-800'
        ]"
      >
        {{ action.status === 'COMPLETED' ? t('operations.tab_completed') : action.status === 'REFUSED' ? t('operations.refuse') : t('operations.tab_pending') }}
      </span>
    </div>

    <!-- Title & Description -->
    <h3 class="text-base font-bold text-slate-900 mb-1">
      {{ action.title }}
    </h3>
    <p class="text-xs text-slate-600 mb-4">
      {{ action.description }}
    </p>

    <!-- Key Metrics Grid -->
    <div class="grid grid-cols-3 gap-3 bg-white/80 p-3 rounded-xl border border-amber-100 mb-4 text-xs">
      <div>
        <div class="text-slate-400 text-[11px] mb-0.5">{{ t('operations.recipients') }}</div>
        <div class="font-bold text-slate-900">{{ action.target_count }} {{ t('common.contacts') }}</div>
      </div>
      <div>
        <div class="text-slate-400 text-[11px] mb-0.5">{{ t('operations.type') }}</div>
        <div class="font-bold text-slate-900">{{ t('operations.invoice_dunning') }}</div>
      </div>
      <div>
        <div class="text-slate-400 text-[11px] mb-0.5">{{ t('operations.channel') }}</div>
        <div class="font-bold text-slate-900">{{ action.channel || 'Email' }}</div>
      </div>
    </div>

    <!-- Consequence Warning Box -->
    <div class="bg-amber-100/60 border border-amber-200/80 rounded-xl p-3 mb-4 flex items-start gap-2.5">
      <AlertTriangle class="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
      <div class="text-xs text-amber-900">
        <strong class="font-semibold">{{ t('operations.consequence_label') }}</strong> {{ action.consequence_warning }}
      </div>
    </div>

    <!-- Actions Buttons -->
    <div v-if="action.status === 'PENDING'" class="flex items-center justify-end gap-3 pt-2">
      <button
        @click="onRefuse"
        :disabled="isSubmitting"
        class="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-white rounded-xl border border-slate-200 transition cursor-pointer"
      >
        {{ t('operations.refuse') }}
      </button>
      <button
        @click="onValidate"
        :disabled="isSubmitting"
        class="px-5 py-2 text-xs font-semibold text-white bg-brand-600 hover:bg-brand-700 active:bg-brand-800 rounded-xl shadow-sm shadow-brand-600/20 transition flex items-center gap-1.5 cursor-pointer"
      >
        <Check class="w-3.5 h-3.5" />
        <span>{{ t('operations.validate_and_execute') }}</span>
      </button>
    </div>

    <!-- Success Message if executed -->
    <div v-else-if="action.status === 'COMPLETED'" class="flex items-center gap-2 text-xs font-semibold text-emerald-700 pt-1">
      <CheckCircle2 class="w-4 h-4" />
      <span>{{ t('operations.batch_success') }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ShieldAlert, AlertTriangle, Check, CheckCircle2 } from 'lucide-vue-next'
import type { StagedAction } from '../types'
import { useAgentStore } from '../stores/agent'
import { useI18n } from '../composables/useI18n'

const props = defineProps<{
  action: StagedAction
}>()

const emit = defineEmits<{
  (e: 'validated', actionId: string): void
  (e: 'refused', actionId: string): void
}>()

const { t } = useI18n()
const store = useAgentStore()
const isSubmitting = ref<boolean>(false)

async function onValidate(): Promise<void> {
  isSubmitting.value = true
  const ok = await store.validateOperation(props.action.action_id)
  isSubmitting.value = false
  if (ok) {
    props.action.status = 'COMPLETED'
    emit('validated', props.action.action_id)
  }
}

async function onRefuse(): Promise<void> {
  isSubmitting.value = true
  const ok = await store.refuseOperation(props.action.action_id)
  isSubmitting.value = false
  if (ok) {
    props.action.status = 'REFUSED'
    emit('refused', props.action.action_id)
  }
}
</script>
