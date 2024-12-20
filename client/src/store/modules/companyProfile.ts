import { fetchCompanyProfile as getCompanyProfile } from '@/services/companyProfiles'
import { CompanyProfile, CompanyProfileState } from '@/types/interfaces'
import { Module } from 'vuex'

const companyProfile: Module<CompanyProfileState, unknown> = {
  namespaced: true,
  state: {
    profile: null,
    loading: false,
    error: null,
  },
  mutations: {
    SET_COMPANY_PROFILE(state, profile: CompanyProfile) {
      state.profile = profile
      localStorage.setItem('companyProfile', JSON.stringify(profile))
    },
    SET_LOADING(state, status: boolean) {
      state.loading = status
    },
    SET_ERROR(state, error: string | null) {
      state.error = error
    },
    LOAD_PROFILE_FROM_STORAGE(state) {
      const storedProfile = localStorage.getItem('companyProfile')
      if (storedProfile) {
        state.profile = JSON.parse(storedProfile)
      }
    },
  },
  actions: {
    async fetchCompanyProfile({ commit }, symbol: string) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const profile = await getCompanyProfile(symbol)
        commit('SET_COMPANY_PROFILE', profile)
      } catch (error) {
        commit('SET_ERROR', 'Failed to fetch company profile.')
      } finally {
        commit('SET_LOADING', false)
      }
    },
    loadProfileFromStorage({ commit }) {
      commit('LOAD_PROFILE_FROM_STORAGE')
    },
  },
  getters: {
    profile: state => state.profile,
    loading: state => state.loading,
    error: state => state.error,
  },
}

export default companyProfile
