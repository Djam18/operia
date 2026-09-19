<script setup lang="ts">
import { useI18n } from '../../composables/useI18n'
import type { QueueStats, QueueTask } from '../../interfaces'
import UiCard from '../ui/UiCard.vue'

defineProps<{
  stats: QueueStats
  tasks: QueueTask[]
}>()

const emit = defineEmits<{
  (e: 'flush-cache'): void
  (e: 'retry-failed'): void
  (e: 'enqueue-demo'): void
}>()

const { t } = useI18n()

function statusColor(status: string): string {
  switch (status) {
    case 'COMPLETED': return 'bg-emerald-50 text-emerald-700 border-emerald-200'
    case 'PROCESSING': return 'bg-blue-50 text-blue-700 border-blue-200 animate-pulse'
    case 'FAILED': return 'bg-rose-50 text-rose-700 border-rose-200'
    default: return 'bg-amber-50 text-amber-700 border-amber-200'
  }
}
</script>

<template>
  <UiCard class="p-5">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
      <div>
        <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wide">
          {{ t('admin.tab_queue') }}
        </h3>
        <p class="text-xs text-slate-500 mt-0.5">
          {{ stats.completed }} {{ t('admin.status_healthy').toLowerCase() }} · {{ stats.avg_duration_ms }} ms {{ t('admin.task_duration').toLowerCase() }}
        </p>
      </div>

      <div class="flex flex-wrap gap-2">
        <button
          class="text-xs px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-md transition"
          @click="emit('flush-cache')"
        >
          {{ t('admin.flush_cache_btn') }}
        </button>
        <button
          v-if="stats.failed > 0"
          class="text-xs px-2.5 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 font-medium rounded-md transition"
          @click="emit('retry-failed')"
        >
          {{ t('admin.retry_failed_btn') }} ({{ stats.failed }})
        </button>
        <button
          class="text-xs px-2.5 py-1.5 bg-brand-50 hover:bg-brand-100 text-brand-700 border border-brand-200 font-medium rounded-md transition"
          @click="emit('enqueue-demo')"
        >
          + {{ t('admin.enqueue_demo_btn') }}
        </button>
      </div>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full text-left text-xs border-collapse">
        <thead>
          <tr class="border-b border-slate-100 text-slate-400 font-semibold">
            <th class="py-2 px-2">{{ t('admin.task_name') }}</th>
            <th class="py-2 px-2">{{ t('admin.task_status') }}</th>
            <th class="py-2 px-2">{{ t('admin.task_duration') }}</th>
            <th class="py-2 px-2 text-right">{{ t('admin.task_queued_at') }}</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-50 text-slate-600">
          <tr v-for="task in tasks.slice(0, 5)" :key="task.id" class="hover:bg-slate-50/60">
            <td class="py-2 px-2 font-medium text-slate-800">{{ task.name }}</td>
            <td class="py-2 px-2">
              <span class="px-2 py-0.5 rounded text-[10px] font-semibold border" :class="statusColor(task.status)">
                {{ task.status }}
              </span>
            </td>
            <td class="py-2 px-2 text-slate-500">{{ task.duration_ms }} ms</td>
            <td class="py-2 px-2 text-right text-[11px] text-slate-400">
              {{ new Date(task.queued_at).toLocaleTimeString() }}
            </td>
          </tr>
          <tr v-if="tasks.length === 0">
            <td colspan="4" class="text-center py-4 text-slate-400">
              Aucune tâche en file d'attente
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </UiCard>
</template>
