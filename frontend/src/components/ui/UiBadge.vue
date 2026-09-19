<template>
  <span
    class="inline-flex items-center gap-1 font-semibold rounded-full tracking-tight transition"
    :class="[variantClasses, sizeClasses]"
  >
    <slot />
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    variant?: 'default' | 'secondary' | 'success' | 'warning' | 'destructive' | 'outline'
    size?: 'sm' | 'md'
  }>(),
  {
    variant: 'default',
    size: 'md',
  }
)

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'success':
      return 'bg-emerald-100 text-emerald-800'
    case 'warning':
      return 'bg-amber-100 text-amber-800'
    case 'destructive':
      return 'bg-rose-100 text-rose-800'
    case 'secondary':
      return 'bg-slate-100 text-slate-700'
    case 'outline':
      return 'border border-slate-200 text-slate-700 bg-white'
    default:
      return 'bg-brand-100 text-brand-800'
  }
})

const sizeClasses = computed(() => {
  return props.size === 'sm' ? 'px-2 py-0.5 text-[10px]' : 'px-2.5 py-0.5 text-xs'
})
</script>
