import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiFetch } from '../config/api'

export interface AuthUser {
  id: string
  email: string
  full_name: string
  role: string
  department: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('operia_token'))
  const user = ref<AuthUser | null>(null)
  const loginError = ref<string | null>(null)
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!token.value)

  async function login(email: string, password: string): Promise<boolean> {
    isLoading.value = true
    loginError.value = null
    try {
      const res = await apiFetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      if (res.ok) {
        const data = await res.json()
        token.value = data.access_token
        user.value = data.user
        localStorage.setItem('operia_token', data.access_token)
        return true
      }
      const err = await res.json().catch(() => ({ detail: 'Erreur de connexion' }))
      loginError.value = err.detail || 'Email ou mot de passe invalide'
      return false
    } catch {
      loginError.value = 'Impossible de contacter le serveur'
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMe(): Promise<void> {
    if (!token.value) return
    try {
      const res = await apiFetch('/auth/me')
      if (res.ok) {
        user.value = await res.json()
      } else if (res.status === 401) {
        logout()
      }
    } catch {
      // Server unreachable — keep token for retry
    }
  }

  function logout(): void {
    token.value = null
    user.value = null
    localStorage.removeItem('operia_token')
  }

  return {
    token,
    user,
    loginError,
    isLoading,
    isAuthenticated,
    login,
    fetchMe,
    logout,
  }
})
