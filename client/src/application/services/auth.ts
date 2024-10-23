import axios from 'axios';
import router from '../../router';
import store from '../../store';


/**
 * クッキーから指定された名前のクッキーを取得
 * @param {*} name
 * @returns {string}
 */
function getCookie(name: string): string | null {
  let cookieValue: string | null = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


/**
 * axiosインスタンスを生成
 * @param {string} baseURL
 * @returns {AxiosInstance}
 */
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/auth/',
  withCredentials: true,
});


/**
 * リクエストインターセプター
 * @param {*} config
 * @returns {Promise} config
 */
apiClient.interceptors.request.use(
  (config) => {
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url.endsWith('login/') &&
      !originalRequest.url.endsWith('token/refresh/')
    ) {
      originalRequest._retry = true;
      try {
        await apiClient.post('token/refresh/');
        console.log(`Refresh token success`);
        return apiClient(originalRequest);
      } catch (refreshError) {
        store.commit('setAuthentication', false);
        router.push('/login');
        console.error(`Refresh token error: ${refreshError}`);
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
