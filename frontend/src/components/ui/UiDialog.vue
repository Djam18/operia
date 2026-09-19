<template>
  <teleport to="body">
    <div
      v-if="open"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs transition-opacity"
      @click.self="$emit('close')"
    >
      <div class="bg-white rounded-2xl border border-slate-200 shadow-2xl max-w-lg w-full overflow-hidden flex flex-col max-h-[90vh]">
        <!-- Header -->
        <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <h3 class="text-sm font-bold text-slate-900">
            <slot name="title">{{ t('common.details') }}</slot>
          </h3>
          <button
            type="button"
            class="text-slate-400 hover:text-slate-600 rounded-lg p-1 transition cursor-pointer"
            @click="$emit('close')"
          >
            ✕
          </button>
        </div>

        <!-- Content -->
        <div class="p-6 overflow-y-auto text-xs text-slate-600 space-y-4">
          <slot />
        </div>

        <!-- Footer -->
        <div v-if="$slots.footer" class="px-6 py-3.5 bg-slate-50 border-t border-slate-100 flex items-center justify-end gap-2">
          <slot name="footer" />
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup lang="ts">
import { useI18n } from '../../composables/useI18n'

const { t } = useI18n()

defineProps<{
  open: boolean
}>()

defineEmits<{
  (e: 'close'): void
}>()
</script>
