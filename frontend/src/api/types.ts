// Auth
export interface LoginRequest {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface RegisterRequest {
  email: string
  first_name: string
  last_name: string
  organization: string
  password: string
  role_ids?: number[]
}

// Users
export interface UserResponse {
  id: number
  email: string
  first_name: string
  last_name: string
  organization: string
  role_ids: number[]
  is_verified: boolean
}

export interface UserUpdateRequest {
  email?: string
  first_name?: string
  last_name?: string
  organization?: string
  password?: string
  role_ids?: number[]
}

// Roles
export interface RoleResponse {
  id: number
  name: string
}
