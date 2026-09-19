<template>
  <div class="relative flex items-center w-full">
    <div v-if="$slots.prefix" class="absolute left-3.5 text-slate-400 flex items-center pointer-events-none">
      <slot name="prefix" />
    </div>

    <input
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      class="w-full bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition py-2.5"
      :class="[$slots.prefix ? 'pl-9' : 'pl-3.5', $slots.suffix ? 'pr-9' : 'pr-3.5']"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      @keydown.enter="$emit('enter')"
    />

    <div v-if="$slots.suffix" class="absolute right-3 text-slate-400 flex items-center">
      <slot name="suffix" />
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    modelValue: string
    placeholder?: string
    type?: string
    disabled?: boolean
  }>(),
  {
    placeholder: '',
    type: 'text',
    disabled: false,
  }
)

defineEmits<{
  (e: 'update:modelValue', val: string): void
  (e: 'enter'): void
}>()
</script>
