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

// Dashboard stats
export interface CategoryCountItem {
  category_code: string
  category_label: string
  count: number
}

export interface TrendingWordItem {
  text: string
  value: number
}

export interface TrendingCategoryItem {
  category_code: string
  category_label: string
  words: TrendingWordItem[]
}

export interface DashboardSummary {
  sources: number
  rss_channels: number
  news: number
  alerts: number
}

export interface DashboardStatsResponse {
  summary: DashboardSummary
  news_by_category: CategoryCountItem[]
  alerts_by_category: CategoryCountItem[]
  trending_by_category: TrendingCategoryItem[]
}

// Categories (IPTC)
export interface CategoryResponse {
  id: number
  name: string
  source: string
}

// Information Sources
export interface InformationSourceResponse {
  id: number
  name: string
  url: string
}

export interface InformationSourceCreateRequest {
  name: string
  url: string
}

// RSS Channels
export interface RssChannelResponse {
  id: number
  url: string
  category_id: number
  information_source_id: number
}

export interface RssChannelCreateRequest {
  url: string
  category_id: number
}

// Alerts
export interface AlertCategoryItem {
  code: string
  label: string
}

export interface AlertResponse {
  id: number
  user_id: number
  name: string
  descriptors: string[]
  categories: AlertCategoryItem[]
  rss_channels_ids: number[]
  information_sources_ids: number[]
  cron_expression: string
}

export interface AlertCreateRequest {
  name: string
  descriptors: string[]
  categories: AlertCategoryItem[]
  rss_channels_ids: number[]
  information_sources_ids: number[]
  cron_expression: string
}

// Notifications
export interface NotificationMetric {
  name: string
  value: number
}

export interface NotificationResponse {
  id: number
  alert_id: number
  timestamp: string
  metrics: NotificationMetric[]
  news_item_id: number | null
  matched_descriptor: string | null
  is_read: boolean
  news_title: string | null
  news_summary: string | null
  news_url: string | null
  news_published: string | null
  source_name: string | null
}