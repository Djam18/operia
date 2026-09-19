<template>
  <div class="lg:col-span-2 bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs">
    <div class="flex items-center justify-between mb-5">
      <div>
        <h2 class="text-base font-bold text-slate-900">{{ t('dashboard.recent_activity') }}</h2>
        <p class="text-xs text-slate-400">{{ t('dashboard.recent_activity_sub') }}</p>
      </div>
      <router-link to="/history" class="text-xs font-semibold text-brand-600 hover:text-brand-700 flex items-center gap-1 cursor-pointer">
        <span>{{ t('common.see_all') }}</span>
        <ArrowRight class="w-3.5 h-3.5" />
      </router-link>
    </div>

    <div class="flex flex-col gap-3">
      <div
        v-for="(item, idx) in items"
        :key="idx"
        class="flex items-center justify-between p-3.5 rounded-xl border border-slate-100 hover:bg-slate-50/80 transition"
      >
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-slate-100 flex items-center justify-center text-slate-500">
            <FileText class="w-4 h-4" />
          </div>
          <div>
            <div class="text-xs font-bold text-slate-900">{{ item.title }}</div>
            <div class="text-[11px] text-slate-500">{{ item.subtitle }}</div>
          </div>
        </div>

        <div class="flex items-center gap-4">
          <span class="text-xs text-slate-400">{{ item.time }}</span>
          <span
            class="px-2.5 py-0.5 rounded-full text-xs font-semibold flex items-center gap-1"
            :class="[
              item.status === 'En attente'
                ? 'bg-amber-100 text-amber-800'
                : 'bg-emerald-100 text-emerald-800'
            ]"
          >
            <component :is="item.status === 'En attente' ? Clock : Check" class="w-3 h-3" />
            {{ item.status }}
          </span>
          <MoreHorizontal class="w-4 h-4 text-slate-400 cursor-pointer" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FileText, Clock, Check, ArrowRight, MoreHorizontal } from 'lucide-vue-next'
import { useI18n } from '../../composables/useI18n'

const { t } = useI18n()

interface ActivityItem {
  title: string
  subtitle: string
  time: string
  status: string
}

defineProps<{
  items: ActivityItem[]
}>()
</script>
