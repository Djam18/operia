<template>
  <div class="flex h-screen overflow-hidden bg-[#F8FAFC]">
    <!-- Sub-Sidebar: Conversations List -->
    <ConversationSidebar
      :conversations="conversations"
      v-model="activeConvId"
      @select-conversation="selectConversation"
      @new-conversation="createNewConversation"
      @delete-conversation="deleteConversation"
    />

    <!-- Main Chat Workspace -->
    <div class="flex-1 flex flex-col h-screen overflow-hidden">
      <!-- Chat Header -->
      <div class="px-6 py-3.5 bg-white border-b border-slate-200 flex items-center justify-between shrink-0">
        <div>
          <div class="flex items-center gap-2.5">
            <h1 class="text-sm font-bold text-slate-900 truncate max-w-md">
              {{ activeConversation?.title || 'Nouvelle conversation' }}
            </h1>
            <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-slate-100 text-slate-700 border border-slate-200 shrink-0">
              <Shield class="w-3 h-3 text-brand-600" />
              <span>Mode contrôlé</span>
            </span>
          </div>
          <p class="text-[11px] text-slate-500 mt-0.5 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-500" />
            <span>Agent prêt · ERP, CRM et Messagerie connectés</span>
          </p>
        </div>

        <!-- Regional Filter -->
        <div class="flex items-center gap-2">
          <span class="text-xs text-slate-400 font-medium">Périmètre :</span>
          <select
            v-model="selectedRegion"
            @change="triggerQuery"
            class="text-xs bg-white border border-slate-200 rounded-xl px-2.5 py-1.5 font-medium text-slate-700 focus:outline-none focus:ring-1 focus:ring-brand-500 cursor-pointer"
          >
            <option value="Toutes">Global (Europe & Afrique)</option>
            <option value="Afrique de l'Ouest">Afrique de l'Ouest (FCFA / XOF)</option>
            <option value="Afrique du Nord">Afrique du Nord (MAD / Maghreb)</option>
            <option value="Europe">Europe (EUR)</option>
          </select>
        </div>
      </div>

      <!-- Chat Messages Feed / Scroll Container -->
      <div ref="chatScrollRef" class="flex-1 overflow-y-auto p-6 space-y-4 max-w-4xl w-full mx-auto">
        <!-- Empty State with Quick Prompts -->
        <div v-if="currentMessages.length === 0" class="py-12 flex flex-col items-center justify-center text-center space-y-4">
          <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-brand-600 to-brand-400 flex items-center justify-center text-white shadow-md">
            <Bot class="w-6 h-6" />
          </div>
          <div class="max-w-md space-y-1">
            <h3 class="text-sm font-bold text-slate-900">Comment puis-je vous aider aujourd'hui ?</h3>
            <p class="text-xs text-slate-500">Posez une question sur les factures, initiez une relance amiable ou analysez les encours clients.</p>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 max-w-lg w-full pt-4 text-left">
            <button
              v-for="(p, idx) in quickPrompts"
              :key="idx"
              @click="sendCustomQuery(p)"
              class="p-3 rounded-xl bg-white border border-slate-200 hover:border-brand-300 hover:bg-brand-50/40 text-xs font-medium text-slate-700 hover:text-brand-900 transition flex items-center justify-between cursor-pointer group shadow-xs"
            >
              <span class="truncate">{{ p }}</span>
              <Sparkles class="w-3.5 h-3.5 text-slate-400 group-hover:text-brand-600 shrink-0 ml-2" />
            </button>
          </div>
        </div>

        <!-- Message List -->
        <ChatMessageBubble
          v-for="msg in currentMessages"
          :key="msg.id"
          :message="msg"
          :show-all="showAll"
          @toggle-show-all="showAll = !showAll"
        />
      </div>

      <!-- Bottom Chat Input Bar -->
      <div class="p-3.5 bg-white border-t border-slate-200 shrink-0">
        <div class="max-w-4xl mx-auto flex flex-col gap-2">
          <div class="relative flex items-center">
            <input
              v-model="inputQuery"
              @keydown.enter="sendCustomQuery()"
              type="text"
              :disabled="isStreaming"
              placeholder="Demandez une analyse, relance ou export de données..."
              class="w-full pl-4 pr-12 py-2.5 bg-slate-50 border border-slate-200 rounded-2xl text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition disabled:opacity-60"
            />
            <button
              @click="sendCustomQuery()"
              :disabled="isStreaming || !inputQuery.trim()"
              class="w-8 h-8 rounded-xl bg-brand-600 hover:bg-brand-700 text-white flex items-center justify-center absolute right-2 transition shadow-xs disabled:opacity-40 cursor-pointer"
            >
              <CornerDownLeft class="w-4 h-4" />
            </button>
          </div>

          <div class="flex items-center justify-between text-[11px] text-slate-400 px-1">
            <span class="flex items-center gap-1.5 text-slate-500 font-medium">
              <ShieldCheck class="w-3.5 h-3.5 text-brand-600" />
              Validation humaine requise (HITL) avant tout impact réel
            </span>
            <span>Appuyez sur Entrée pour envoyer</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Context Sidebar -->
    <ContextSidebar :selected-region="selectedRegion" />
  </div>
</template>

<script setup lang="ts">
import { Bot, Shield, CornerDownLeft, ShieldCheck, Sparkles } from 'lucide-vue-next'
import ConversationSidebar from '../components/agent/ConversationSidebar.vue'
import ContextSidebar from '../components/agent/ContextSidebar.vue'
import ChatMessageBubble from '../components/agent/ChatMessageBubble.vue'
import { useAgentChat } from '../composables/useAgentChat'

const {
  conversations, activeConvId, activeConversation, currentMessages,
  selectedRegion, inputQuery, showAll, isStreaming,
  chatScrollRef, createNewConversation, selectConversation, deleteConversation,
  triggerQuery, sendCustomQuery,
} = useAgentChat()

const quickPrompts = [
  "Donne-moi les factures impayées depuis plus de 30 jours.",
  "Prépare une relance amiable par email pour les clients éligibles.",
  "Exporte les comptes clients actifs de la région Europe en CSV.",
  "Analyse les limites de crédit et les dépassements d'encours."
]
</script>
