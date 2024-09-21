// src/plugins/axios.js

import axios from 'axios';
import router from '../router';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/',
  withCredentials: true, // クッキーを送信する
});

// レスポンスインターセプター（必要に応じて）
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        await apiClient.post('token/refresh/');
        return apiClient(originalRequest);
      } catch (refreshError) {
        // リフレッシュトークンが無効な場合、ログアウト処理を行う
        // 必要に応じてstateを更新
        router.push('/login');
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
