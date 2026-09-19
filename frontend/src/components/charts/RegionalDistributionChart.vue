<template>
  <div class="flex items-center gap-6">
    <!-- SVG Donut -->
    <div class="relative w-32 h-32 shrink-0">
      <svg class="w-full h-full -rotate-90" viewBox="0 0 100 100">
        <!-- Background circle -->
        <circle cx="50" cy="50" r="38" fill="none" stroke="#f1f5f9" stroke-width="12" />

        <!-- Europe (45%) -->
        <circle
          cx="50"
          cy="50"
          r="38"
          fill="none"
          stroke="#4f46e5"
          stroke-width="12"
          stroke-dasharray="107 238"
          stroke-dashoffset="0"
        />

        <!-- Afrique de l'Ouest (30%) -->
        <circle
          cx="50"
          cy="50"
          r="38"
          fill="none"
          stroke="#06b6d4"
          stroke-width="12"
          stroke-dasharray="71 238"
          stroke-dashoffset="-107"
        />

        <!-- Maghreb (15%) -->
        <circle
          cx="50"
          cy="50"
          r="38"
          fill="none"
          stroke="#f59e0b"
          stroke-width="12"
          stroke-dasharray="35 238"
          stroke-dashoffset="-178"
        />

        <!-- Autres (10%) -->
        <circle
          cx="50"
          cy="50"
          r="38"
          fill="none"
          stroke="#10b981"
          stroke-width="12"
          stroke-dasharray="24 238"
          stroke-dashoffset="-213"
        />
      </svg>

      <div class="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span class="text-xs font-black text-slate-900">18 406</span>
        <span class="text-[9px] text-slate-400 font-medium">{{ t('common.invoices') }}</span>
      </div>
    </div>

    <!-- Legend -->
    <div class="flex flex-col gap-2 text-xs flex-1">
      <div v-for="item in regions" :key="item.name" class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full" :class="item.dotColor"></span>
          <span class="text-slate-600 font-medium">{{ item.name }}</span>
        </div>
        <span class="font-bold text-slate-900">{{ item.percent }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from '../../composables/useI18n'

const { t } = useI18n()

const regions = computed(() => [
  { name: t('analytics.region_europe'), percent: 45, dotColor: 'bg-brand-600' },
  { name: t('analytics.region_west_africa'), percent: 30, dotColor: 'bg-cyan-500' },
  { name: t('analytics.region_maghreb'), percent: 15, dotColor: 'bg-amber-500' },
  { name: t('analytics.other_hubs'), percent: 10, dotColor: 'bg-emerald-500' },
])
</script>
