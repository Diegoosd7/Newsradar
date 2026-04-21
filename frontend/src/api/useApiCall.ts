import type {
  LoginRequest,
  TokenResponse,
  RegisterRequest,
  UserResponse,
  UserUpdateRequest,
  RoleResponse,
  DashboardStatsResponse,
} from './types'

const BASE_URL = '/api/v1'

function authHeaders(token: string): HeadersInit {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  }
}

function jsonHeaders(): HeadersInit {
  return { 'Content-Type': 'application/json' }
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = `Error ${res.status}`
    try {
      const body = await res.json()
      detail = body.detail ?? detail
    } catch {
      // ignore parse error
    }
    throw new Error(detail)
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

export function useApiCall() {
  async function login(data: LoginRequest): Promise<TokenResponse> {
    const res = await fetch(`${BASE_URL}/auth/login`, {
      method: 'POST',
      headers: jsonHeaders(),
      body: JSON.stringify(data),
    })
    return handleResponse<TokenResponse>(res)
  }

  async function register(data: RegisterRequest): Promise<UserResponse> {
    const res = await fetch(`${BASE_URL}/auth/register`, {
      method: 'POST',
      headers: jsonHeaders(),
      body: JSON.stringify(data),
    })
    return handleResponse<UserResponse>(res)
  }

  async function getUsers(token: string): Promise<UserResponse[]> {
    const res = await fetch(`${BASE_URL}/users/`, {
      headers: authHeaders(token),
    })
    return handleResponse<UserResponse[]>(res)
  }

  async function updateUser(
    token: string,
    userId: number,
    data: UserUpdateRequest,
  ): Promise<UserResponse> {
    const res = await fetch(`${BASE_URL}/users/${userId}`, {
      method: 'PUT',
      headers: authHeaders(token),
      body: JSON.stringify(data),
    })
    return handleResponse<UserResponse>(res)
  }

  async function deleteUser(token: string, userId: number): Promise<void> {
    const res = await fetch(`${BASE_URL}/users/${userId}`, {
      method: 'DELETE',
      headers: authHeaders(token),
    })
    return handleResponse<void>(res)
  }

  async function getRoles(token: string): Promise<RoleResponse[]> {
    const res = await fetch(`${BASE_URL}/roles/`, {
      headers: authHeaders(token),
    })
    return handleResponse<RoleResponse[]>(res)
  }

  async function getDashboardStats(token: string): Promise<DashboardStatsResponse> {
    const res = await fetch(`${BASE_URL}/stats/dashboard`, {
      headers: authHeaders(token),
    })
    return handleResponse<DashboardStatsResponse>(res)
  }

  return {
    login,
    register,
    getUsers,
    updateUser,
    deleteUser,
    getRoles,
    getDashboardStats,
  }
}