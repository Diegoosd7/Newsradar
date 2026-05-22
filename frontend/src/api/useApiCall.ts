import type {
  LoginRequest,
  TokenResponse,
  RegisterRequest,
  UserResponse,
  UserUpdateRequest,
  RoleResponse,
  DashboardStatsResponse,
  CategoryResponse,
  InformationSourceResponse,
  InformationSourceCreateRequest,
  RssChannelResponse,
  RssChannelCreateRequest,
  AlertResponse,
  AlertCreateRequest,
  NotificationResponse,
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
      if (Array.isArray(body.detail)) {
        detail = body.detail
          .map((e: { loc?: unknown[]; msg?: string }) => {
            const field = Array.isArray(e.loc) ? e.loc.slice(1).join('.') : ''
            return field ? `${field}: ${e.msg}` : (e.msg ?? 'Validation error')
          })
          .join(' | ')
      } else if (typeof body.detail === 'string') {
        detail = body.detail
      } else if (body.detail) {
        detail = JSON.stringify(body.detail)
      }
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

  // Categories
  async function getCategories(token: string): Promise<CategoryResponse[]> {
    const res = await fetch(`${BASE_URL}/categories`, {
      headers: authHeaders(token),
    })
    return handleResponse<CategoryResponse[]>(res)
  }

  // Information Sources
  async function getSources(token: string): Promise<InformationSourceResponse[]> {
    const res = await fetch(`${BASE_URL}/information-sources`, {
      headers: authHeaders(token),
    })
    return handleResponse<InformationSourceResponse[]>(res)
  }

  async function createSource(
    token: string,
    data: InformationSourceCreateRequest,
  ): Promise<InformationSourceResponse> {
    const res = await fetch(`${BASE_URL}/information-sources`, {
      method: 'POST',
      headers: authHeaders(token),
      body: JSON.stringify(data),
    })
    return handleResponse<InformationSourceResponse>(res)
  }

  async function deleteSource(token: string, sourceId: number): Promise<void> {
    const res = await fetch(`${BASE_URL}/information-sources/${sourceId}`, {
      method: 'DELETE',
      headers: authHeaders(token),
    })
    return handleResponse<void>(res)
  }

  // RSS Channels (all)
  async function getAllChannels(token: string): Promise<RssChannelResponse[]> {
    const res = await fetch(`${BASE_URL}/rss-channels`, {
      headers: authHeaders(token),
    })
    return handleResponse<RssChannelResponse[]>(res)
  }

  // RSS Channels (per source)
  async function getSourceChannels(
    token: string,
    sourceId: number,
  ): Promise<RssChannelResponse[]> {
    const res = await fetch(
      `${BASE_URL}/information-sources/${sourceId}/rss-channels`,
      { headers: authHeaders(token) },
    )
    return handleResponse<RssChannelResponse[]>(res)
  }

  async function createSourceChannel(
    token: string,
    sourceId: number,
    data: RssChannelCreateRequest,
  ): Promise<RssChannelResponse> {
    const res = await fetch(
      `${BASE_URL}/information-sources/${sourceId}/rss-channels`,
      {
        method: 'POST',
        headers: authHeaders(token),
        body: JSON.stringify(data),
      },
    )
    return handleResponse<RssChannelResponse>(res)
  }

  async function deleteSourceChannel(
    token: string,
    sourceId: number,
    channelId: number,
  ): Promise<void> {
    const res = await fetch(
      `${BASE_URL}/information-sources/${sourceId}/rss-channels/${channelId}`,
      {
        method: 'DELETE',
        headers: authHeaders(token),
      },
    )
    return handleResponse<void>(res)
  }

  // Alerts (per user)
  async function getUserAlerts(token: string, userId: number): Promise<AlertResponse[]> {
    const res = await fetch(`${BASE_URL}/users/${userId}/alerts`, {
      headers: authHeaders(token),
    })
    return handleResponse<AlertResponse[]>(res)
  }

  async function createUserAlert(
    token: string,
    userId: number,
    data: AlertCreateRequest,
  ): Promise<AlertResponse> {
    const res = await fetch(`${BASE_URL}/users/${userId}/alerts`, {
      method: 'POST',
      headers: authHeaders(token),
      body: JSON.stringify(data),
    })
    return handleResponse<AlertResponse>(res)
  }

  async function deleteUserAlert(
    token: string,
    userId: number,
    alertId: number,
  ): Promise<void> {
    const res = await fetch(`${BASE_URL}/users/${userId}/alerts/${alertId}`, {
      method: 'DELETE',
      headers: authHeaders(token),
    })
    return handleResponse<void>(res)
  }

  // Notifications (per user)
  async function getUserNotifications(
    token: string,
    userId: number,
  ): Promise<NotificationResponse[]> {
    const res = await fetch(`${BASE_URL}/users/${userId}/notifications`, {
      headers: authHeaders(token),
    })
    return handleResponse<NotificationResponse[]>(res)
  }

  async function deleteAlertNotification(
    token: string,
    userId: number,
    alertId: number,
    notificationId: number,
  ): Promise<void> {
    const res = await fetch(
      `${BASE_URL}/users/${userId}/alerts/${alertId}/notifications/${notificationId}`,
      {
        method: 'DELETE',
        headers: authHeaders(token),
      },
    )
    return handleResponse<void>(res)
  }

  return {
    login,
    register,
    getUsers,
    updateUser,
    deleteUser,
    getRoles,
    getDashboardStats,
    getCategories,
    getSources,
    createSource,
    deleteSource,
    getAllChannels,
    getSourceChannels,
    createSourceChannel,
    deleteSourceChannel,
    getUserAlerts,
    createUserAlert,
    deleteUserAlert,
    getUserNotifications,
    deleteAlertNotification,
  }
}
