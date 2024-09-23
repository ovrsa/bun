import { createStore } from 'vuex';
import apiClient from '../plugins/axios';
import router from '../router';

interface State {
  isAuthenticated: boolean | null;
}

const store = createStore<State>({
  state: {
    isAuthenticated: null,
  },
  mutations: {
    setAuthentication(state, status: boolean) {
      console.log('setAuthentication', status);
      state.isAuthenticated = status;
    },
  },
  actions: {
    async checkAuth({ commit }) {
      try {
        await apiClient.get('/check-auth/');
        commit('setAuthentication', true);
        console.log('認証済み');
      } catch (error) {
        commit('setAuthentication', false);
        console.error('未認証', error);
      }
    },
    async logout({ commit }) {
      try {
        await apiClient.post('logout/');
        console.log('ログアウトしました。');
      } catch (error) {
        console.error('ログアウトに失敗しました。', error);
      }
      commit('setAuthentication', false);
      router.push('/login');
      console.log('ログインページに遷移しました。');
    },
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
  },
});

export default store;
