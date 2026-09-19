<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useI18n } from '../composables/useI18n'
import { useAdminStore } from '../stores/admin'
import AdminSystemHealthCard from '../components/admin/AdminSystemHealthCard.vue'
import AdminModelConfigCard from '../components/admin/AdminModelConfigCard.vue'
import AdminGuardrailsCard from '../components/admin/AdminGuardrailsCard.vue'
import AdminQueueMonitor from '../components/admin/AdminQueueMonitor.vue'

const { t } = useI18n()
const adminStore = useAdminStore()
const toastMessage = ref<string | null>(null)

function showToast(msg: string) {
  toastMessage.value = msg
  setTimeout(() => {
    toastMessage.value = null
  }, 3000)
}

async function handleSave() {
  const success = await adminStore.updateConfig(adminStore.config)
  if (success) showToast(t('admin.config_saved_msg'))
}

async function handleFlush() {
  const success = await adminStore.flushCache()
  if (success) showToast(t('admin.cache_flushed_msg'))
}

async function handleRetry() {
  const retried = await adminStore.retryFailedTasks()
  showToast(`${retried} ${t('admin.retry_failed_btn').toLowerCase()}`)
}

async function handleEnqueue() {
  await adminStore.enqueueDemoTask('export_invoices_reconcile')
  showToast('Tâche ajoutée à la file asynchrone')
}

onMounted(() => {
  adminStore.loadAll()
})
</script>

<template>
  <div class="space-y-6 pb-12">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200/80 pb-5">
      <div>
        <div class="flex items-center gap-3">
          <h1 class="text-2xl font-black tracking-tight text-slate-900">{{ t('admin.title') }}</h1>
          <span class="text-xs px-2.5 py-0.5 rounded-full font-bold bg-purple-50 text-purple-700 border border-purple-200">
            v1.0.0 API
          </span>
        </div>
        <p class="text-xs sm:text-sm text-slate-500 mt-1 max-w-2xl">{{ t('admin.subtitle') }}</p>
      </div>

      <div class="flex items-center gap-3">
        <div v-if="toastMessage" class="text-xs font-semibold px-3 py-1.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-lg shadow-sm">
          {{ toastMessage }}
        </div>
        <button
          class="text-xs font-medium px-3 py-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg shadow-sm transition"
          :disabled="adminStore.isLoading"
          @click="adminStore.loadAll()"
        >
          {{ adminStore.isLoading ? '...' : '↻ Actualiser' }}
        </button>
      </div>
    </div>

    <!-- 3 Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <AdminSystemHealthCard :health="adminStore.health" />
      <AdminModelConfigCard
        :config="adminStore.config"
        :is-saving="adminStore.isSaving"
        @update:config="adminStore.config = $event"
        @save="handleSave"
      />
      <AdminGuardrailsCard
        :config="adminStore.config"
        :is-saving="adminStore.isSaving"
        @update:config="adminStore.config = $event"
        @save="handleSave"
      />
    </div>

    <!-- Bottom Queue & Cache Monitor -->
    <AdminQueueMonitor
      :stats="adminStore.queueStats"
      :tasks="adminStore.recentTasks"
      @flush-cache="handleFlush"
      @retry-failed="handleRetry"
      @enqueue-demo="handleEnqueue"
    />
  </div>
</template>
