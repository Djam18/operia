<template>
  <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <UiCard
      v-for="card in cards"
      :key="card.id"
      :border-variant="card.highlight ? 'warning' : 'default'"
      :class="card.highlight ? 'bg-amber-50/40 border-amber-200/80' : ''"
      class="p-5 flex flex-col justify-between"
    >
      <div
        class="flex items-center justify-between text-xs font-medium mb-3"
        :class="card.highlight ? 'text-amber-900 font-semibold' : 'text-slate-500'"
      >
        <span>{{ card.label }}</span>
        <component
          :is="card.icon"
          class="w-4 h-4"
          :class="card.highlight ? 'text-amber-600' : 'text-slate-400'"
        />
      </div>

      <div>
        <div
          class="text-3xl font-extrabold"
          :class="card.highlight ? 'text-amber-700' : 'text-slate-900'"
        >
          {{ card.value }}
        </div>
        <div
          class="text-xs mt-1"
          :class="card.subtitleColorClass"
        >
          {{ card.subtitle }}
        </div>
      </div>
    </UiCard>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { MessageSquare, FileText, Clock, CheckCircle } from 'lucide-vue-next'
import UiCard from '../ui/UiCard.vue'
import { useI18n } from '../../composables/useI18n'
import type { DashboardStats } from '../../interfaces'

const props = defineProps<{
  pendingCount: number
  stats?: DashboardStats
}>()

const { t } = useI18n()

const cards = computed(() => [
  {
    id: 'queries',
    label: t('dashboard.kpi_queries'),
    value: props.stats?.queries_count ?? 128,
    subtitle: t('dashboard.kpi_queries_sub'),
    icon: MessageSquare,
    highlight: false,
    subtitleColorClass: 'text-slate-500',
  },
  {
    id: 'actions',
    label: t('dashboard.kpi_actions'),
    value: props.stats?.actions_count ?? 42,
    subtitle: t('dashboard.kpi_actions_sub'),
    icon: FileText,
    highlight: false,
    subtitleColorClass: 'text-slate-500',
  },
  {
    id: 'pending',
    label: t('dashboard.kpi_pending'),
    value: props.stats?.pending_count ?? props.pendingCount,
    subtitle: t('dashboard.kpi_pending_sub'),
    icon: Clock,
    highlight: true,
    subtitleColorClass: 'text-amber-800',
  },
  {
    id: 'completed',
    label: t('dashboard.kpi_completed'),
    value: props.stats?.completed_count ?? 35,
    subtitle: t('dashboard.kpi_completed_sub'),
    icon: CheckCircle,
    highlight: false,
    subtitleColorClass: 'text-emerald-600 font-medium',
  },
])
</script>
