import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApiCall } from '@/api/useApiCall'
import type { UserResponse } from '@/api/types'

export interface AuthUser {
  id: number
  email: string
  first_name: string
  last_name: string
  organization: string
  is_verified: boolean
  role_ids: number[]
  role: 'GESTOR' | 'LECTOR'
}

const STORAGE_KEY = 'newsradar_auth'

function loadFromStorage(): { token: string; user: AuthUser } | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

function saveToStorage(token: string, user: AuthUser) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ token, user }))
}

function clearStorage() {
  localStorage.removeItem(STORAGE_KEY)
}

function resolveRole(roleIds: number[], roles: { id: number; name: string }[]): 'GESTOR' | 'LECTOR' {
  const userRoleNames = roles
    .filter((r) => roleIds.includes(r.id))
    .map((r) => r.name.toUpperCase())
  return userRoleNames.includes('GESTOR') ? 'GESTOR' : 'LECTOR'
}

export const useAuthStore = defineStore('auth', () => {
  const stored = loadFromStorage()
  const token = ref<string | null>(stored?.token ?? null)
  const user = ref<AuthUser | null>(stored?.user ?? null)

  const isAuthenticated = computed(() => token.value !== null && user.value !== null)
  const role = computed<'GESTOR' | 'LECTOR'>(() => user.value?.role ?? 'LECTOR')

  const api = useApiCall()

  async function login(email: string, password: string): Promise<void> {
    const tokenRes = await api.login({ email, password })
    const t = tokenRes.access_token

    const [users, roles] = await Promise.all([api.getUsers(t), api.getRoles(t)])

    const found = users.find((u: UserResponse) => u.email === email)
    if (!found) throw new Error('Usuario no encontrado tras el login')

    const authUser: AuthUser = {
      ...found,
      role: resolveRole(found.role_ids, roles),
    }

    token.value = t
    user.value = authUser
    saveToStorage(t, authUser)
  }

  function logout() {
    token.value = null
    user.value = null
    clearStorage()
  }

  function updateUser(updated: UserResponse, roles: { id: number; name: string }[]) {
    if (!user.value) return
    const authUser: AuthUser = {
      ...updated,
      role: resolveRole(updated.role_ids, roles),
    }
    user.value = authUser
    if (token.value) saveToStorage(token.value, authUser)
  }

  return { token, user, isAuthenticated, role, login, logout, updateUser }
})
