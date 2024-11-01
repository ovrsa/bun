import { Module } from 'vuex'
import { SymbolState } from '@/types/interfaces'

const state: SymbolState = {
  selectedSymbol: null,
}

const symbolModule: Module<SymbolState, string> = {
  namespaced: true,
  state,
  mutations: {
    SET_SELECTED_SYMBOL(state, symbol: string) {
      state.selectedSymbol = symbol
    },
    CLEAR_SELECTED_SYMBOL(state) {
      state.selectedSymbol = null
    },
  },
  actions: {
    updateSelectedSymbol({ commit }, symbol: string) {
      commit('SET_SELECTED_SYMBOL', symbol)
    },
    clearSelectedSymbol({ commit }) {
      commit('CLEAR_SELECTED_SYMBOL')
    },
  },
  getters: {
    selectedSymbol: state => state.selectedSymbol,
  },
}

export default symbolModule
