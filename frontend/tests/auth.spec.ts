import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '../src/stores/auth'

describe('useAuthStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.restoreAllMocks()
  })

  it('initializes with no token when localStorage is empty', () => {
    const auth = useAuthStore()
    expect(auth.isAuthenticated).toBe(false)
    expect(auth.token).toBeNull()
    expect(auth.user).toBeNull()
  })

  it('initializes with token when present in localStorage', () => {
    localStorage.setItem('operia_token', 'test-jwt-token')
    const auth = useAuthStore()
    expect(auth.isAuthenticated).toBe(true)
    expect(auth.token).toBe('test-jwt-token')
  })

  it('logs in successfully and persists token', async () => {
    const auth = useAuthStore()
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        access_token: 'mock-jwt-token',
        user: { id: 'user-admin', email: 'admin@operia.io', full_name: 'Alex Martin', role: 'ADMIN', department: 'Finance' },
      }),
    } as any)

    const success = await auth.login('admin@operia.io', 'admin123')
    expect(success).toBe(true)
    expect(auth.token).toBe('mock-jwt-token')
    expect(auth.user?.email).toBe('admin@operia.io')
    expect(auth.isAuthenticated).toBe(true)
    expect(localStorage.getItem('operia_token')).toBe('mock-jwt-token')
  })

  it('handles login failure cleanly', async () => {
    const auth = useAuthStore()
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: async () => ({ detail: 'Identifiants invalides' }),
    } as any)

    const success = await auth.login('admin@operia.io', 'wrong')
    expect(success).toBe(false)
    expect(auth.token).toBeNull()
    expect(auth.loginError).toBe('Identifiants invalides')
    expect(auth.isAuthenticated).toBe(false)
  })

  it('logs out and clears token from localStorage', () => {
    localStorage.setItem('operia_token', 'active-token')
    const auth = useAuthStore()
    expect(auth.isAuthenticated).toBe(true)

    auth.logout()
    expect(auth.token).toBeNull()
    expect(auth.user).toBeNull()
    expect(auth.isAuthenticated).toBe(false)
    expect(localStorage.getItem('operia_token')).toBeNull()
  })
})
