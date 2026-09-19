<template>
  <div
    class="bg-white border rounded-2xl shadow-xs transition"
    :class="[
      borderVariant === 'warning'
        ? 'border-amber-200/90'
        : borderVariant === 'highlight'
        ? 'border-brand-200/90'
        : 'border-slate-200/80',
      padded ? 'p-6' : ''
    ]"
  >
    <div v-if="$slots.header" class="border-b border-slate-100 pb-4 mb-4">
      <slot name="header" />
    </div>

    <div>
      <slot />
    </div>

    <div v-if="$slots.footer" class="border-t border-slate-100 pt-4 mt-4">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    borderVariant?: 'default' | 'warning' | 'highlight'
    padded?: boolean
  }>(),
  {
    borderVariant: 'default',
    padded: true,
  }
)
</script>
