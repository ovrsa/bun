import { Module } from 'vuex'
import { fetchStockPrices as getStockPrices } from '@/application/services/stockPrices'
import { stockPricesState } from '@/types/interfaces'

const stockPricesModule: Module<stockPricesState, unknown> = {
  namespaced: true,
  state: {
    data: null,
    loading: false,
    error: null,
  },
  mutations: {
    SET_STOCK_PRICES(state, stockPrices: stockPricesState[]) {
      state.data = stockPrices
      localStorage.setItem('stockPrices', JSON.stringify(stockPrices))
    },
    SET_LOADING(state, status: boolean) {
      state.loading = status
    },
    SET_ERROR(state, error: string | null) {
      state.error = error
    },
    LOAD_STOCK_PRICES_FROM_STORAGE(state) {
      const storedStockPrices = localStorage.getItem('stockPrices')
      if (storedStockPrices) {
        state.data = JSON.parse(storedStockPrices)
      }
    },
  },
  actions: {
    async fetchStockPrices({ commit }, symbol: string) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const stockPrices = await getStockPrices(symbol)
        commit('SET_STOCK_PRICES', stockPrices)
      } catch (error) {
        commit('SET_ERROR', 'Failed to fetch stock prices.')
      } finally {
        commit('SET_LOADING', false)
      }
    },
    loadStockPricesFromStorage({ commit }) {
      commit('LOAD_STOCK_PRICES_FROM_STORAGE')
    },
  },
  getters: {
    stockPrices: state => state.data,
    loading: state => state.loading,
    error: state => state.error,
  },
}

export default stockPricesModule
