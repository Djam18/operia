<template>
  <div class="w-64 border-r border-slate-200 bg-white flex flex-col shrink-0 h-full select-none">
    <!-- Sidebar Header -->
    <div class="p-3.5 border-b border-slate-100 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900">{{ t('agent.conversations') }}</h2>
        <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-slate-100 text-slate-600">
          {{ conversations.length }}
        </span>
      </div>
      <button
        @click="$emit('new-conversation')"
        class="flex items-center gap-1 px-2 py-1 rounded-lg bg-brand-50 hover:bg-brand-100 text-brand-700 text-xs font-semibold transition cursor-pointer"
        title="Nouvelle conversation"
      >
        <Plus class="w-3.5 h-3.5" />
        <span class="hidden sm:inline">Nouveau</span>
      </button>
    </div>

    <!-- Search input -->
    <div class="p-2.5 border-b border-slate-100">
      <div class="relative flex items-center">
        <Search class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 pointer-events-none" />
        <input
          v-model="searchQuery"
          type="text"
          :placeholder="t('common.search')"
          class="w-full pl-8 pr-7 py-1.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-brand-500 focus:bg-white transition"
        />
        <button
          v-if="searchQuery"
          @click="searchQuery = ''"
          class="absolute right-2 text-slate-400 hover:text-slate-600 text-xs"
        >
          ✕
        </button>
      </div>
    </div>

    <!-- Conversation list -->
    <div class="flex-1 overflow-y-auto p-2 flex flex-col gap-1.5">
      <button
        v-for="c in filteredConversations"
        :key="c.id"
        type="button"
        @click="$emit('select-conversation', c.id); $emit('update:modelValue', c.id)"
        class="group relative w-full text-left p-2.5 rounded-xl transition flex flex-col gap-1 cursor-pointer border"
        :class="[
          modelValue === c.id
            ? 'bg-brand-50/80 border-brand-200 text-brand-950 shadow-xs'
            : 'bg-white border-transparent hover:bg-slate-50/80 hover:border-slate-100 text-slate-700'
        ]"
      >
        <!-- Active indicator bar -->
        <div
          v-if="modelValue === c.id"
          class="absolute left-0 top-2 bottom-2 w-1 bg-brand-600 rounded-r-full"
        />

        <div class="flex items-center justify-between gap-1 pl-1">
          <div class="flex items-center gap-1.5 min-w-0">
            <MessageSquare class="w-3.5 h-3.5 shrink-0" :class="modelValue === c.id ? 'text-brand-600' : 'text-slate-400'" />
            <span class="text-xs font-semibold truncate leading-tight">{{ c.title }}</span>
          </div>

          <!-- Delete button on hover -->
          <button
            v-if="conversations.length > 1"
            type="button"
            @click.stop="$emit('delete-conversation', c.id)"
            class="opacity-0 group-hover:opacity-100 p-1 rounded-md hover:bg-rose-50 hover:text-rose-600 text-slate-400 transition shrink-0"
            title="Supprimer la conversation"
          >
            <Trash2 class="w-3.5 h-3.5" />
          </button>
        </div>

        <div class="flex items-center justify-between text-[11px] text-slate-400 pl-1">
          <span>{{ c.date }}</span>
          <span v-if="c.messages && c.messages.length > 0" class="text-[10px] font-medium text-slate-400">
            {{ c.messages.length }} msg
          </span>
        </div>
      </button>

      <div v-if="filteredConversations.length === 0" class="p-4 text-center text-xs text-slate-400">
        Aucune conversation
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Plus, Search, MessageSquare, Trash2 } from 'lucide-vue-next'
import type { Conversation } from '../../interfaces'
import { useI18n } from '../../composables/useI18n'

const { t } = useI18n()

const props = defineProps<{
  conversations: Conversation[]
  modelValue: string
}>()

defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'select-conversation', value: string): void
  (e: 'new-conversation'): void
  (e: 'delete-conversation', value: string): void
}>()

const searchQuery = ref<string>('')

const filteredConversations = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return props.conversations
  return props.conversations.filter(c =>
    c.title.toLowerCase().includes(q) ||
    (c.messages && c.messages.some(m => m.content.toLowerCase().includes(q)))
  )
})
</script>
