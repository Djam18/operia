<script setup lang="ts">
import { ref } from 'vue'
import { Mail, ShieldCheck, ChevronDown, Send } from 'lucide-vue-next'
import type { OutboxEmail } from '../../interfaces'

defineProps<{
  emails: OutboxEmail[]
}>()

const openEmailId = ref<string | null>(null)

function toggleEmail(id: string) {
  openEmailId.value = openEmailId.value === id ? null : id
}
</script>

<template>
  <div class="bg-white rounded-2xl border border-slate-200 divide-y divide-slate-100 shadow-xs overflow-hidden">
    <div class="p-4 bg-slate-50 border-b border-slate-200/80 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <Mail class="w-4 h-4 text-brand-600" />
        <span class="text-xs font-bold text-slate-800 uppercase tracking-wide">
          Boîte d'envoi locale (Simulation & Traçabilité Offline)
        </span>
      </div>
      <span class="text-[11px] px-2.5 py-0.5 rounded-full font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
        <ShieldCheck class="w-3 h-3" />
        Mode Local Garanti Zéro Fuite Externe
      </span>
    </div>

    <div v-for="email in emails" :key="email.id" class="p-4 hover:bg-slate-50/50 transition">
      <div class="flex items-center justify-between cursor-pointer" @click="toggleEmail(email.id)">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-brand-50 text-brand-600 flex items-center justify-center shrink-0">
            <Send class="w-4 h-4" />
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="font-bold text-xs text-slate-900">{{ email.recipient_name }}</span>
              <span class="text-[11px] text-slate-400 font-mono">({{ email.recipient_email }})</span>
              <span class="px-2 py-0.2 rounded text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                {{ email.delivery_mode }}
              </span>
            </div>
            <div class="text-xs text-slate-600 mt-0.5 font-medium">{{ email.subject }}</div>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <span class="text-[11px] text-slate-400">
            {{ email.created_at ? new Date(email.created_at).toLocaleTimeString() : 'À l\'instant' }}
          </span>
          <ChevronDown
            class="w-4 h-4 text-slate-400 transition-transform"
            :class="{ 'rotate-180': openEmailId === email.id }"
          />
        </div>
      </div>

      <!-- Preview Email Body -->
      <div
        v-if="openEmailId === email.id"
        class="mt-3 p-4 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-700 font-sans leading-relaxed"
        v-html="email.body_html"
      />
    </div>

    <div v-if="emails.length === 0" class="p-8 text-center text-xs text-slate-400">
      Aucun email envoyé pour le moment. Validez une relance dans l'onglet "En attente" pour simuler l'envoi local.
    </div>
  </div>
</template>
