<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    class="inline-flex items-center justify-center font-medium transition rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/20 disabled:opacity-50 disabled:pointer-events-none cursor-pointer"
    :class="[variantClasses, sizeClasses]"
    @click="$emit('click', $event)"
  >
    <svg
      v-if="loading"
      class="animate-spin -ml-1 mr-2 h-4 w-4 text-current"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    variant?: 'default' | 'outline' | 'destructive' | 'ghost' | 'secondary'
    size?: 'sm' | 'md' | 'lg'
    type?: 'button' | 'submit' | 'reset'
    disabled?: boolean
    loading?: boolean
  }>(),
  {
    variant: 'default',
    size: 'md',
    type: 'button',
    disabled: false,
    loading: false,
  }
)

defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'outline':
      return 'border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 hover:text-slate-900 shadow-xs'
    case 'destructive':
      return 'bg-rose-600 text-white hover:bg-rose-700 shadow-sm shadow-rose-600/20'
    case 'ghost':
      return 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
    case 'secondary':
      return 'bg-slate-100 text-slate-900 hover:bg-slate-200 shadow-xs'
    default:
      return 'bg-brand-600 text-white hover:bg-brand-700 active:bg-brand-800 shadow-sm shadow-brand-600/20'
  }
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'px-3 py-1.5 text-xs'
    case 'lg':
      return 'px-5 py-3 text-base'
    default:
      return 'px-4 py-2 text-sm'
  }
})
</script>
