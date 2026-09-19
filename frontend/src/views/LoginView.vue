<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-brand-50/30 to-slate-100 flex items-center justify-center p-4">
    <div class="w-full max-w-sm">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="w-12 h-12 bg-brand-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg shadow-brand-600/20">
          <BrainCircuit class="w-6 h-6 text-white" />
        </div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">OpérIA</h1>
        <p class="text-sm text-slate-500 mt-1">{{ t('login.subtitle') }}</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleLogin" class="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-sm space-y-5">
        <div v-if="auth.loginError" class="p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-700 font-medium">
          {{ auth.loginError }}
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1.5">{{ t('login.email') }}</label>
          <input
            v-model="email" type="email" required autocomplete="email"
            class="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500 transition"
            placeholder="admin@operia.io"
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1.5">{{ t('login.password') }}</label>
          <input
            v-model="password" type="password" required autocomplete="current-password"
            class="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500 transition"
            placeholder="••••••••"
          />
        </div>

        <button
          type="submit" :disabled="auth.isLoading"
          class="w-full py-2.5 bg-brand-600 hover:bg-brand-700 disabled:opacity-50 text-white rounded-xl text-sm font-semibold shadow-sm shadow-brand-600/20 transition flex items-center justify-center gap-2"
        >
          <Loader2 v-if="auth.isLoading" class="w-4 h-4 animate-spin" />
          <LogIn v-else class="w-4 h-4" />
          {{ auth.isLoading ? t('login.loading') : t('login.submit') }}
        </button>

        <p class="text-[11px] text-slate-400 text-center">
          {{ t('login.default_hint') }}
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { BrainCircuit, LogIn, Loader2 } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'
import { useI18n } from '../composables/useI18n'

const auth = useAuthStore()
const router = useRouter()
const { t } = useI18n()

const email = ref('admin@operia.io')
const password = ref('')

async function handleLogin() {
  const ok = await auth.login(email.value, password.value)
  if (ok) {
    router.push('/')
  }
}
</script>
