import { fetchCompanyFinancials as getCompanyFinancials } from '@/services/companyFinancials'
import { CompanyFinancials, CompanyFinancialsState } from '@/types/interfaces'
import { Module } from 'vuex'

const companyFinancials: Module<CompanyFinancialsState, unknown> = {
  namespaced: true,
  state: {
    data: null,
    loading: false,
    error: null,
  },
  mutations: {
    SET_COMPANY_FINANCIALS(state, data: CompanyFinancials) {
      state.data = data
      localStorage.setItem('companyFinancials', JSON.stringify(data))
    },
    SET_LOADING(state, status: boolean) {
      state.loading = status
    },
    SET_ERROR(state, error: string | null) {
      state.error = error
    },
    LOAD_FINANCIALS_FROM_STORAGE(state) {
      const storedData = localStorage.getItem('companyFinancials')
      if (storedData) {
        state.data = JSON.parse(storedData)
      }
    },
  },
  actions: {
    async fetchCompanyFinancials({ commit }, symbol: string) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const data = await getCompanyFinancials(symbol)
        commit('SET_COMPANY_FINANCIALS', data)
      } catch (error) {
        commit('SET_ERROR', 'Failed to fetch company financials.')
      } finally {
        commit('SET_LOADING', false)
      }
    },
    loadFinancialsFromStorage({ commit }) {
      commit('LOAD_FINANCIALS_FROM_STORAGE')
    },
  },
  getters: {
    data: state => state.data,
    loading: state => state.loading,
    error: state => state.error,
  },
}

export default companyFinancials
