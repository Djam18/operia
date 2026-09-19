<template>
  <UiCard class="flex flex-col justify-between hover:border-brand-300 transition">
    <template #header>
      <div class="flex items-center justify-between">
        <UiBadge :variant="playbook.badgeVariant">{{ playbook.category }}</UiBadge>
        <span class="text-[11px] text-slate-400 font-mono">{{ playbook.duration }}</span>
      </div>
    </template>

    <div class="space-y-2 mb-4">
      <h3 class="font-bold text-slate-900 text-sm">{{ playbook.title }}</h3>
      <p class="text-xs text-slate-500 leading-relaxed">{{ playbook.description }}</p>
    </div>

    <template #footer>
      <div class="flex items-center justify-between pt-1">
        <span class="text-[11px] font-semibold text-slate-400">{{ playbook.source }}</span>
        <UiButton size="sm" @click="$emit('launch', playbook)">
          <Play class="w-3.5 h-3.5 mr-1" />
          {{ launchLabel }}
        </UiButton>
      </div>
    </template>
  </UiCard>
</template>

<script setup lang="ts">
import { Play } from 'lucide-vue-next'
import UiCard from '../ui/UiCard.vue'
import UiBadge from '../ui/UiBadge.vue'
import UiButton from '../ui/UiButton.vue'
import type { Playbook } from '../../data/playbooks'

defineProps<{
  playbook: Playbook
  launchLabel: string
}>()

defineEmits<{
  (e: 'launch', playbook: Playbook): void
}>()
</script>
