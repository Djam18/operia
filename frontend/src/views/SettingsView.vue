<template>
  <div class="p-8 max-w-5xl mx-auto flex flex-col gap-8">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-slate-900 tracking-tight">{{ t('settings.title') }}</h1>
      <p class="text-sm text-slate-500 mt-0.5">{{ t('settings.subtitle') }}</p>
    </div>

    <!-- Section 1: Contrôle et validations -->
    <div class="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs flex flex-col gap-5">
      <div>
        <h2 class="text-base font-bold text-slate-900">{{ t('settings.controls_title') }}</h2>
        <p class="text-xs text-slate-500 mt-0.5">{{ t('settings.controls_desc') }}</p>
      </div>

      <div class="space-y-4 pt-2">
        <label class="flex items-center justify-between p-3.5 rounded-xl border border-slate-100 hover:bg-slate-50/60 cursor-pointer transition">
          <div class="flex items-center gap-3">
            <ShieldCheck class="w-4 h-4 text-brand-600" />
            <span class="text-xs font-semibold text-slate-800">{{ t('settings.hitl_emails') }}</span>
          </div>
          <input type="checkbox" v-model="hitlEmails" @change="saveSettings"
            class="w-4 h-4 text-brand-600 rounded-md border-slate-300 focus:ring-brand-500" />
        </label>

        <label class="flex items-center justify-between p-3.5 rounded-xl border border-slate-100 hover:bg-slate-50/60 cursor-pointer transition">
          <div class="flex items-center gap-3">
            <ShieldCheck class="w-4 h-4 text-brand-600" />
            <span class="text-xs font-semibold text-slate-800">{{ t('settings.hitl_data') }}</span>
          </div>
          <input type="checkbox" v-model="hitlData" @change="saveSettings"
            class="w-4 h-4 text-brand-600 rounded-md border-slate-300 focus:ring-brand-500" />
        </label>

        <label class="flex items-center justify-between p-3.5 rounded-xl border border-slate-100 hover:bg-slate-50/60 cursor-pointer transition">
          <div class="flex items-center gap-3">
            <ShieldCheck class="w-4 h-4 text-brand-600" />
            <span class="text-xs font-semibold text-slate-800">{{ t('settings.hitl_export') }}</span>
          </div>
          <input type="checkbox" v-model="hitlExport" @change="saveSettings"
            class="w-4 h-4 text-brand-600 rounded-md border-slate-300 focus:ring-brand-500" />
        </label>
      </div>

      <div v-if="saveStatus" class="text-xs font-medium" :class="saveStatus === 'ok' ? 'text-emerald-600' : 'text-red-600'">
        {{ saveStatus === 'ok' ? '✓ ' + t('settings.saved') : '✕ ' + t('settings.save_error') }}
      </div>
    </div>

    <!-- Section 2: Connexions métier -->
    <div class="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs flex flex-col gap-5">
      <div>
        <h2 class="text-base font-bold text-slate-900">{{ t('settings.connections_title') }}</h2>
        <p class="text-xs text-slate-500 mt-0.5">{{ t('settings.connections_desc') }}</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
        <div class="p-4 rounded-xl border border-slate-200 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <Database class="w-5 h-5 text-slate-400" />
            <div>
              <div class="text-xs font-bold text-slate-900">{{ t('settings.db_label') }}</div>
              <div class="text-[11px] font-semibold flex items-center gap-1" :class="connStatus.database_type ? 'text-emerald-600' : 'text-slate-400'">
                <span class="w-1.5 h-1.5 rounded-full" :class="connStatus.database_type ? 'bg-emerald-500' : 'bg-slate-300'"></span>
                <span>{{ connStatus.database_type || '—' }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="p-4 rounded-xl border border-slate-200 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <BrainCircuit class="w-5 h-5 text-slate-400" />
            <div>
              <div class="text-xs font-bold text-slate-900">Gemini AI</div>
              <div class="text-[11px] font-semibold flex items-center gap-1" :class="connStatus.gemini_active ? 'text-emerald-600' : 'text-amber-600'">
                <span class="w-1.5 h-1.5 rounded-full" :class="connStatus.gemini_active ? 'bg-emerald-500' : 'bg-amber-400'"></span>
                <span>{{ connStatus.gemini_active ? t('settings.connected') : t('settings.disconnected') }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ShieldCheck, Database, BrainCircuit } from 'lucide-vue-next'
import { apiFetch } from '../config/api'
import { useAgentStore } from '../stores/agent'
import { useI18n } from '../composables/useI18n'

const store = useAgentStore()
const { t } = useI18n()

const hitlEmails = ref(true)
const hitlData = ref(true)
const hitlExport = ref(true)
const saveStatus = ref<string | null>(null)

const connStatus = ref({ database_type: '', gemini_active: false, resend_active: false, mode: 'local', is_online: false })

onMounted(async () => {
  try {
    const res = await apiFetch('/settings')
    if (res.ok) {
      const d = await res.json()
      hitlEmails.value = d.require_hitl_emails
      hitlData.value = d.require_hitl_data_mutation
      hitlExport.value = d.require_hitl_exports
    }
  } catch { /* fallback defaults */ }

  try {
    const res = await apiFetch('/status/connectivity')
    if (res.ok) connStatus.value = await res.json()
  } catch { /* offline */ }
})

async function saveSettings() {
  saveStatus.value = null
  try {
    const res = await apiFetch('/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        require_hitl_emails: hitlEmails.value,
        require_hitl_data_mutation: hitlData.value,
        require_hitl_exports: hitlExport.value,
      }),
    })
    saveStatus.value = res.ok ? 'ok' : 'error'
  } catch {
    saveStatus.value = 'error'
  }
  setTimeout(() => { saveStatus.value = null }, 2000)
}
</script>
