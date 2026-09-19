<template>
  <div class="w-full flex flex-col gap-3">
    <div class="space-y-2.5">
      <div v-for="bucket in displayBuckets" :key="bucket.label" class="space-y-1">
        <div class="flex items-center justify-between text-xs">
          <span class="font-medium text-slate-700">{{ bucket.label }}</span>
          <span class="font-bold text-slate-900">{{ bucket.formattedAmount }}</span>
        </div>

        <div class="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden flex">
          <div
            class="h-full rounded-full transition-all duration-500"
            :class="bucket.color"
            :style="{ width: bucket.percentage + '%' }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { formatCurrency } from '../../utils/currency'
import { useI18n } from '../../composables/useI18n'

const { t } = useI18n()

export interface AgingBucket {
  label: string
  amount: number
  percentage: number
  color?: string
}

const props = withDefaults(
  defineProps<{
    buckets?: AgingBucket[]
    currency?: string
  }>(),
  {
    currency: 'EUR',
  }
)

const defaultBuckets = computed<AgingBucket[]>(() => [
  { label: t('analytics.aging_normal'), amount: 124500, percentage: 55, color: 'bg-emerald-500' },
  { label: t('analytics.aging_n1'), amount: 86420, percentage: 38, color: 'bg-brand-500' },
  { label: t('analytics.aging_n2'), amount: 34100, percentage: 15, color: 'bg-amber-500' },
  { label: t('analytics.aging_dispute'), amount: 11060, percentage: 5, color: 'bg-rose-500' },
])

const displayBuckets = computed(() => {
  const source = props.buckets && props.buckets.length > 0 ? props.buckets : defaultBuckets.value
  return source.map((b) => ({
    ...b,
    color: b.color || 'bg-brand-500',
    formattedAmount: formatCurrency(b.amount, props.currency),
  }))
})
</script>
