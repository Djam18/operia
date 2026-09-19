<template>
  <header class="h-14 border-b border-slate-800/80 px-6 flex items-center justify-between bg-[#0B0F17]">
    <div class="flex items-center gap-6">
      <router-link to="/" class="flex items-center gap-3 hover:opacity-90 transition cursor-pointer">
        <div class="w-7 h-7 rounded-lg bg-cyan-600 flex items-center justify-center font-bold text-white text-xs">
          A
        </div>
        <div>
          <div class="font-bold text-white text-sm tracking-tight">Atlas</div>
          <div class="text-[9px] uppercase tracking-widest text-slate-400 font-semibold">{{ t('console.copilot_sub') }}</div>
        </div>
      </router-link>

      <nav class="flex items-center gap-1">
        <router-link to="/console" class="px-3 py-1.5 rounded-lg font-semibold transition cursor-pointer"
          :class="[$route.path === '/console' ? 'bg-slate-800 text-white' : 'text-slate-400 hover:text-white']">
          {{ t('console.console_tab') }}
        </router-link>
        <router-link to="/data" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition cursor-pointer">
          {{ t('console.sources_tab') }}
        </router-link>
        <router-link to="/history" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition cursor-pointer">
          {{ t('console.journal_tab') }}
        </router-link>
      </nav>
    </div>

    <div class="flex items-center gap-4">
      <router-link to="/" class="text-xs text-cyan-400 hover:underline flex items-center gap-1 font-medium cursor-pointer">
        <span>{{ t('console.standard_mode') }}</span>
      </router-link>

      <router-link to="/operations" class="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 hover:bg-slate-800 border border-slate-800 text-amber-400 text-[11px] font-medium transition cursor-pointer">
        <span class="w-2 h-2 rounded-full bg-amber-400"></span>
        <span>{{ t('console.pending_actions_badge') }}</span>
      </router-link>

      <router-link to="/settings" class="w-7 h-7 rounded-full bg-slate-800 hover:bg-slate-700 flex items-center justify-center text-[11px] font-bold text-slate-300 transition cursor-pointer" title="Paramètres">
        AM
      </router-link>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useI18n } from '../../composables/useI18n'

const { t } = useI18n()
</script>
