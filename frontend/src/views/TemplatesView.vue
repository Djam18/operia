<template>
  <div class="p-8 max-w-7xl mx-auto flex flex-col gap-8">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">{{ t('templates.title') }}</h1>
        <p class="text-sm text-slate-500 mt-0.5">{{ t('templates.subtitle') }}</p>
      </div>
      <UiTabs :items="categoryTabs" v-model="activeCategory" />
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <PlaybookCard
        v-for="playbook in filteredPlaybooks"
        :key="playbook.id"
        :playbook="playbook"
        :launch-label="t('templates.btn_launch')"
        @launch="runPlaybook"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import UiTabs, { type TabItem } from '../components/ui/UiTabs.vue'
import PlaybookCard from '../components/templates/PlaybookCard.vue'
import { PLAYBOOKS, type Playbook } from '../data/playbooks'
import { useI18n } from '../composables/useI18n'
import { apiFetch } from '../config/api'

const { t } = useI18n()
const router = useRouter()
const activeCategory = ref<string>('all')
const playbooksList = ref<Playbook[]>(PLAYBOOKS)

onMounted(async () => {
  try {
    const res = await apiFetch('/templates')
    if (res.ok) {
      const serverTpls = await res.json()
      // Merge with default details
      playbooksList.value = serverTpls.map((st: any) => {
        const found = PLAYBOOKS.find(p => p.id === st.id)
        return found || {
          id: st.id,
          title: st.title,
          category: st.category,
          source: st.source,
          duration: st.duration,
          description: `Playbook opérationnel automatisé pour ${st.category}`,
          defaultPrompt: `Exécute l'action '${st.title}' sur le périmètre configuré.`
        }
      })
    }
  } catch {
    // Keep default PLAYBOOKS
  }
})

const categoryTabs = computed<TabItem[]>(() => [
  { label: 'Toutes les recettes', value: 'all' },
  { label: t('templates.tag_finance'), value: 'Finance' },
  { label: t('templates.tag_crm'), value: 'CRM' },
  { label: t('templates.tag_audit'), value: 'Audit' },
])

const filteredPlaybooks = computed<Playbook[]>(() => {
  if (activeCategory.value === 'all') return playbooksList.value
  return playbooksList.value.filter((pb) => pb.category === activeCategory.value)
})

function runPlaybook(playbook: Playbook): void {
  router.push({
    path: '/agent',
    query: { prompt: playbook.defaultPrompt },
  })
}
</script>
