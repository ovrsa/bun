import router from '@/router'
import apiClient from '@/services/auth'
import { AuthState } from '@/types/interfaces'
import { Module } from 'vuex'

const state: AuthState = {
  isAuthenticated: null,
  token: null,
  error: null,
}

const authModule: Module<AuthState, any> = {
  namespaced: true,
  state,
  mutations: {
    setAuthentication(state, status: boolean) {
      state.isAuthenticated = status
    },
  },
  actions: {
    async checkAuth({ commit }) {
      try {
        await apiClient.get('check-auth/')
        commit('setAuthentication', true)
      } catch (error) {
        commit('setAuthentication', false)
      }
    },
    async logout({ commit }) {
      try {
        await apiClient.post('logout/')
        commit('setAuthentication', false)
        router.push('/login')
      } catch (error) {
        console.error(`Error logging out: ${error}`)
      }
    },
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
  },
}

export default authModule
