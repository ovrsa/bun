import axios, {
  AxiosError,
  AxiosHeaders,
  InternalAxiosRequestConfig,
} from 'axios'
import store from '../store'

/**
 * 認証用のクライアント
 * 認証ではCSRFトークンをヘッダーに追加する必要があるため、
 * 責務を分離するために新たにクライアントを作成
 */
const authClient = axios.create({
  baseURL: `${import.meta.env.VITE_BASE_URL}/auth/`,
  withCredentials: true, // Cookieを送信するために必要
})

/**
 * クッキーから指定した名前のクッキーを取得
 * @param name クッキー名
 * @returns クッキーの値または null
 */
export function getCookie(name: string): string | null {
  let cookieValue: string | null = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';') // クッキーを取得
    // クッキーを1つずつ処理
    for (let cookie of cookies) {
      cookie = cookie.trim()
      if (cookie.startsWith(`${name}=`)) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

/**
 * リクエスト時にCSRFトークンをヘッダーに追加
 */
authClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const csrfToken = getCookie('csrftoken')
    if (csrfToken) {
      // headers が undefined の場合、AxiosHeaders インスタンスを作成
      if (!config.headers || !(config.headers instanceof AxiosHeaders)) {
        config.headers = new AxiosHeaders(config.headers)
      }

      // AxiosHeaders のメソッドを使用してトークンを設定
      if (config.headers instanceof AxiosHeaders) {
        config.headers.set('X-CSRFToken', csrfToken)
      }
    }
    return config
  },
  (error: AxiosError) => Promise.reject(error)
)

/**
 * レスポンス時にトークンのリフレッシュを行う
 */
authClient.interceptors.response.use(
  response => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean
    }

    // トークンが期限切れの場合
    if (error.response?.status === 401 && !originalRequest._retry) {
      const refreshToken = getCookie('refresh_token')
      if (!refreshToken) {
        store.commit('auth/setAuthentication', false) // 認証状態を解除
        return Promise.reject(error)
      }

      originalRequest._retry = true
      try {
        await authClient.post('token/refresh/', { refresh: refreshToken })
        return authClient(originalRequest)
      } catch (refreshError) {
        store.commit('auth/setAuthentication', false)
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default authClient
