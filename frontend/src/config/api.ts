export const API_VERSION = 'v1'
export const API_SEMVER = '1.0.0'
export const API_BASE = `/api/${API_VERSION}`

export function apiPath(endpoint: string, version: string = API_VERSION): string {
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
  return `/api/${version}${cleanEndpoint}`
}

export async function apiFetch<T = any>(endpoint: string, options: RequestInit = {}): Promise<Response> {
  const url = endpoint.startsWith('http') || endpoint.startsWith('/api/') ? endpoint : apiPath(endpoint)
  const headers = new Headers(options.headers || {})

  if (!headers.has('X-API-Version')) {
    headers.set('X-API-Version', API_SEMVER)
  }

  // Attach JWT token from localStorage if present
  const token = localStorage.getItem('operia_token')
  if (token && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  return fetch(url, {
    ...options,
    headers,
  })
}
