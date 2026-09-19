<template>
  <!-- User message -->
  <div v-if="message.sender === 'user'" class="flex justify-end items-end gap-2 my-2">
    <span class="text-[10px] text-slate-400 mb-1">{{ message.timestamp }}</span>
    <div class="bg-slate-900 text-white px-4 py-2.5 rounded-2xl rounded-br-xs max-w-lg text-xs leading-relaxed shadow-xs">
      {{ message.content }}
    </div>
  </div>

  <!-- Assistant message -->
  <div v-else class="flex items-start gap-3 my-4">
    <!-- OpérIA Avatar -->
    <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-brand-600 to-brand-400 flex items-center justify-center text-white shrink-0 mt-0.5 shadow-xs">
      <Bot class="w-4 h-4" />
    </div>

    <!-- Message Content & Blocks -->
    <div class="flex-1 max-w-3xl space-y-3">
      <div class="flex items-center gap-2">
        <span class="text-xs font-bold text-slate-900">OpérIA</span>
        <span class="text-[10px] px-1.5 py-0.5 rounded bg-brand-50 text-brand-700 font-semibold border border-brand-100">Agent</span>
        <span class="text-[10px] text-slate-400">{{ message.timestamp }}</span>
      </div>

      <!-- Thinking Banner -->
      <div
        v-if="message.isThinking"
        class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-50 text-brand-700 text-xs font-semibold border border-brand-200 animate-pulse"
      >
        <span class="w-2 h-2 rounded-full bg-brand-600 animate-ping" />
        <span>{{ message.thinkingMessage || 'Analyse en cours...' }}</span>
      </div>

      <!-- Assistant Text -->
      <div
        v-if="message.content"
        class="text-xs text-slate-800 leading-relaxed font-medium bg-white p-3.5 rounded-2xl border border-slate-200/80 shadow-xs whitespace-pre-line"
      >
        {{ message.content }}
      </div>

      <!-- Tool Execution Badge -->
      <ToolExecutionBadge
        v-if="message.tools && message.tools.length > 0"
        :tools="message.tools"
      />

      <!-- Invoices Table -->
      <InvoiceTableCard
        v-if="message.invoices && message.invoices.length > 0"
        :invoices="isShowingAll ? message.invoices : message.invoices.slice(0, 5)"
        :total-count="message.invoices.length"
        :show-all="isShowingAll"
        @toggle-show-all="isShowingAll = !isShowingAll"
      />

      <!-- Staged Action Card -->
      <StagedActionCard
        v-if="message.stagedAction"
        :action="message.stagedAction"
        @validated="(id) => { if (message.stagedAction) message.stagedAction.status = 'COMPLETED'; $emit('action-validated', id) }"
        @refused="(id) => { if (message.stagedAction) message.stagedAction.status = 'REFUSED'; $emit('action-refused', id) }"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Bot } from 'lucide-vue-next'
import type { ChatMessage } from '../../interfaces'
import ToolExecutionBadge from '../ToolExecutionBadge.vue'
import StagedActionCard from '../StagedActionCard.vue'
import InvoiceTableCard from './InvoiceTableCard.vue'

defineProps<{
  message: ChatMessage
  showAll?: boolean
}>()

defineEmits<{
  (e: 'toggle-show-all'): void
  (e: 'action-validated', actionId: string): void
  (e: 'action-refused', actionId: string): void
}>()

const isShowingAll = ref<boolean>(false)
</script>
