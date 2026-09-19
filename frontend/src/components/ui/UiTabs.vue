<template>
  <div class="flex items-center gap-1 p-1 bg-slate-100 rounded-xl">
    <button
      v-for="tab in items"
      :key="tab.value"
      type="button"
      class="px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 cursor-pointer"
      :class="[
        modelValue === tab.value
          ? 'bg-white text-slate-900 shadow-xs'
          : 'text-slate-500 hover:text-slate-800'
      ]"
      @click="$emit('update:modelValue', tab.value)"
    >
      <span>{{ tab.label }}</span>
      <span
        v-if="tab.badge !== undefined"
        class="px-1.5 py-0.2 rounded-full text-[10px] bg-slate-200 text-slate-700"
      >
        {{ tab.badge }}
      </span>
    </button>
  </div>
</template>

<script setup lang="ts">
export interface TabItem {
  label: string
  value: string
  badge?: number | string
}

defineProps<{
  items: TabItem[]
  modelValue: string
}>()

defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()
</script>
