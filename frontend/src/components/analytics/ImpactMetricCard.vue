<template>
  <UiCard :border-variant="variant">
    <div class="text-xs text-slate-500 font-medium mb-1">{{ label }}</div>
    <div
      class="text-3xl font-extrabold"
      :class="variant === 'highlight' ? 'text-brand-700' : 'text-slate-900'"
    >
      {{ value }}
    </div>
    <div
      v-if="subtitle"
      class="text-[11px] font-medium mt-1"
      :class="subtitleColorClass"
    >
      {{ subtitle }}
    </div>
  </UiCard>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import UiCard from '../ui/UiCard.vue'

interface Props {
  label: string
  value: string | number
  subtitle?: string
  variant?: 'default' | 'highlight'
  positive?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  positive: false,
})

const subtitleColorClass = computed(() => {
  if (props.positive) return 'text-emerald-600'
  if (props.variant === 'highlight') return 'text-emerald-600'
  return 'text-slate-500'
})
</script>
